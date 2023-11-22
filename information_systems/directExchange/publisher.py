import pika
import sys
import os
from time import sleep
from random import randint
import threading

# priorities:
# 
# high-priority
# medium-priority
# low-priority

IP_ADDRESS = "localhost"
EXCHANGE = "direct_logs"
EXCHANGE_TYPE = "direct"
MIN_TIME_TO_WAIT = 1
priorities = {"high-priority": 2, 
              "medium-priority": 4, 
              "low-priority": 6}
stop_flag = False

def main(priority_delay, priority_name):
    counter = 0
    while not stop_flag:
        sleep(priority_delay)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=IP_ADDRESS))
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, 
                                 exchange_type=EXCHANGE_TYPE)

        counter += 1
        message = f"Number of [{priority_name}] messages: {counter}"
        
        body = bytes(message, encoding="utf-8")

        channel.basic_publish(exchange=EXCHANGE,
                              routing_key=priority_name,
                              body=body)

        print(f"\t [{priority_name}] message is sent to direct exchange: [N:{counter}]")


if __name__ == "__main__":
    threads = []
    try:
        for priority, max_time_to_wait in priorities.items():
            time_to_wait = randint(MIN_TIME_TO_WAIT, max_time_to_wait)
            threads.append(threading.Thread(target=main, args=(time_to_wait, priority)))
        
        [t.start() for t in threads]

        # Wait for the user to press Ctrl+C
        while True:
            sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        [t.join() for t in threads]
        print('Interrupted')
        try: 
            sys.exit(0)
        except SystemError:
            os._exit(0)
    
        