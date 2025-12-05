from typing import List, Literal, Optional
from pydantic import BaseModel

from shared.models.visas import PassportVisaAssertion


class CreateUserPayload(BaseModel):
    name: str
    password: str
    email: str
    active: Optional[bool] = True
    role: Optional[Literal["admin", "user"]] = "user"

class UserModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
    role: Optional[Literal["admin", "user"]] = "user"
    location: Optional[str] = None

class CouchbaseUserModel(UserModel):
    id: str

class PasswordChangeRequest(BaseModel):
    new_password: str
    token: str

class PasswordRecoveryRequest(BaseModel):
    user_email: str


class PasswordRecoveryModel(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    role: Optional[Literal["admin", "user"]] = "user"
    location: Optional[str] = None
    expires_at: Optional[int] = None

class CouchbaseUserModelNoPassword(CouchbaseUserModel):
    @classmethod
    def from_full_model(cls, full_model: CouchbaseUserModel):
        data = full_model.model_dump(exclude={"password"}, exclude_unset=True, exclude_none=True)
        return cls(**data)
    
    @classmethod
    def from_dict(cls, dict_model: dict):
        data = dict_model.copy()
        data.pop("password", None)  
        return cls(**data)


class PassportUserAssertionModel(BaseModel):
    id: Optional[str] = None
    passportVisaAssertions: Optional[List[PassportVisaAssertion]] = []

class CouchbaseUserAssertionModel(PassportUserAssertionModel):
    user_uuid: Optional[str] = None

class AssertUserVisasPayload(BaseModel):
    visas_uuids: List[str]