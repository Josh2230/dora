from dora import Node
import logging
import pyarrow as pa

def main():
    node = Node()
    for i in range(50):
        data = pa.array(["bye"])
        node.send_output("input_two", data)
        # logging.info("sender two sent: %s", data)

        event = node.next(0.1)
        if event is not None and event["type"] == "STOP":
            logging.info("stopping sender two early")
            break

    logging.info("Sender two finished")

if __name__ == "__main__":
    main()
