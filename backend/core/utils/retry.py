import logging
from typing import Optional

from tenacity import retry, retry_if_exception, stop_after_attempt, wait_random


def retrying_factory(
    max_attempts: int = 3,
    wait_min: int = 1,  # s
    wait_max: int = 2,  # s
    transient_exceptions: Optional[tuple] = None,
):
    """Factory for creating retrying decorators. Main point of this factory is
    to introduce some logging to the bare retrying.retry decorators.
    For more see docs of retrying library https://github.com/rholder/retrying.
    """

    def retry_if_transient(e: Exception) -> bool:
        if transient_exceptions is None:
            return False
        if isinstance(e, transient_exceptions):
            logging.warning("Retrying on transient exception: %s", e)
            return True
        return False

    decorator = retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_random(wait_min, wait_max),
        retry=retry_if_exception(retry_if_transient),
        reraise=True,
    )

    return decorator
