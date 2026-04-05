from dora import Node
import logging
import pyarrow as pa

def main():
    node = Node()
    count = 0
    total = 0
    avg = 0
    for event in node:
        event_type = event["type"]
        if event_type == "INPUT":
            input_id = event["id"]

            if input_id == "input_one":
                sender_one_data = event["value"].to_pylist()[0]
                count += 1
                total += sender_one_data
                avg = total/count
                logging.info("Stateful Node current avg: %s", avg)

            elif input_id == "input_two":
                sender_two_data = event["value"].to_pylist()[0]
                count += 1
                total += sender_two_data
                avg = total/count
                logging.info("Stateful Node current avg: %s", avg)

        elif event_type == "STOP":
            logging.info("Stateful node stopping early")
            break

if __name__ == "__main__":
    main()


