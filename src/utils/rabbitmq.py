import pika


class RabbitMQClient:
    def __init__(self, host="localhost"):
        self.host = host
        self.connection = None
        self.channel = None

    def _connect(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host)
            )
            self.channel = self.connection.channel()

    def publish_message(self, queue_name: str, message: str):
        self._connect()
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,  # default nameless exchange
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self):
        if self.connection is not None and not self.connection.is_closed:
            self.connection.close()
