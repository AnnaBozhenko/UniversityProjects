import pika
import sys
import os

IP_ADDRESS = "localhost"
EXCHANGE = "topic_logs"
EXCHANGE_TYPE = "topic"

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]

    for b_k in binding_keys:
        channel.queue_bind(queue=queue_name,
                           exchange=EXCHANGE,
                           routing_key=b_k)

    print("Waiting for logs...")

    def callback(ch, method, properties, body):
        message_type = method.routing_key.split(".")[-1]
        body = body.decode("utf-8")
        print(f"Received [{message_type}]:[{body}]")

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemError:
            os._exit(0)
