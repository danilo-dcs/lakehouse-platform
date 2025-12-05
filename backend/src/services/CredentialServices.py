import json
from typing import List
import uuid6

from repositories.CouchbaseRepository import CouchbaseRepository
from shared.models.credentials import CreateCredentialsPayload, CouchbaseCredentialModel
from shared.models.storage import Storage, StorageBucketItem
from shared.handlers.CouchbaseQueryBuilder import CouchbaseQueryBuilder
from shared.handlers.FilesHandler import FilesHandler

from fastapi import HTTPException, status


class CredentialServices:
    def __init__(self, files_handler: FilesHandler = None) -> None:
        self.filesHandler = files_handler

        self.scope = "credentials"

        self.couchbaseRepo = CouchbaseRepository(
            scope=self.scope,
        )

    async def create_credentials(
        self, payload: CreateCredentialsPayload, collection_name: str = "cloud"
    ) -> CouchbaseCredentialModel:
        from shared.handlers.EncryptionHandler import EncryptionHandler
        from services.VisasServices import VisaServices

        encryptationHandler = EncryptionHandler()

        invalid_ids = list([])

        visaServices = VisaServices()

        if payload.visa_uuids:
            for visa_id in payload.visa_uuids:
                response = visaServices.get_by_id(visa_uuid=visa_id)

            if not response:
                invalid_ids.append(visa_id)
        else:
            payload.visa_uuids = []

        if invalid_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Provided visa ids are invalid: {invalid_ids}")

        credentials_id = str(uuid6.uuid7())

        encryptedCredential = encryptationHandler.encrypt_credentials(
            payload.credential.model_dump(exclude_none=True, exclude_unset=True)
        )

        couchbase_credential = CouchbaseCredentialModel(
            id=credentials_id,
            bucket_names=payload.bucket_names,
            storage_type=payload.storage_type,
            visa_uuids=payload.visa_uuids,
            credential=encryptedCredential,
        )

        await self.couchbaseRepo.create_document(
            collection_name=collection_name,
            key=credentials_id,
            value=couchbase_credential.model_dump(
                exclude_none=True, exclude_unset=True
            ),
        )

        return couchbase_credential

    async def create_credentials_from_json(
        self,
        credentials_file_path: str,
        storage_type: Storage,
        bucket_names: List[str],
        visa_uuids: List[str] = None,
    ) -> CouchbaseCredentialModel:
        from shared.handlers.EncryptionHandler import EncryptionHandler
        from services.VisasServices import VisaServices

        encryptationHandler = EncryptionHandler()

        if not self.filesHandler:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="CredentialService instance has no Files Handler object. Make sure to pass a FilesHandler's object on the CredentialServices constructor"
            )

        credential_data = json.loads(
            self.filesHandler.read(path=credentials_file_path, mode="r")
        )

        credentials_id = str(uuid6.uuid7())

        encryptedCredential = encryptationHandler.encrypt_credentials(credential_data)

        couchbase_credential = CouchbaseCredentialModel(
            id=credentials_id,
            storage_type=storage_type,
            visa_uuids=visa_uuids,
            credential=encryptedCredential,
            bucket_names=bucket_names,
        )

        invalid_ids = list([])

        if visa_uuids:
            visaServices = VisaServices()
            for visa_id in visa_uuids:
                response = visaServices.get_by_id(visa_uuid=visa_id)

            if not response:
                invalid_ids.append(visa_id)
        else:
            visa_uuids = []

        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Povided visa ids are invalid: {invalid_ids}"
            )

        await self.couchbaseRepo.create_document(
            collection_name="cloud",
            key=credentials_id,
            value=couchbase_credential.model_dump(
                exclude_none=True, exclude_unset=True
            ),
        )

        return couchbase_credential

    async def list_all_cloud(
        self, collection_name: str = "cloud"
    ) -> List[CouchbaseCredentialModel]:
        response = await self.couchbaseRepo.get_documents(collection_name)

        if not response:
            return []

        parsed_response = map(
            lambda x: CouchbaseCredentialModel(**x["cloud"]), response
        )

        return list(parsed_response)

    async def list_by_id(
        self, credential_id: str, collection_name="cloud"
    ) -> CouchbaseCredentialModel:
        response = await self.couchbaseRepo.get_document_by_id(
            collection_name=collection_name, document_key=credential_id
        )

        if not response:
            return {}

        parsed_response = map(
            lambda x: CouchbaseCredentialModel(**x["cloud"]), response
        )

        return list(parsed_response)[0]

    async def list_by_visa_id(
        self, visa_uuid: str, collection_name="cloud"
    ) -> List[CouchbaseCredentialModel]:
        queryBuilder = CouchbaseQueryBuilder(
            scope=self.scope, collection=collection_name
        )

        query = (
            queryBuilder.select()
            .where_any(target="id", in_filed="visa_uuids", op="=", value=visa_uuid)
            .build()
        )

        response = await self.couchbaseRepo.query(statement=query)

        if not response:
            return {}

        parsed_response = list(
            map(lambda x: CouchbaseCredentialModel(**x["cloud"]), response)
        )

        return parsed_response

    async def list_by_visa_ids(
        self, visa_uuids: list[str], collection_name="cloud"
    ) -> List[CouchbaseCredentialModel]:
        queryBuilder = CouchbaseQueryBuilder(
            scope=self.scope, collection=collection_name
        )

        query = (
            queryBuilder.select()
            .where_intersect(target="visa_uuids", in_values=visa_uuids)
            .build()
        )

        response = await self.couchbaseRepo.query(statement=query)

        if not response:
            return {}

        parsed_response = list(
            map(lambda x: CouchbaseCredentialModel(**x["cloud"]), response)
        )

        return parsed_response

    async def list_by_visa_ids_and_bucket(
        self, visa_uuids: list[str], bucket_name: str, collection_name="cloud"
    ) -> List[CouchbaseCredentialModel]:
        queryBuilder = CouchbaseQueryBuilder(
            scope=self.scope, collection=collection_name
        )

        query = (
            queryBuilder.select()
            .where_intersect(target="id", in_filed="visa_uuids", value=visa_uuids)
            .build()
        )

        response = await self.couchbaseRepo.query(statement=query)

        if not response:
            return {}

        parsed_response = list(
            map(lambda x: CouchbaseCredentialModel(**x["cloud"]), response)
        )

        filtered_response = [
            item for item in parsed_response if bucket_name in item.bucket_names
        ]

        return filtered_response

    async def list_by_visa_and_bucket(
        self,
        visa_uuid: str,
        bucket_name: str,
        storage_type: Storage,
        collection_name="cloud",
    ) -> List[CouchbaseCredentialModel]:
        queryBuilder = CouchbaseQueryBuilder(
            scope=self.scope, collection=collection_name
        )

        query = (
            queryBuilder.select()
            .where(field="storage_type", op="=", value=storage_type)
            .where_any(target="visa", in_filed="visa_uuids", op="=", value=visa_uuid)
            .where_any(
                target="bucket_name", in_filed="bucket_names", op="=", value=bucket_name
            )
            .build()
        )

        response = await self.couchbaseRepo.query(statement=query)

        if not response:
            return []

        parsed_response = list(
            map(lambda x: CouchbaseCredentialModel(**x["cloud"]), response)
        )

        return parsed_response

    async def list_storage_buckets(self) -> List[StorageBucketItem]:
        credential_items = await self.list_all_cloud(collection_name="cloud")

        response = list()

        if not credential_items:
            return response

        response = [
            StorageBucketItem(storage_type=item.storage_type, bucket_name=name)
            for item in credential_items
            for name in item.bucket_names
        ]

        return response

    async def delete_by_id(self, credential_uuid: str, collection_name="cloud") -> str:
        await self.couchbaseRepo.delete_document(
            collection_name=collection_name, document_key=credential_uuid
        )
        return credential_uuid

    async def revoke_credential_from_visa(
        self, credential_uuid: str, visa_uuid: str, collection_name="cloud"
    ) -> CouchbaseCredentialModel:
        old_credential = await self.list_by_id(credential_id=credential_uuid)

        if not old_credential:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"ivalid credential id: {credential_uuid}"
            )

        old_credential = CouchbaseCredentialModel(**old_credential)

        if not old_credential.visa_uuids or visa_uuid not in old_credential.visa_uuids:
            return visa_uuid

        uploaded_visa_ids = old_credential.visa_uuids

        uploaded_visa_ids.remove(visa_uuid)

        uploaded_credential = CouchbaseCredentialModel(
            id=old_credential.id,
            storage_type=old_credential.storage_type,
            visa_uuids=uploaded_visa_ids,
            bucket_names=old_credential.bucket_names,
            credential=old_credential.credential,
        )

        await self.couchbaseRepo.upsert_document(
            collection_name=collection_name,
            key=credential_uuid,
            value=uploaded_credential.model_dump(exclude_none=True, exclude_unset=True),
        )

        return uploaded_credential

    async def revoke_credential_from_visa_with_payload(
        self,
        credential_payload: CouchbaseCredentialModel,
        visa_uuid: str,
        collection_name="cloud",
    ) -> CouchbaseCredentialModel:
        if not credential_payload.visa_uuids:
            return visa_uuid

        uploaded_visa_ids = credential_payload.visa_uuids

        uploaded_visa_ids.remove(visa_uuid)

        uploaded_credential = CouchbaseCredentialModel(
            id=credential_payload.id,
            storage_type=credential_payload.storage_type,
            visa_uuids=uploaded_visa_ids,
            bucket_names=credential_payload.bucket_names,
            credential=credential_payload.credential,
        )

        await self.couchbaseRepo.upsert_document(
            collection_name=collection_name,
            key=credential_payload.id,
            value=uploaded_credential.model_dump(exclude_unset=True, exclude_none=True),
        )

        return uploaded_credential

    async def grant_credential_to_visa(
        self, credential_uuid: str, visa_uuid: str, collection_name="cloud"
    ) -> CouchbaseCredentialModel:
        # to prevent circular dependencies
        from services.VisasServices import VisaServices

        visaServices = VisaServices()

        passport_visa = await visaServices.get_by_id(visa_uuid=visa_uuid)

        if not passport_visa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid visa_uuid: {visa_uuid}"
            )

        old_credential = await self.list_by_id(credential_id=credential_uuid)

        if not old_credential:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid credential_uuid: {credential_uuid}"
            )

        new_credential = old_credential.model_copy(deep=True)

        if not new_credential.visa_uuids:
            new_credential.visa_uuids = []

        new_credential.visa_uuids.append(visa_uuid)

        await self.couchbaseRepo.upsert_document(
            collection_name=collection_name,
            key=credential_uuid,
            value=new_credential.model_dump(exclude_none=True, exclude_unset=True),
        )

        return new_credential
