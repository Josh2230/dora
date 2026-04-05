from dora import Node
import logging
import pyarrow as pa
import random


def main():
    node = Node()
    for i in range(50):
        data = pa.array(
            [
                {
                    "type": 1,
                    "speed": random.randint(0, 50),
                    "status": random.randint(0, 1),
                    "distance": random.randint(0, 15) * i,
                }
            ]
        )

        node.send_output("input_one", data)

        event = node.next(timeout=0.1)

        if event and event["type"] == "STOP":
            logging.info("Stopping sender_one early")
            break

if __name__ == "__main__":
    main()
