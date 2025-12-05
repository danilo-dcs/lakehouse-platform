from pydantic import BaseModel


class EncryptionConfs(BaseModel):
    secret_key: str
