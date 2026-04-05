from dora import Node
import logging

def main():
    node = Node()

    ticks = 0
    seconds = 0
    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            event_id = event["id"]

            if event_id == "tick":
                ticks += 1
                if ticks % 2 == 0:
                    seconds += 1
                    logging.info("One second passed. Current second: %d",seconds)


if __name__ == "__main__":
    main()
