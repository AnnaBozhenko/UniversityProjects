import pika
import sys
import os

IP_ADDRESS = "localhost"
QUEUE = "hugs_dispatcher"
MIN_TIME_TO_SLEEP = 2
MAX_TIME_TO_SLEEP = 5

def main():
    global counter

    # set up connection to broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(IP_ADDRESS))
    # set up channel
    channel = connection.channel()
    # set up queue
    channel.queue_declare(queue=QUEUE, 
                          durable=False, 
                          exclusive=False, 
                          auto_delete=False)
    
    def callback(ch, method, properties, body):
        global counter
        
        message = body.decode("utf-8")
        counter += 1
        print(f"Received message: {message}, total number of messages: {counter}")
    
    channel.basic_consume(queue=QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)
    
    print(f"Subscribed to the queue '{QUEUE}'")
    channel.start_consuming()


if __name__ == "__main__":
    counter = 0
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemError:
            os._exit(0)
