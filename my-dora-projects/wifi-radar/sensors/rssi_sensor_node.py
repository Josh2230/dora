from dora import Node
import logging
import random
import time
import pyarrow as pa

def main():
    # simulate mock rssi data to send to kalman filter
    # real thing will be its own process per unique phone to send data to kalman filter
    # phone 1 -> kalman filter, phone 2 -> kalman filter... etc

    node = Node()
    for i in range(100):
        rssi_data = -random.uniform(65, 80)
        current_time = time.time()

        data = pa.array([rssi_data, current_time])
        node.send_output("rssi_data", data)

        event = node.next(0.1)
        if event and event["type"] == "STOP":
            logging.info("stopping rssi sensor node early")
            break

if __name__ == "__main__":
    main()
