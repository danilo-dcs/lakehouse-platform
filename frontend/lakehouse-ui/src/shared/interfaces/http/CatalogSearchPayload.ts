export interface CatalogFilter {
  property_name: string
  operator: string
  property_value: string
}

export interface CatalogSearchPayload {
  filters: CatalogFilter[]
  page_numbe?: number
}
