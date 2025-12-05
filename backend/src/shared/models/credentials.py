from typing import List, Optional, Union
from pydantic import BaseModel

from shared.models.storage import Storage

class GoogleCredentialsModel(BaseModel):
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None 
    client_x509_cert_url: Optional[str] = None
    universe_domain: Optional[str] = None

class AmazonCredentialsModel(BaseModel):
    access_key: Optional[str] = None
    secret_access_key: Optional[str] = None
    region: Optional[str] = None

class HadoopCredentialsModel(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class CreateCredentialsPayload(BaseModel):
    visa_uuids: Optional[List[str]] = None
    bucket_names: List[str]
    storage_type: Storage
    credential: Union[GoogleCredentialsModel, AmazonCredentialsModel, HadoopCredentialsModel]

class DeleteCredentialResponse(BaseModel):
    deleted_credential_id: str

class EncryptedCredentialsPayload(BaseModel):
    visa_uuids: Optional[List[str]] = []
    storage_type: Optional[Storage] = None
    bucket_names: Optional[List[str]] = []
    # credential: Optional[Union[GoogleCredentialsModel,AmazonCredentialsModel]] = None
    credential: Optional[str]  = None

class CouchbaseCredentialModel(EncryptedCredentialsPayload):
    id: str