"""Support for PCE Methods."""
from __future__ import annotations
from typing import List
import aiohttp
from pygazpar.types.PceType import PceType
from .helpers import _api_wrapper
from .exceptions import ClientError
BASE_URL="https://monespace.grdf.fr/api/e-conso/pce"
class  GazparPCE:
     # ------------------------------------------------------
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
    async def get_list_pce(self) -> List[PceType]:
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL,
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        )
        resultsPCE=[]
        if(response.content_type=="application/json"):
             responseJSON=await response.json()
        else:  
             raise ClientError("Invalid response from server")
        for item in responseJSON:
            resultsPCE.append(PceType(**item)) 
        return resultsPCE
    async def get_pce_details(self,pce:str) -> PceType:
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+"/"+pce+"/details",
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        )
        if(response.content_type=="application/json"):
             responseJSON=await response.json()
        else:  
             raise ClientError("Invalid response from server")
        return PceType(**responseJSON)
    async def get_pce_meteo(self,pce:str,dateFin:str,nbJours:int) -> any:
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+"/"+pce+"/meteo",
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        params={"dateFinPeriode":dateFin,"nbJours":nbJours}
        )
        if(response.content_type=="application/json"):
             return await response.json()
        else:  
             raise ClientError("Invalid response from server")
