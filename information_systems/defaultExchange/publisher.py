import pika
from random import randint
from time import sleep
import os
import sys

IP_ADDRESS = "localhost"
QUEUE = "hugs_dispatcher"
MIN_TIME_TO_SLEEP = 2
MAX_TIME_TO_SLEEP = 5

def main():
    counter = 0
    while (True):
        time_to_sleep = randint(MIN_TIME_TO_SLEEP, MAX_TIME_TO_SLEEP)
        sleep(time_to_sleep)

        # set up connection to broker
        connection = pika.BlockingConnection(pika.ConnectionParameters(IP_ADDRESS))
        # set up channel
        channel = connection.channel()
        # set up queue
        channel.queue_declare(queue=QUEUE, 
                              durable=False, 
                              exclusive=False, 
                              auto_delete=False)
        
        message = f"Number of people needing hugs since the app run: {counter}"
        counter += 1
        body = bytes(message, encoding="utf-8")

        channel.basic_publish(exchange="",
                              routing_key=QUEUE,
                              body=body)
        
        print(f"Message is sent to Default Exchange [N:{counter}]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemError:
            os._exit(0)
