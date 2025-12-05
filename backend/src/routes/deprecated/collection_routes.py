from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from services.CollectionServices import CollectionServices
from shared.models.storage import Storage

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.post("/create", summary="Create a new collection dir")
async def create_collections(
    user_id: str = Form(...),
    storage_type: Storage = Form(...),
    collection_name: str = Form(...),
    namenode_address: str = Form(None),
    bucket_name: str = Form(None), 
    credential_name: str = Form(None)
):
    
    collection_services = CollectionServices()

    result = await collection_services.create_collection(
        user_id=user_id,
        storage_type=storage_type,
        collection_name=collection_name,
        namenode_address=namenode_address,
        bucket_name=bucket_name,
        credential_name=credential_name
    )
    
    return JSONResponse({"message": "Success!", "collection": result})


@router.post("/list", summary="List collection names")
async def list_collections(
    user_id: str = Form(...),
    storage_type: Storage = Form(...),
    namenode_address: str = Form(None),
    bucket_name: str = Form(None), 
    credential_name: str = Form(None)
):
    collection_services = CollectionServices()

    result = await collection_services.list_collections(
        user_id=user_id,
        storage_type=storage_type,
        namenode_address=namenode_address,
        bucket_name=bucket_name,
        credential_name=credential_name
    )

    return JSONResponse({"message": "Success!", "collections": result})
