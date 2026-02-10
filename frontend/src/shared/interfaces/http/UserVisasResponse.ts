export interface PassportVisa {
  id: string
  visaName: string
  visaIssuer?: string
  visaDescription?: string
  visaSecret?: string
}

export interface PassportVisaAssertions {
  passportVisa: PassportVisa
  status: string
  assertedAt: number
}

export interface UserPassportResponse {
  id: string
  passportVisaAssertions?: PassportVisaAssertions[]
  user_uuid: string
}
