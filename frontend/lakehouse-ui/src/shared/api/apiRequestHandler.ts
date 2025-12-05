import sources from '@/assets/configs/sources.json'
import type { SourceConfigs } from '../interfaces/configs/SourceConfigs'
import { unauthorizedRequestHandler } from './unauthorizedRequestHandler'
import { useUserStore } from '@/stores/userStore'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export async function apiRequestHandler<T>(
  endpoint: string,
  method: HttpMethod = 'GET',
  body?: any,
  headers?: any,
): Promise<T> {
  const { lakehouse_api_url }: SourceConfigs = sources as SourceConfigs

  const finalUrl = `${lakehouse_api_url}${endpoint}`

  const userStore = useUserStore()

  const finalHeaders: Record<string, string> = {
    ...(headers || {}),
    ...(userStore.accessToken ? { Authorization: `Bearer ${userStore.accessToken}` } : {}),
  }

  if (['POST', 'PUT', 'PATCH'].includes(method)) {
    finalHeaders['Content-Type'] = 'application/json'
  }

  try {
    let response = await fetch(finalUrl, {
      method,
      headers: finalHeaders,
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include',
    })

    if (response.status === 401) {
      const refreshed = await unauthorizedRequestHandler(lakehouse_api_url)

      if (refreshed) {
        // Retry request with the new token
        const retryHeaders = {
          ...finalHeaders,
          Authorization: `Bearer ${userStore.accessToken}`,
        }

        response = await fetch(finalUrl, {
          method,
          headers: retryHeaders,
          body: body ? JSON.stringify(body) : undefined,
          credentials: 'include',
        })
      }
    }

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(
        `API request failed: ${response.status} ${response.statusText} — ${errorText}`,
      )
    }

    if (response.status === 204) {
      return {} as T
    }

    const data: T = await response.json()
    return data
  } catch (error) {
    console.error('Fetch error:', error)
    throw error
  }
}
