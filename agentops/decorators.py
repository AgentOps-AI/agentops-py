from .client import Client
import inspect
import functools
from .log_config import logger


def record_function(event_name: str):
    """
    Decorator to record an event before and after a function call.
    Usage:
            - Actions: Records function parameters and return statements of the
                    function being decorated. Additionally, timing information about
                    the action is recorded
    Args:
            event_name (str): The name of the event to record.
    """

    def decorator(func):
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                client = Client()
                if (
                    client._session is None
                    or client._session.has_ended
                    or client._worker is None
                ):
                    logger.warning("Cannot record event - no current session")
                    return func(*args, **kwargs)
                return await client._record_event_async(
                    func, event_name, *args, **kwargs
                )

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                client = Client()
                if (
                    client._session is None
                    or client._session.has_ended
                    or client._worker is None
                ):
                    logger.warning("Cannot record event - no current session")
                    return func(*args, **kwargs)
                return client._record_event_sync(func, event_name, *args, **kwargs)

            return sync_wrapper

    return decorator
