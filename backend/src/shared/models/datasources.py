
from pydantic import BaseModel

class CouchbaseConfigs(BaseModel):
    host: str
    user: str
    password: str
    bucket: str = None

class DatasourceConfigs(BaseModel):
    couchbase: CouchbaseConfigs
