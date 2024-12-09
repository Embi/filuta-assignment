import json
import logging
import os
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exceptions import AMQPChannelError, AMQPConnectionError

__RMQ_CONNECTION: BlockingConnection = None
__RMQ_CHANNEL: BlockingChannel = None
__RMQ_CREDS = pika.PlainCredentials(
    username=os.environ.get("RMQ_USER"), password=os.environ.get("RMQ_PASS")
)
__RMQ_CONNECTION_PARAMS = pika.ConnectionParameters(
    host=os.environ.get("RMQ_HOST"),
    port=os.environ.get("RMQ_PORT"),
    virtual_host=os.environ.get("RMQ_VHOST"),
    credentials=__RMQ_CREDS,
    heartbeat=1800,
    blocked_connection_timeout=60,
)
__RMQ_EXCEPTIONS_TO_RETRY = (AMQPConnectionError, AMQPChannelError)

__EXCHANGE = "/recommender"


def get_channel() -> BlockingChannel:
    global __RMQ_CONNECTION, __RMQ_CHANNEL
    if __RMQ_CONNECTION is None or __RMQ_CONNECTION.is_closed:
        __RMQ_CONNECTION = pika.BlockingConnection(__RMQ_CONNECTION_PARAMS)
    if __RMQ_CHANNEL is None or __RMQ_CHANNEL.is_closed:
        __RMQ_CHANNEL = __RMQ_CONNECTION.channel()
    return __RMQ_CHANNEL


def rmq_connection_retry(func: Callable) -> Callable:
    """Simple decorator that retries on common errors."""

    def wrapper(*args, **kwargs):
        retry_count = 3
        global __RMQ_CONNECTION, __RMQ_CHANNEL
        while retry_count:
            try:
                return func(*args, **kwargs)
            except __RMQ_EXCEPTIONS_TO_RETRY as e:
                __RMQ_CONNECTION = None
                __RMQ_CHANNEL = None
                retry_count -= 1
                if retry_count == 0:
                    raise
                logging.warning("Retrying RMQ connection", exc_info=e)

    return wrapper


@rmq_connection_retry
def get_message(queue: str):
    channel = get_channel()
    frame, prop, body = channel.basic_get(queue)
    if frame is not None:
        logging.debug(
            "Consumed message with tag %s from %s queue", frame.delivery_tag, queue
        )
    return frame, prop, body


@rmq_connection_retry
def ack_message(delivery_tag: str):
    channel = get_channel()
    channel.basic_ack(delivery_tag)
    logging.debug("Acknowledged message with tag %s", delivery_tag)


@rmq_connection_retry
def publish_message(msg: dict, routing_key: str):
    channel = get_channel()
    channel.basic_publish(__EXCHANGE, routing_key, json.dumps(msg))
    logging.debug(
        "Published message %s to %s exchange with routing key %s",
        msg,
        __EXCHANGE,
        routing_key,
    )
