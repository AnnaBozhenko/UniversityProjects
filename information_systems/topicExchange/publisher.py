import pika
import sys
from datetime import date

IP_ADDRESS = "localhost"
EXCHANGE = "topic_logs"
EXCHANGE_TYPE = "topic"

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=IP_ADDRESS))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

    routing_key = sys.argv[1] if len(sys.argv) > 1 else "anonimous.info"

    message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "No messages yet, take a hug instead!"
    body = bytes(message, encoding="utf-8")

    channel.basic_publish(exchange=EXCHANGE, 
                          routing_key=routing_key,
                          body=body)

    print(f"Sent: [{routing_key}] with content: [{message}]")

    channel.close()

if __name__ == "__main__":
    main()

