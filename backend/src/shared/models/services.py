from pydantic import BaseModel

class PassportBrokerConfs(BaseModel):
    host: str
    port: int
    url: str

class ServiceConfs(BaseModel):
    passport_broker: PassportBrokerConfs

