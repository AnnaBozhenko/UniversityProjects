import pika
import sys
import os

IP_ADDRESS = "localhost"
EXCHANGE = "direct_logs"
EXCHANGE_TYPE = "direct"
priority_name = "medium-priority"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=IP_ADDRESS))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, 
                             exchange_type=EXCHANGE_TYPE)


    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(queue=queue_name, 
                       exchange=EXCHANGE,
                       routing_key=priority_name)

    def callback(ch, method, properties, body):
        message = body.decode("utf-8")
        print(f"Received message: [{message}]")

    channel.basic_consume(queue=queue_name, 
                          on_message_callback=callback,
                          auto_ack=True)

    print(f"Waiting for [{priority_name}] messages...")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemError:
            os._exit(0)


