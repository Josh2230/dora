from dora import Node
import logging


def main():
    node = Node()
    input_one_data = None
    input_two_data = None

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            input_id = event["id"]

            if input_id == "input_one":
                input_one_data = event["value"].to_pylist()
                logging.info("received data %s", input_one_data)

            elif input_id == "input_two":
                input_two_data = event["value"].to_pylist()
                logging.info("received data %s", input_two_data)

            if input_one_data and input_two_data:
                combined_data = input_one_data + input_two_data
                logging.info("combined data: %s", combined_data)

                input_one_data = None
                input_two_data = None

        elif event_type == "STOP":
            logging.info(
                "Multi Node receiver stopping after receiving event: %s", event
            )
            break


if __name__ == "__main__":
    main()
