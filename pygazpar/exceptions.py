"""Support for Exception custom."""
class ClientError(Exception):
    """Exception to indicate a general API error."""


class ClientCommunicationError(
    ClientError,
):
    """Exception to indicate a communication error."""


class ClientAuthenticationError(
    ClientError,
):
    """Exception to indicate an authentication error."""
