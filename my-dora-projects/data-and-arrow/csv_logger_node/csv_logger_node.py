from dora import Node
import logging

def main():
    node = Node()

    with open("data.csv", "w") as f:

        for event in node:
            event_type = event["type"]

            if event_type == "INPUT":
                input_id = event["id"]

                if input_id == "input_one":
                    data = str(event["value"].to_pylist())
                    logging.info("writing data from sender_one to file")
                    f.write(data + "\n")
                    f.flush()

            elif event_type == "STOP":
                logging.info("Stopping csv_logger_node early")
                f.flush()
                break

if __name__ == "__main__":
    main()
