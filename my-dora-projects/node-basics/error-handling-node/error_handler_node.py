from dora import Node
import logging
import random


def main():
    # need to setup basic congif to let logging print at the info level because it's not configured
    # for us if we use just a single node compared to multiple nodes with inputs and outputs
    logging.basicConfig(level=logging.INFO)
    logging.info("reached start")
    node = Node()
    CONST = 1
    logging.info("Node initialized")

    while True:
        # randomly catch an error and gracefully move on
        try:
            divisor = random.randint(0, 4)
            some_val = CONST / divisor
        except ZeroDivisionError:
            logging.info("ERROR: Zero Division Error")

        logging.info("Checking for events")
        event = node.next(timeout=0.1)
        if event and event["type"] == "STOP":
            logging.info("Stopping main node")
            break


if __name__ == "__main__":
    main()
