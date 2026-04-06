from dora import Node
import logging

def main():
    node = Node()
    frame_count = 0
    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            input_id = event["id"]

            if input_id == "frame":
                frame_count += 1
                # logging.info("Received frame %s ", data)
                logging.info("Current frame: %d", frame_count)


        elif event_type == "STOP":
            logging.info("Stopping frame counter")
            break

if __name__ == "__main__":
    main()
