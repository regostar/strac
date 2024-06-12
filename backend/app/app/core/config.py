import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from enum import Enum
from msal import ConfidentialClientApplication
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()
print("TENANT_ID =  ", os.getenv("TENANT_ID"))

# OneDrive API configuration
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GRAPH_SCOPES = os.getenv("GRAPH_SCOPES")
DRIVE_ID = os.getenv("DRIVE_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_API_URL = "https://graph.microsoft.com/v1.0"

# MSAL application
graph_client = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

def get_access_token():
    token_response = graph_client.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise HTTPException(status_code=500, detail="Could not acquire access token")


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings, extra='ignore'):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    WHEATER_URL: str = "https://wttr.in"

    
    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("../../.env")





# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UserAuthConfigSnippet>
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
    SendMailPostRequestBody)
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
import json
from msgraph.generated.models.subscription import Subscription



class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphServiceClient

    def __init__(self, client_id, tenant_id, graph_scopes):
        # self.settings = config
        # client_id = self.settings['clientId']
        # tenant_id = self.settings['tenantId']
        # clientSecret = self.settings['clientSecret']
        # graph_scopes = self.settings['graphUserScopes'].split(' ')
        graph_scopes = graph_scopes.split(',')
        # self.device_code_credential = ClientSecretCredential(tenant_id, client_id, clientSecret)
        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)
# </UserAuthConfigSnippet>

    # <GetUserTokenSnippet>
    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token
    # </GetUserTokenSnippet>

    # <GetUserSnippet>
    async def get_user(self):
        """
        Used to display the user details
        """
        # Only request specific properties using $select
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )

        request_config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user
    # </GetUserSnippet>


    # <MakeGraphCallSnippet>
    async def list_files(self):
        """
        This function is used to list all files in the root of the one drive
        We can modify this to list all files in a specific location also
        """
        try:
            print("____________-")
            # List all children in root of the one drive
            items = await self.user_client.drives.by_drive_id(DRIVE_ID).items.by_drive_item_id('root').children.get()
            if items and items.value:
                for item in items.value:
                    print(item.id, item.name, item.size, item.folder, item.file)

            # Convert result3 to JSON
                result_json = json.dumps([{
                    'name': each.name,
                    'id': each.id,
                    'web_url': each.web_url
                } for each in items.value], indent=4)
            return result_json
        except Exception as e:
            print(f"Error: {e}")
            return None
    # </MakeGraphCallSnippet>


    async def download_files(self, item_id: str = None):
        """
        Documentation -
        Returns a 302 Found response redirecting to a preauthenticated download URL for the file, 
        which is the same URL available through the @microsoft.graph.downloadUrl property on the DriveItem.
        To download the contents of the file your application needs to follow the Location header in the response. 
        Many HTTP client libraries will automatically follow the 302 redirection and start downloading the file immediately.
        """
        try:
            result = await self.user_client.drives.by_drive_id(DRIVE_ID).items.by_drive_item_id(item_id).content.get()
            print(result)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
        

    
    async def list_permissions(self, item_id: str = None):
        """
        This function is used to list all permissions of the file specified
        """
        # result = await self.user_client.drives.by_drive_id(DRIVE_ID).items.by_drive_item_id(item_id).permissions.get()

        # # if result and result.value:
        # #     for item in result.value:
        # #         print(item.id, item.roles, item.grantedTo, item.link)
        # print(result)
        # result_json = json.dumps([{
        #         'roles': each.roles,
        #         'id': each.id,
        #         "granted_to": each.granted_to,
        #     } for each in result.value], indent=4)
        # return [{
        #         'roles': each.roles,
        #         'id': each.id,
        #         "granted_to": each.granted_to,
        #     } for each in result.value]
        # # return result_json
        try:
            # Fetch permissions of the specified item
            permissions = await self.user_client.drives.by_drive_id(DRIVE_ID).items.by_drive_item_id(item_id).permissions.get()
            
            # Extract role, id, and username from the permissions
            extracted_permissions = []
            
            return permissions.value

        except Exception as e:
            print(f"Error: {e}")
            return None
        
 
    async def create_subscription(self):
        """
        This function is used to register a webhook
        whenevr a file changes with permissions, this webhook is triggered
        This is a one time thing, needs to be deleted if it has to be recreated
        """
        try:
            request_body = Subscription(
                change_type="updated",
                notification_url="https://hooks.zapier.com/hooks/catch/19139951/2o9gf6p/",
                # this can be our app url or any public facing url
                # resource=f"/me/drive/items/{item_id}/permissions",
                # resource=f"/drive/items/{item_id}",
                resource=f"/drives/{DRIVE_ID}/root",
                expiration_date_time="2024-12-31T11:00:00.0000000Z",
                client_state="SecretClientState",
                # fields=['permissions']
            )
            subscription = await self.user_client.subscriptions.post(request_body)
            return subscription
        except Exception as e:
            print(f"Error: {e}")
            return None


graph: Graph = Graph(CLIENT_ID, TENANT_ID, GRAPH_SCOPES)

# await greet_user(graph)


settings = Settings()
