interface BucketItem {
  storage_type: string
  bucket_name: string
}

export interface GetBucketListResponse {
  bucket_list: BucketItem[]
}
