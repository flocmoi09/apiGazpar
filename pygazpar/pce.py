"""Support for PCE Methods."""
from __future__ import annotations
from typing import List
import aiohttp
from pygazpar.types.PceType import PceType
from .helpers import _api_wrapper
from .exceptions import ClientError
BASE_URL="https://monespace.grdf.fr/api/e-conso/pce"
class  GazparPCE:
    """ Class PCE data from the API."""
     # ------------------------------------------------------
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
    async def get_list_pce(self) -> List[PceType]:
          """ Get all PCE from an account."""
          response=await _api_wrapper(
          session=self._session,
          method="get",
          url=BASE_URL,
          headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
          )
          results_pce=[]
          if response.content_type=="application/json":
               responsejson=await response.json()
          else:
               raise ClientError("Invalid response from server")
          for item in responsejson:
               results_pce.append(PceType(**item))
          return results_pce
    async def get_pce_details(self,pce:str) -> PceType:
        """ Get PCE details."""
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+"/"+pce+"/details",
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        )
        if response.content_type=="application/json":
             responsejson=await response.json()
        else:
             raise ClientError("Invalid response from server")
        return PceType(**responsejson)
    async def get_pce_meteo(self,pce:str,date_fin:str,nb_jours:int) -> any:
        """ Get PCE meteo temp data."""
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+"/"+pce+"/meteo",
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        params={"dateFinPeriode":date_fin,"nbJours":nb_jours}
        )
        if response.content_type=="application/json":
             return await response.json()
        else:
             raise ClientError("Invalid response from server")
