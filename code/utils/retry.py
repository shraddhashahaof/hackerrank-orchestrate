import time
from utils.logger import logger


def with_retry(fn, retries: int = 3, delay: float = 2.0):
    """
    Retry a callable up to `retries` times with `delay` seconds between attempts.
    Raises RuntimeError if all attempts fail.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            last_error = e
            logger.warning(
                f"Attempt {attempt}/{retries} failed: {e}"
            )
            if attempt < retries:
                time.sleep(delay)

    raise RuntimeError(
        f"All {retries} attempts failed. Last error: {last_error}"
    )