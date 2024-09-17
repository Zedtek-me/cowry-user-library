from kombu import Exchange, Consumer, Queue, Connection
from django.conf import settings
from typing import Type, List, Optional
import logging
import json
import socket
from apps.users_api.models import AdminBooksRepresentation

logger = logging.getLogger("root")

class LibraryConsumer:
    '''consumer class that takes data from the remote service'''
    def __init__(self):
        self.connection = Connection(settings.BROKER_URL)
        logger.debug(f"connecting to broker on ...{settings.BROKER_URL}")
        try:
            self.connection.connect()
            logger.debug("connection successfully made to broker")
        except Exception as e:
            logger.exception(f"error connecting to broker... error: {e}")
        self.channel = self.connection and self.connection.channel()
    
    def get_exchange(self, use_default:bool=True, name=None, _type=None)->Type[Exchange]:
        '''creates and returns an exchange'''
        exchange_name = "library_default_exchange"
        exchange_type = "direct"
        if not use_default:
            exchange_name = name
            exchange_type = _type
        exchange = Exchange(name=exchange_name, type=exchange_type, channel=self.channel, durable=True)
        # explicitly declare the exchange in rabbitmq again
        exchange.declare(channel=self.channel)
        return exchange

    def get_queue(self, routing_key="library.user.api")->Type[Queue]:
        '''creates a default queue for the only remote process that needs to consume message from this producing process'''
        exchange = self.get_exchange(use_default=True)
        queue = Queue(name=routing_key, exchange=exchange, routing_key=routing_key, channel=self.channel, durable=True)
        queue.declare(channel=self.channel)
        return queue

    def get_consumer(self):
        '''creates and returns the consumer for this queue'''
        queue = self.get_queue()
        consumer = Consumer(queues=queue, channel=self.channel, no_ack=False, callbacks=[self.callback], accept=["application/json", "text/plain"])
        consumer.declare()
        return consumer
    
    def callback(self, body, message):
        logger.debug(f"message body: {body}\n message object: {message}")
        if isinstance(body, str):
            body = json.loads(body)
        data = {
            "title":body.get("book_title"),
            "author":body.get("book_author"),
            "description":body.get("description", "default description"),
            "category":body.get("category", "DEFAULT"),
            "status":body.get("status", "AVAILABLE")
        }
        admin_books_representation = AdminBooksRepresentation(**data)
        admin_books_representation.meta["remote_book_id"] = body.get("remote_book_id")
        admin_books_representation.save()
        logger.debug(f"admin book repre obj: {admin_books_representation.__dict__}")
        message.ack()
    
    def consume_from_queue(self):
        logger.debug(f"started consuming from queue....")
        consumer = self.get_consumer()
        self.connection.ensure_connection(max_retries=10)
        with consumer:
            while True:
                try:
                    self.connection.drain_events()
                except socket.timeout:
                    self.connection.drain_events()
