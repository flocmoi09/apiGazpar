"""Support for Helper."""
from typing import Any
import socket
import aiohttp
import async_timeout
from pygazpar.exceptions import ClientAuthenticationError, ClientCommunicationError,ClientError

async def _api_wrapper(
    session:aiohttp.ClientSession,
    method: str,
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    params: dict | None = None,
) -> Any:
    """Get information from the API."""
    try:
        async with async_timeout.timeout(10):
            response = await session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
            )
            _verify_response_or_raise(response)
            return response

    except TimeoutError as exception:
        msg = f"Timeout error fetching information - {exception}"
        raise ClientCommunicationError(
            msg,
        ) from exception
    except (aiohttp.ClientError, socket.gaierror) as exception:
        msg = f"Error fetching information - {exception}"
        raise ClientCommunicationError(
            msg,
        ) from exception
    except Exception as exception:  # pylint: disable=broad-except
        msg = f"Something really wrong happened! - {exception}"
        raise ClientError(
            msg,
        ) from exception
def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise ClientAuthenticationError(
            msg,
        )
    response.raise_for_status()
