
# import yaml
# import requests
# import uuid6

# from couchbase.cluster import Cluster, ClusterOptions
# from couchbase.auth import PasswordAuthenticator
# from couchbase.management.collections import CollectionManager, ScopeManager
# import couchbase.subdocument as SD

# from shared.models.datasources import CouchbaseConfigs

# class CouchbaseRepositorySDK:

#     def __init__(self, host:str = None, port:str = None, user:str = None, password:str = None):

#         if host and port and user and password:
#             self.host = host
#             self.port = port
#             self.user = user
#             self.password = password
        
#         else:
#             with open('conf/datasouces.yml') as conf:
#                 yml_data = yaml.safe_load(conf)
#             conf = CouchbaseConfigs(**yml_data)

#             self.host = conf.host
#             self.port = conf.port
#             self.user = conf.user
#             self.password = conf.password

#         self.cluster = Cluster('couchbase://localhost', ClusterOptions(
#             PasswordAuthenticator('admin', 'admin1234')
#         ))

    
#     # creation
#     async def create_bucket(self, bucket_name: str, ram_quota: str = '512') -> str: 

#         url = f'http://{self.host}:{self.port}/pools/default/buckets'

#         auth = (self.user, self.password)

#         data = {
#             'name': bucket_name,
#             'ramQuotaMB': ram_quota
#         }

#         response = await requests.post(url=url, auth=auth, data=data)

#         if response.status_code != 200:
#             raise Exception("Error in creating collection")

#         return bucket_name
    


#     async def create_document(self, bucket_name:str, collection_name: str, data: dict) -> dict:

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         collection = bucket.collection(collection_name)  

#         _id = f"{collection}::{uuid6.uuid7()}"

#         await collection.insert(_id, data)
            
#         return {
#             "id": _id,
#             **data
#         }
    


#     async def create_scope(self, bucket_name:str, scope_name: str) -> str:

#         url = f"http://{self.host}:{self.port}/pools/default/buckets/{bucket_name}/scopes"

#         auth = (self.user, self.password)

#         data = {
#             'name': scope_name
#         }

#         response = await requests.post(url, auth=auth, data=data)

#         if response.status_code != 200:
#             raise Exception("Error in creating scope")

#         return scope_name


#     # deletion
#     async def delete_document(self, bucket_name:str, collection_name: str, document_id: str) -> str:

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         collection = bucket.collection(collection_name)  

#         await collection.remove(document_id)

#         return document_id


#     # edit
#     async def edit_document(self, bucket_name:str, collection_name: str, document_id: str, data: dict):

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         collection = bucket.collection(collection_name)  

#         original_document = self.get_document(collection_name, document_id)

#         new_records = [ key for key in data if key not in original_document ]
#         removerd_records = [ key for key in original_document if key not in data ]
#         edited_records = [ key for key in data if key in original_document and original_document[key] != data[key]]

#         operations = [
#                 SD.upsert(key, data[key]) for key in new_records
#             ] + [
#                 SD.remove(key) for key in removerd_records
#             ] + [
#                 SD.replace(key, data[key]) for key in edited_records
#             ]

#         await collection.mutate_in(document_id, operations)

#         return data
    

#     # get
#     async def get_document(self, bucket_name:str, collection_name: str, document_id: str) -> dict:

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         collection = bucket.collection(collection_name)  

#         response = collection.get(document_id)

#         return response.content_as(dict)
    


#     async def get_documents(self, bucket_name:str, collection_name: str, document_ids: list[str]):
        
#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         collection = bucket.collection(collection_name)  

#         response = await collection.get_multi(document_ids)

#         parsed_results = [ item.content_as(dict) for item in response.values() ]

#         return parsed_results
    

#     async def list_buckets(self) -> list[str]:

#         buckets = self.cluster.buckets().get_all_buckets()
        
#         bucket_names = [ bucket.name for bucket in buckets ]

#         return bucket_names

    

#     async def list_collections(self, bucket_name:str) -> list[str]:

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return

#         collection_manager = CollectionManager(bucket)
        
#         collections = await collection_manager.get_all_collections()

#         collection_names = [ collection.name for collection in collections ]

#         return collection_names



#     async def list_scopes(self, bucket_name:str):

#         bucket = self.cluster.bucket(bucket_name)

#         if not bucket:
#             return
        
#         scope_manager = ScopeManager(bucket)
        
#         scopes = await scope_manager.get_all_scopes()

#         scope_names = [ scope.name for scope in scopes ]

#         return scope_names