import { useUserStore } from '@/stores/userStore'
import router from '@/router'
import type { LoginResponse } from '../interfaces/http/LoginResponse'

export const unauthorizedRequestHandler = async (apiBaseUrl: string): Promise<boolean> => {
  const userStore = useUserStore()

  const response = await fetch(`${apiBaseUrl}/auth/refresh`, {
    method: 'POST',
    credentials: 'include',
  })

  if (response.status === 401) {
    userStore.clearUser()
    router.push('/login')
    return false
  }

  const data = (await response.json()) as LoginResponse

  userStore.setUser({
    email: data.email,
    role: data.user_role,
    userId: data.user_id,
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    tokenType: data.token_type,
  })

  return true
}
