export type OperatorKey = 'equals' | 'not equals' | 'contains' | 'greater than' | 'lower than'

export type PropertyName =
  | 'collection_id'
  | 'collection_name'
  | 'is_public'
  | 'inserted_at'
  | 'inserted_by'
  | 'storage_type'
  | 'location'
  | 'collection_description'
  | 'status'

export interface CollectionFilter {
  property_name: PropertyName
  property_value: any
  operator: OperatorKey
}

export interface CollectionSearchRequest {
  filters?: CollectionFilter[]
  page_number?: number
}
