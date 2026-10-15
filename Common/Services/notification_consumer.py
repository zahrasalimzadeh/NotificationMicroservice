import os
import pika


class NotificationConsumer:
    def __init__(self, process_message):
        self.process_message = process_message

    def start(self):
        credentials = pika.PlainCredentials(
            username=os.getenv("RABBITMQ_USERNAME"),
            password=os.getenv("RABBITMQ_PASSWORD")
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
            virtual_host=os.getenv("RABBITMQ_VIRTUAL_HOST"),
            credentials=credentials
        )

        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.exchange_declare(
            exchange="notification-exchange",
            exchange_type="direct",
            durable=True
        )

        channel.queue_declare(
            queue="notification-queue",
            durable=True
        )

        channel.queue_bind(
            queue="notification-queue",
            exchange="notification-exchange",
            routing_key="notification"
        )

        def consume_message(ch, method, properties, body):
            self.process_message(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Consume Completed!---------")

        channel.basic_consume(
            queue="notification-queue",
            on_message_callback=consume_message,
            auto_ack=False
        )

        channel.start_consuming()