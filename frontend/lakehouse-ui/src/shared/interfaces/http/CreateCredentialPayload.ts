export type StorageType = 'gcs' | 's3' | 'hdfs'

export interface GoogleCredential {
  type: string
  project_id: string
  private_key_id: string
  private_key: string
  client_email: string
  client_id: string
  auth_uri: string
  token_uri: string
  auth_provider_x509_cert_url: string
  client_x509_cert_url: string
  universe_domain: string
}

export interface S3Credential {
  access_key: string
  secret_access_key: string
  region: string
}

export interface HdfsCredential {
  user: string
  password: string
}

export interface CreateCredentialpayload {
  visa_uuids: string[]
  bucket_names: string[]
  storage_type: StorageType
  credential: GoogleCredential | S3Credential | HdfsCredential
}
