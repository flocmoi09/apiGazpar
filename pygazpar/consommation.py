"""Support for Consommation Methods."""
from __future__ import annotations
from typing import  Dict, Any
import aiohttp
from pygazpar.helpers import _api_wrapper
from pygazpar.types.ConsommationType import ConsommationType
from pygazpar.enum import ConsommationRole,Frequency
from .exceptions import ClientError

BASE_URL="https://monespace.grdf.fr/api/e-conso/pce/consommation/"
class  GazparConsommation:
     '''Get the consommation JSON or File from the API'''
     # ------------------------------------------------------
     def __init__(self, session: aiohttp.ClientSession):
        self._session = session
     # ------------------------------------------------------
     async def get_consommation(self,pce:str,date_debut:str,date_fin:str,type_conso:ConsommationRole) -> ConsommationType:
          '''Get the consommation from the API'''
          response=await _api_wrapper(
          session=self._session,
          method="get",
          url=BASE_URL+type_conso.value,
          headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
          params={"dateDebut":date_debut,"dateFin":date_fin,"pceList[0]":pce}
          )
          if response.content_type=="application/json":
               responsejson=await response.json()
          else: 
               raise ClientError("Invalid response from server")
          return ConsommationType(**responsejson[pce])
     # ------------------------------------------------------
     async def get_consommation_file(self,pce:str,date_debut:str,date_fin:str,type_conso:ConsommationRole,frequency:Frequency) -> Dict[str, Any]:
          '''Get the consommation file from the API'''
          response=await _api_wrapper(
          session=self._session,
          method="get",
          url=BASE_URL+type_conso.value+"/telecharger",
          headers={"Content-type": "application/json","X-Requested-With": "XMLHttpRequest"},
          params={"dateDebut":date_debut,"dateFin":date_fin,"pceList[0]":pce,"frequence":frequency.value}
          )
          if response.content_type=="text/html":
               raise ClientError("Invalid response from server")
          else:
               filename = response.headers["Content-Disposition"].split("filename=")[1]
               filecontent = await response.content()
               return {"filename":filename,"content":filecontent}
