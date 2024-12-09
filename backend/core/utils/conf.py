import logging
from pydantic_settings import BaseSettings


class SingletonSettingsMixin:
    """Singletone per class name - i.e., only one instance per configuration
    group (ApiSettings, CoreSettings...) is allowed.
    """

    __instances = {}

    def __new__(cls, *args, **kwargs):
        if cls.__name__ not in cls.__instances:
            logging.debug(f"Instantiating {cls.__name__}.")
            cls.__instances[cls.__name__] = super().__new__(cls, *args, **kwargs)
        return cls.__instances[cls.__name__]


class CoreSettings(SingletonSettingsMixin, BaseSettings):
    # Code version
    version: str
    # Logging settings
    log_level: str = "INFO"

    # Rabbitmq configuration
    rmq_user: str
    rmq_pass: str
    rmq_host: str
    rmq_port: str
    rmq_vhost: str

    # Postgresql configuration
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
