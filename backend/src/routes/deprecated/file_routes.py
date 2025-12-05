import os
import traceback


from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
    Header,
)
from fastapi.responses import FileResponse, JSONResponse
from starlette.formparsers import MultiPartParser


from services.FileServices import FileServices
from shared.models.storage import Storage
from shared.handlers.FilesHandler import FilesHandler
from shared.handlers.TimeHandler import TimeHandler

router = APIRouter(prefix="/files", tags=["Files"])

MultiPartParser.max_file_size = 1 * 1024 * 1024


@router.post("/download-request", summary="Download request")
async def download_file_request(
    user_id: str = Form(...),
    file_name: str = Form(...),
    collection_name: str = Form(...),
    storage_type:  Storage = Form(...), 
    namenode_address: str = Form(None),
    bucket_name: str = Form(None),
    credential_name: str = Form(...),
    raw: bool = Form(True),
    processed: bool = Form(False),
    curated: bool = Form(False) 
):
    files_services = FileServices()

    result = await files_services.create_download_request(
        user_id=user_id,
        file_name=file_name,
        collection_name=collection_name,
        storage_type=storage_type, 
        namenode_address=namenode_address,
        bucket_name=bucket_name,
        credential_name=credential_name,
        raw=raw,
        processed=processed,
        curated=curated
    )

    return JSONResponse({"message": "File transfer allowed!", "payload": result})


@router.post("/download", summary="Download request") #TODO convert this function into a get request
async def download(
    file_name: str = Form(...),
    download_token: str = Form(...)
):
    try:

        timeHandler = TimeHandler()

        _, timestamp = download_token.split(":")

        if timeHandler.is_expired(timestamp):
            return HTTPException(status_code=400, detail="Expired Token")

        download_path = os.path.join("/", "tmp", "api", "downloads", download_token)

        fileHandler = FilesHandler()

        if not fileHandler.check_dir(download_path):
            return HTTPException(status_code=400, detail="Invalid or unexisting download token")

        local_file_path = os.path.join(download_path, file_name)

    except Exception as e:
        error_message = f"Error saving file: {str(e)}"
        stack_trace = traceback.format_exc()
        print("An error occurred:")
        print(stack_trace) 
        return HTTPException(status_code=500, detail=error_message)  

    return FileResponse(
        path=local_file_path,
        status_code=200,
        file_name=file_name,
        media_type="application/octet-stream",
    )


@router.post("/list", summary="List files from a given collection")
async def list_files(
    user_id: str = Form(...),
    collection_name: str = Form(...),
    storage_type: Storage = Form(...),
    namenode_address: str = Form(None),
    bucket_name: str = Form(None),
    credential_name: str = Form(None),
    raw: bool = Form(True),
    processed: bool = Form(False),
    curated: bool = Form(False)
):
    try: 
        files_services = FileServices()

        result = await files_services.list_files(
            user_id=user_id,
            collection_name=collection_name,
            storage_type=storage_type,
            namenode_address=namenode_address,
            bucket_name=bucket_name,
            credential_name=credential_name,
            raw=raw,
            processed=processed,
            curated=curated
        )

    except Exception as e:
        error_message = f"Error saving file: {str(e)}"
        stack_trace = traceback.format_exc()
        print("An error occurred:")
        print(stack_trace) 
        return HTTPException(status_code=500, detail=error_message)  

    return JSONResponse({"message": "Success!", "files": result})


@router.post("/metadata", summary="Get files metadata")
async def get_files_metadata(
    user_id: str = Form(...),
    collection_name: str = Form(...),
    file_names: list[str] = Form(...),
    storage_type: Storage = Form(...),
    namenode_address: str = Form(None),
    bucket_name: str = Form(None),
    credential_name: str = Form(None),
    raw: bool = Form(True),
    processed: bool = Form(False),
    curated: bool = Form(False)
):
    try: 
        files_services = FileServices()

        result = await files_services.get_files_metadata(
            user_id=user_id,
            collection_name=collection_name,
            file_names=file_names,
            storage_type=storage_type,
            namenode_address=namenode_address,
            bucket_name=bucket_name,
            credential_name=credential_name,
            raw=raw,
            processed=processed,
            curated=curated
        )

    except Exception as e:
        error_message = f"Error saving file: {str(e)}"
        stack_trace = traceback.format_exc()
        print("An error occurred:")
        print(stack_trace) 
        return HTTPException(status_code=500, detail=error_message)  

    return JSONResponse({"message": "Success!", "metadata": result})


@router.post(
    "/upload-request",
    summary="Open a file upload call to the server",
    description="This endpoint will generate a file transfer area and an upload token to be used to upload the actual file"
)
async def upload_file_request(
    user_id: str = Form(...),
    file_name: str = Form(...), 
    collection: str = Form(...), 
    storage_type:  Storage = Form(...),  
    bucket: str = Form(None),
    namenode_address: str = Form(None),
    credential_name: str = Form(None)
):
    files_services = FileServices()
    
    result = await files_services.create_upload_file_request( 
        user_id=user_id,
        file_name=file_name,
        collection=collection,
        storage_type=storage_type,  
        bucket=bucket,
        namenode_address=namenode_address,
        credential_name=credential_name
    )

    return JSONResponse({"message": "File transfer allowed!", "payload": result})


@router.post(
    "/upload",
    summary="Upload files",
    description="""
    To upload large files you'll have to stream the file to this endpoint.

    If you are using python:

    ______
    import requests

    # Define the URL of the endpoint
    url = "http://your-server-url/upload_large_gcs"

    # Define the headers you need to send
    headers = {
        "upload_token": "c3188f162d7e658f89f2ea367ef768ad:1724079970.496256",
        "output_filename": "results.csv",
        "Content-Type": "application/octet-stream"
    }

    # Define a generator to read the file in chunks
    def file_chunk_generator(file_path, chunk_size=1*1024*1024):
        with open(file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                yield chunk

    # Stream the file to the server
    file_path = "path_to_your_file.zip"
    response = requests.post(url, headers=headers, data=file_chunk_generator(file_path))
    ______

    If you are using node:

    ______
    const fs = require('fs');
    const axios = require('axios');
    const path = require('path');

    const CHUNK_SIZE = 1 * 1024 * 1024; // 1MB chunk size
    const filePath = path.resolve(__dirname, 'path_to_your_file.zip'); // Path to your file
    const url = 'http://your-server-url/upload_large_gcs';

    async function streamFileInChunks(filePath, url) {
    const fileStream = fs.createReadStream(filePath, { highWaterMark: CHUNK_SIZE });
    
    const headers = {
        "upload_token": "c3188f162d7e658f89f2ea367ef768ad:1724079970.496256",
        "output_filename": "results.csv",
        "Content-Type": "application/octet-stream"
    };

    try {
        const response = await axios.post(url, fileStream, { headers });
        console.log('Upload successful:', response.status);
    } catch (error) {
        console.error('Upload failed:', error.message);
    }
    }

    streamFileInChunks(filePath, url);
    ______
    """,
)
async def upload(
    request: Request,
    file_name: str = Header(..., convert_underscores=True),
    upload_token: str = Header(..., convert_underscores=True)
):
    try:

        timeHandler = TimeHandler()

        _, timestamp = upload_token.split(":")

        if timeHandler.is_expired(timestamp):
            return HTTPException(status_code=400, detail="Expired Token")

        upload_path = os.path.join("/", "tmp", "api", "uploads", upload_token)

        fileHandler = FilesHandler()

        if not fileHandler.check_dir(upload_path):
            return HTTPException(status_code=400, detail="Invalid or unexisting upload token")

        fileHandler.set_base_path(upload_path)

        await fileHandler.save_stream_file(filename=file_name, stream=request.stream())

        if not fileHandler.check_file(os.path.join(upload_path, file_name)):
            return HTTPException(status_code=400, detail="Unable to save the file correctly")
        
        files_services = FileServices()
        
        response = await files_services.upload_files(tmp_dir=upload_path)

        fileHandler.delete_dir(upload_path) # removing temporary directory

    except Exception as e:
        error_message = f"Error saving file: {str(e)}"
        stack_trace = traceback.format_exc()
        print("An error occurred:")
        print(stack_trace) 
        return HTTPException(status_code=500, detail=error_message)  

    return JSONResponse({"message": "Files Uploaded!", "file": response})

