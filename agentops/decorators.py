import agentops
from .client import Client
import inspect
import functools
from typing import Optional


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
            async def async_wrapper(*args, session_id: Optional[str] = None, **kwargs):
                return await Client()._record_event_async(
                    func, event_name, *args, session_id=session_id, **kwargs
                )

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, session_id: Optional[str] = None, **kwargs):
                print(session_id)
                return Client()._record_event_sync(
                    func, event_name, *args, session_id=session_id, **kwargs
                )

            return sync_wrapper

    return decorator


def track_route(function):
    @functools.wraps(function)
    def wrapped_route(*args, **kwargs):
        client = agentops.create_client()
        return function(ao_client=client, *args, **kwargs)

    return wrapped_route
