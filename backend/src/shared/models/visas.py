
from typing import List, Optional
from pydantic import BaseModel


class CreateVisaPayload(BaseModel):
	visaName: str 
	visaIssuer: str 
	visaDescription: str


class VisaModel(BaseModel):
	id: str 
	visaName: str 
	visaIssuer: str 
	visaDescription: str
	visaSecret: Optional[str] = None
	
	
class PassportVisaAssertion(BaseModel):
	passportVisa: VisaModel
	status: Optional[str] = None
	assertedAt: Optional[int] = None
	

class AssertedUser(BaseModel):
	id: str
	
class VisaAssertedUser(BaseModel):
	status: Optional[str] = None
	assertedAt: Optional[int] = None
	passportUser: Optional[AssertedUser]
	
class AssertedVisaModel(VisaModel):
	passportVisaAssertions: Optional[List[VisaAssertedUser]] = None
	

	