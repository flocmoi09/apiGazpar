"""Support for GRDF authentication."""
from __future__ import annotations
import logging
import aiohttp
from yarl import URL
from .helpers import _api_wrapper
from .exceptions import ClientError

SESSION_TOKEN_URL = "https://connexion.grdf.fr/api/v1/authn"
AUTH_TOKEN_URL = "https://connexion.grdf.fr/login/sessionCookieRedirect"
LOG = logging.getLogger(__name__)

class GazparAuth:
    '''Manage the Auth API connection'''
    # ------------------------------------------------------
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession, token: str = None):

        self.__username = username
        self.__password = password
        self._session = session
        self._token = token
    # ------------------------------------------------------
    async def request_token(self) -> str:
        '''Request the token to the API'''
        response= await _api_wrapper(
        session=self._session,
        method="post",
        url=SESSION_TOKEN_URL,
        headers={"Content-type": "application/json", "domain":"grdf.fr","X-Requested-With": "XMLHttpRequest"},
        data={"username": self.__username,"password": self.__password,"options":
              {"multiOptionalFactorEnroll": "false","warnBeforePasswordExpired": "false"}},
        )
        if response.content_type=="application/json":
            responsejson=await response.json()
            session_token = responsejson.get("sessionToken")
        else:
            raise ClientError("Invalid response from server")
        LOG.debug("Session token: %s", session_token)
        response=await _api_wrapper(
            session=self._session,
            method="get",
            url=AUTH_TOKEN_URL,
            headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
            params={"checkAccountSetupComplete": "true","token": session_token,"redirectUrl": "https://monespace.grdf.fr"},

        )
        auth_token = self._session.cookie_jar.filter_cookies(URL("https://monespace.grdf.fr")).get("auth_token")
        self._token = auth_token.value
        return auth_token.value  # type: ignore
