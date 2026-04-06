import rerun as rr
import time
from dora import Node
import logging

def main():
    node = Node()
    # initializes rerun with the name "my_app", spawn = True auto opens rerun for you
    rr.init("my_app", spawn=True)

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            input_id = event["id"]

            if input_id == "input_one":
                data = event["value"].to_pylist()[0]

                # loop from sender one takes 0.1 seconds per iteration so we can simulate real time by multiplying 0.1
                rr.set_time("time", duration=data["time"] * 0.1)
                rr.log("avg_speed", rr.Scalars(data["avg_speed"]))
                rr.log("distance", rr.Scalars(data["distance"]))

                logging.info("logged data to rerun: avg_speed=%s distance=%s", data["avg_speed"], data["distance"])


        elif event_type == "STOP":
            logging.info("Stopping csv_logger_node early")
            break

if __name__ == "__main__":
    main()
