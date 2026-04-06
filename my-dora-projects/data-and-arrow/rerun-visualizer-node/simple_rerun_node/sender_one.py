from dora import Node
import logging
import pyarrow as pa
import random


def main():
    node = Node()
    total_distance = 0
    total_speed = 0
    count = 0
    for i in range(101):
        curr_speed = random.randint(0, 50)
        total_speed += curr_speed
        curr_distance = curr_speed * 0.1
        total_distance += curr_distance
        count += 1


        avg_speed = total_speed / count
        data = pa.array(
            [
                {
                    "time": i,
                    "type": 1,
                    "avg_speed": avg_speed,
                    "status": random.randint(0, 1),
                    "distance": total_distance,
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
