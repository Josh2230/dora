import numpy as np
import cv2 as cv
from dora import Node
import logging
import pyarrow as pa

def main():

    node = Node()

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            input_id = event["id"]

            if input_id == "tick":

                # Capture frame-by-frame
                ret, frame = cap.read()
                fps = cap.get(cv.CAP_PROP_FPS)

                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Our operations on the frame come here
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                # Display the resulting frame
                cv.imshow('frame', frame)

                data = pa.array(frame.ravel())
                metadata = event["metadata"]
                metadata.pop("timestamp", None)
                metadata["encoding"] = "bgr8"
                metadata["width"] = int(frame.shape[1])
                metadata["height"] = int(frame.shape[0])
                metadata["primitive"] = "image"

                node.send_output("frame", data, metadata)
                if cv.waitKey(1) == ord('q'):
                    break

        elif event_type == "STOP":
            # When everything done, release the capture
            cap.release()
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
