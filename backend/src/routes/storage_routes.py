from fastapi import (
    APIRouter,
    Depends,
    Request
)

from starlette.formparsers import MultiPartParser


from services.CollectionServices import CollectionServices
from services.CredentialServices import CredentialServices
from services.FileServices import FileServices
from shared.models.storage import CreateCollectionPayload, CreateCollectionResponse, DownloadFileRequestPayload, DownloadFileRequestResponse, GetStorageBucketListResponse, UploadFileRequestPayload, UploadFileRequestResponse
from routes.auth_routes import auth_oauth2_scheme


router = APIRouter(prefix="/storage", tags=["Storage"])

MultiPartParser.max_file_size = 1 * 1024 * 1024

@router.get("/bucket-list",
    summary="Get the list of storage buckets available in the system", 
    response_model=GetStorageBucketListResponse, 
    response_model_exclude_none=True, 
    response_model_exclude_unset=True
)
async def get_bucket_list(request: Request, _:str = Depends(auth_oauth2_scheme)) -> GetStorageBucketListResponse :
    credentialServices = CredentialServices()

    response = await credentialServices.list_storage_buckets()

    return GetStorageBucketListResponse(bucket_list=response)


@router.post(
    "/collections/create", 
    summary="Create a new collection dir", 
    response_model=CreateCollectionResponse, 
    response_model_exclude_none=True, 
    response_model_exclude_unset=True
)
async def create_collections(
    request: Request,
    payload: CreateCollectionPayload, 
    _: str = Depends(auth_oauth2_scheme)
) -> CreateCollectionResponse:
    
    user_id = request.state.user
    
    collection_services = CollectionServices()

    result = await collection_services.create_collection(payload=payload, user_id=user_id)
    
    return result


@router.post(
    "/files/download-request", 
    summary="Download request", 
    response_model=DownloadFileRequestResponse
)
async def download_file_request(
    request: Request,
    payload: DownloadFileRequestPayload,
    _: str = Depends(auth_oauth2_scheme)
) -> DownloadFileRequestResponse:
    user_id = request.state.user

    files_services = FileServices()

    result = await files_services.create_download_request_directly(payload, user_id=user_id) 

    return result


@router.post(
    "/files/upload-request",
    summary="Open a file upload call to the server",
    description="This endpoint will generate a signed url on the bucket for the user to transfer the file directly",
    response_model=UploadFileRequestResponse
)
async def upload_file_request_direct(
    request: Request,
    payload: UploadFileRequestPayload,
    _: str = Depends(auth_oauth2_scheme)
) -> UploadFileRequestResponse:
    
    user_id = request.state.user

    files_services = FileServices()
    
    result = await files_services.create_upload_file_request_directly(payload=payload, user_id=user_id)

    return result
