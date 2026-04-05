from dora import Node
import logging
import pyarrow as pa


def main():
    node = Node()
    speed = 0
    distance = 0
    count = 0

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":

            input_id = event["id"]

            if input_id == "input_one":
                data = event["value"].to_pylist()[0]
                speed += data["speed"]
                distance += data["distance"]
                count += 1

                avg_speed = speed / count
                avg_distance = distance / count

                node.send_output("avg_speed", pa.array([avg_speed], type=pa.float32()), {"primitive": "series"})
                node.send_output("avg_distance", pa.array([avg_distance], type=pa.float32()), {"primitive": "series"})


        elif event["type"] == "STOP":
            logging.info("Stopping sender_two early")
            break

if __name__ == "__main__":
    main()
