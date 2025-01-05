"""Support for Consommation Methods."""
from __future__ import annotations
import logging
import aiohttp
from .helpers import _api_wrapper
from pygazpar.types.consommation_type import Consommation_type
from pygazpar.enum import ConsommationRole,Frequency
from .exceptions import ClientError

BASE_URL="https://monespace.grdf.fr/api/e-conso/pce/consommation/"

class  GazparConsommation:
# ------------------------------------------------------
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
    
    async def get_consommation(self,pce:str,dateDebut:str,dateFin:str,type:ConsommationRole) -> Consommation_type:
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+type.value,
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        params={"dateDebut":dateDebut,"dateFin":dateFin,"pceList[0]":pce}
        )
        if(response.content_type=="application/json"):
             responseJSON=await response.json()
        else:  
             raise ClientError("Invalid response from server")
        return Consommation_type(**responseJSON[pce])

    async def get_consommation_file(self,pce:str,dateDebut:str,dateFin:str,type:ConsommationRole,frequency:Frequency) -> Consommation_type:
         # We remove an eventual existing data file (from a previous run that has not deleted it).
        
        response=await _api_wrapper(
        session=self._session,
        method="get",
        url=BASE_URL+type.value+"/telecharger",
        headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
        params={"dateDebut":dateDebut,"dateFin":dateFin,"pceList[0]":pce,"frequence":frequency.value}
        )
        
        if(response.content_type=="text/html"):
             raise ClientError("Invalid response from server")
        else:  
            filename = response.headers["Content-Disposition"].split("filename=")[1]
            fileContent = await response.content()
            return {"filename":filename,"content":fileContent}
       