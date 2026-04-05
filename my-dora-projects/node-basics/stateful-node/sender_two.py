from dora import Node
import pyarrow as pa
import logging
import random

def main():
    node = Node()

    for i in range(50):
        data = pa.array([random.randint(0, 10)])
        node.send_output("input_two", data)
        logging.info("Sender two sent: %s", data)

        event = node.next(0.1)

        if event is not None and event["type"] == "STOP":
            logging.info("stopping sender one early")
            break

    logging.info("Sender two finished")

if __name__ == "__main__":
    main()
