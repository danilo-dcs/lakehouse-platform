const isTokenExpired = (token: string | null): boolean => {
  if (!token) return true

  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const payload = JSON.parse(window.atob(base64))

    // 'exp' is in seconds, Date.now() gives milliseconds
    const currentTime = Date.now() / 1000

    return payload.exp < currentTime
  } catch (e) {
    console.error('Invalid token:', e)
    return true
  }
}

export default isTokenExpired
