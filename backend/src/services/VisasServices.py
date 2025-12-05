from typing import List
import uuid6

import requests
from repositories.CouchbaseRepository import CouchbaseRepository
from shared.models.env import EnvSettings
from shared.models.visas import AssertedVisaModel, CreateVisaPayload, VisaModel


class VisaServices:
    def __init__(self) -> None:
        settings = EnvSettings()

        self.scope = "users"
        self.couchbaseRepo = CouchbaseRepository(
            scope=self.scope
        )

        self.passport_broker_url = settings.PASSPORT_BROKER_SERVICE_URL

    async def create_visa(self, payload: CreateVisaPayload) -> VisaModel:
        visa_id = str(uuid6.uuid7())

        passport_broker_url = (
            f"{self.passport_broker_url}/admin/ga4gh/passport/v1/visas"
        )

        body = VisaModel(
            id=visa_id,
            visaName=payload.visaName,
            visaIssuer=payload.visaIssuer,
            visaDescription=payload.visaDescription,
        )

        response = requests.post(url=passport_broker_url, json=body.model_dump())

        if not response or "error" in response:
            return {}

        return body

    async def delete_visa(self, visa_uuid: str) -> str:
        from services.CredentialServices import CredentialServices
        from services.UserServices import UserServices

        userServices = UserServices()

        # Removing visa from user's asserted visas document records

        response = await userServices.list_users_by_visa_id(visa_uuid=visa_uuid)

        if response:
            user_visas_map = response

            for user_visas in user_visas_map:
                await userServices.revoke_visas_from_user(
                    user_uuid=user_visas.user_uuid, visa_uuids=[visa_uuid]
                )

        # Removing visa from credentials document records

        credentialServices = CredentialServices()

        credentials_per_visa = await credentialServices.list_by_visa_id(
            visa_uuid=visa_uuid
        )

        if credentials_per_visa:
            for credential in credentials_per_visa:
                await credentialServices.revoke_credential_from_visa_with_payload(
                    credential_payload=credential, visa_uuid=visa_uuid
                )

        # Removing visa from passport broker

        passport_broker_url = f"{self.passport_broker_url}/admin/ga4gh/passport/v1/visas/{visa_uuid}"

        requests.delete(url=passport_broker_url)

        return visa_uuid

    async def list_all(self) -> List[VisaModel]:
        passport_broker_url = (
            f"{self.passport_broker_url}/admin/ga4gh/passport/v1/visas"
        )

        response = requests.get(url=passport_broker_url)

        if not response or "error" in response:
            return []

        passport_visas = response.json()

        return [VisaModel(**visa) for visa in passport_visas]

    async def get_by_id(self, visa_uuid: str) -> AssertedVisaModel:
        passport_broker_url = f"{self.passport_broker_url}/admin/ga4gh/passport/v1/visas/{visa_uuid}"

        response = requests.get(url=passport_broker_url)

        if not response or "error" in response:
            return {}

        response = response.json()

        return AssertedVisaModel(**response)

    async def update_visa(self, payload: AssertedVisaModel) -> VisaModel:
        from services.UserServices import UserServices

        userServices = UserServices()

        response = await userServices.list_users_by_visa_id(visa_uuid=payload.id)

        if response:
            for user in response:
                for visaAssertions in user.passportVisaAssertions:
                    if payload.id == visaAssertions.passportVisa.id:
                        visaAssertions.passportVisa.visaName = payload.visaName
                        visaAssertions.passportVisa.visaIssuer = payload.visaIssuer
                        visaAssertions.passportVisa.visaDescription = (
                            payload.visaDescription
                        )
                        visaAssertions.passportVisa.visaSecret = payload.visaSecret

        for user_assertion in response:
            await self.couchbaseRepo.upsert_document(
                collection_name="visa",
                key=user_assertion.id,
                value=user_assertion.model_dump(exclude_none=True, exclude_unset=True),
            )

        passport_broker_url = f"{self.passport_broker_url}/admin/ga4gh/passport/v1/visas/{payload.id}"

        body = payload.model_dump()

        response = requests.put(url=passport_broker_url, json=body)

        if not response or "error" in response:
            return {}

        response = response.json()

        response = VisaModel(**response)

        return response
