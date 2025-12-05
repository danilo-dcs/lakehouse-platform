import aiofiles
import os
import shutil
import typing
from typing import BinaryIO, List


from fastapi import UploadFile


class FilesHandler:

    def __init__(self, base_path: str = None) -> None:

        self.base_path = base_path

        if base_path is None:
            return

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)


    def check_dir(self, path) -> bool:
        """Check if a given dir exists."""
        return os.path.exists(path) and os.path.isdir(path)
    
    def check_file(self, path) -> bool:
        """Check if a given file exists."""
        return os.path.exists(path) and os.path.isfile(path)


    def delete_dir(self, repo_path: str) -> None:
        """Delete dir and its content"""
        if self.check_dir(repo_path):
            try:
                shutil.rmtree(repo_path)
            except Exception as e:
                print(f"Error: {e}")


    def get_base_path(self) -> str:
        """Return the object instance's base path"""
        return self.base_path


    def read(self, path: str, mode: str = "rb") -> str:
        """Read a generic file given a file path (with the file name)"""
        content = None
        with open(path, mode) as f:
            content = f.read()
        return content

       
    async def save(self, path: str, file: BinaryIO) -> None:
        """Save a generic file into a given file dir path"""
        with open(path, "wb") as buff:
            buff.write(file.read())

    async def save_uploaded_file(self, file: UploadFile) -> List[str]:
        """handle files uploaded to an endpoint"""

        save_path = os.path.join(self.base_path, file.filename)

        await self.save(save_path, file.file)

        return save_path
    
    async def save_stream_file(self, filename: str, stream: typing.AsyncGenerator[bytes, None]) -> List[str]:
        """Handle file streams being uploaded into an endpoint"""

        save_path = os.path.join(self.base_path, filename)

        async with aiofiles.open(save_path, "wb") as f:
            async for chunk in stream:
                await f.write(chunk)

        return save_path


    def set_base_path(self, path: str) -> None:
        """Set the object's base path to a given path"""
        self.base_path = path