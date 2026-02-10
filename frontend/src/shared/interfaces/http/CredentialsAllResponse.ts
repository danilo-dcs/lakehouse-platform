type StorageType = 'gcs' | 's3' | 'hdfs'

export interface CredentialItem {
  visa_uuids: string[]
  storage_type: StorageType
  bucket_names: []
  credential: string
  id: string
}

export type CredentialsAllResponse = CredentialItem[]
