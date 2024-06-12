from typing import Annotated
from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import requests


from app.core.config import settings
from app.schemas.response_schema import IGetResponseBase, create_response
from app.core.config import graph

router = APIRouter()

api_reference: dict[str, str] = {"api_reference": "https://github.com/chubin/wttr.in"}




# @router.get("/list")
# async def list_files() -> JSONResponse:
#     """
#     Gets Weather by city using sync work
#     """
#     access_token = get_access_token()

#     # Construct request to Microsoft graph api using the access token generated
#     headers = {'Authorization': f'Bearer {access_token}'}
#     graph_url_list_files = f"{GRAPH_API_URL}/me/drive/root/children"
#     graph_api_response = requests.get(graph_url_list_files, headers=headers)

#     if graph_api_response.status_code == 200:
#         return graph_api_response.json()
#     else:
#         raise HTTPException(status_code=graph_api_response.status_code, detail=graph_api_response.json())


@router.get("/list")
async def list_files() -> JSONResponse:
    """
    Gets Weather by city using sync work
    """

    response = await graph.list_files()
    return response


@router.get("/get_permissions")
async def get_permissions_of_file(item_id: str = None) -> JSONResponse:
    """
    Gets Weather by city using sync work
    """

    response = await graph.list_permissions(item_id)
    return response


@router.get("/download")
async def get_download(item_id: str = None) -> JSONResponse:
    """
    Gets Weather by city using sync work
    """

    response = await graph.download_files(item_id)
    return response

