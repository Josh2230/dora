from dora import Node
import pyarrow as pa
import logging

def main():
    node = Node()

    for i in range(50):
        data = pa.array(["hello"])
        node.send_output("input_one", data)
        # logging.info("Sender one sent: %s", data)


        event = node.next(0.1)

        if event is not None and event["type"] == "STOP":
            logging.info("stopping sender one early")
            break

    logging.info("Sender one finished")

if __name__ == "__main__":
    main()
