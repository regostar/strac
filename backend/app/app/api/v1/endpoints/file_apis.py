from typing import Annotated
from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import requests
from fastapi.responses import PlainTextResponse


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
    Gets files list in one drive
    """

    response = await graph.list_files()
    return response


@router.get("/get_permissions")
async def get_permissions_of_file(item_id: str = None) -> JSONResponse:
    """
    Gets permission of a file
    """

    response = await graph.list_permissions(item_id)
    return response


@router.get("/download")
async def get_download(item_id: str = None) -> JSONResponse:
    """download a file"""

    response = await graph.download_files(item_id)
    return response


@router.get("/subscribe_permission_changes")
async def get_subscribe() -> JSONResponse:
    """
    subscribe to permission changes
    """
    print("came to subscribe")
    response = await graph.create_subscription()
    return response


@router.get("/unsubscribe")
async def unsubscribe(subscription_id: str) -> JSONResponse:
    """
    Un subscribe to permission changes
    """
    print("came to unsubscribe")
    response = await graph.delete_subscription(subscription_id)
    return response



# Handle notifications
@router.post("/notifications")
async def notifications(request: Request, validationToken: str= None):
    # data = await request.json()
    # print(data)
    # # return data, 202
    print("triggered")
    # print("!", request.url.query.params.get("validationToken"))

    # validation_token = request.query_params.get('validationToken')
    print(" validation_token = ", validationToken)
    if validationToken:
        return PlainTextResponse(validationToken)
    data = await request.json()
    print(data)
    return data


@router.get("/notifications")
async def notifications2(validationToken: str):
    # data = await request.json()
    # print(data)
    # # return data, 202
    print("triggered")
    # print("!", request.url.query.params.get("validationToken"))

    # validation_token = request.query_params.get('validationToken')
    print(" validation_token = ", validationToken)
    if validationToken:
        return PlainTextResponse(validationToken)
    return PlainTextResponse("", status_code=400)

    # for value in data.get('value', []):


# # Validate subscription
# @router.get('/notifications')
# async def validate_subscription(request: Request):
#     print("Received check webhook")

#     validation_token = request.query_params.get('validationToken')
#     print(" validation_token = ", validation_token)
#     if validation_token:
#         return PlainTextResponse(validation_token)
#     return PlainTextResponse('', status_code=400)
