import json
import logging
from typing import Callable
from core.utils.conf import CoreSettings

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exceptions import AMQPChannelError, AMQPConnectionError


class RMQClient:
    """Singleton implementation of a simple synchronous RabbitMQ Client."""

    __instance = {}
    __RMQ_EXCEPTIONS_TO_RETRY = (AMQPConnectionError, AMQPChannelError)

    def __init__(self):
        core_settins = CoreSettings()
        creds = pika.PlainCredentials(
            username=core_settins.rmq_user,
            password=core_settins.rmq_pass,
        )
        self.__connection_params = pika.ConnectionParameters(
            host=core_settins.rmq_host,
            port=core_settins.rmq_port,
            virtual_host=core_settins.rmq_vhost,
            credentials=creds,
            heartbeat=1800,
            blocked_connection_timeout=60,
        )
        self.__channel = None
        self.__connection = None

    def __new__(cls, *args, **kwargs):
        """Only instantiate once."""
        if "instance" not in cls.__instance:
            logging.debug("Instantiating RMQClient.")
            cls.__instance["instance"] = super().__new__(cls, *args, **kwargs)
        return cls.__instance["instance"]

    def __get_connection(self) -> BlockingConnection:
        if self.__connection is None or self.__connection.is_closed:
            self.__connection = pika.BlockingConnection(self.__connection_params)
        return self.__connection

    def __get_channel(self) -> BlockingChannel:
        if self.__channel is None or self.__channel.is_closed:
            self.__channel = self.__get_connection().channel()
        return self.__channel

    def __refresh_connection(self) -> None:
        """Try to close existing connection and channel, forcing new ones to
        get open.
        """
        logging.debug("Refreshing rmq connection.")
        try:
            logging.debug("Attempting to close existing channel.")
            self.__channel.close()
        except pika.exceptions.ChannelWrongStateError:
            logging.debug("Channel already closed")
        try:
            logging.debug("Attempting to close existing connection.")
            self.__connection.close()
        except pika.exceptions.ConnectionWrongStateError:
            logging.debug("Connection already closed")

    def __rmq_connection_retry(func: Callable) -> Callable:
        """Simple decorator that retries on errors defined in
        __RMQ_EXCEPTIONS_TO_RETRY class variable.
        """

        def wrapper(self, *args, **kwargs):
            retry_count = 3
            while retry_count:
                try:
                    return func(self, *args, **kwargs)
                except self.__RMQ_EXCEPTIONS_TO_RETRY as e:
                    self.__refresh_connection()
                    retry_count -= 1
                    if retry_count == 0:
                        raise
                    logging.warning("Retrying RMQ connection", exc_info=e)

        return wrapper

    @__rmq_connection_retry
    def get_message(self, queue: str):
        channel = self.__get_channel()
        frame, prop, body = channel.basic_get(queue)
        if frame is not None:
            logging.debug(
                "Consumed message with tag %s from %s queue", frame.delivery_tag, queue
            )
        return frame, prop, body

    @__rmq_connection_retry
    def ack_message(self, delivery_tag: str):
        channel = self.__get_channel()
        channel.basic_ack(delivery_tag)
        logging.debug("Acknowledged message with tag %s", delivery_tag)

    @__rmq_connection_retry
    def publish_message(self, msg: dict, exchange: str, routing_key: str):
        channel = self.__get_channel()
        channel.basic_publish(exchange, routing_key, json.dumps(msg))
        logging.debug(
            "Published message %s to %s exchange with routing key %s",
            msg,
            exchange,
            routing_key,
        )
