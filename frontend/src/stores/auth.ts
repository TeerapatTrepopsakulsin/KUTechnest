import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AuthTokens } from '../types/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!tokens.value?.access)
  const userRole = computed(() => user.value?.role)
  const userStatus = computed(() => user.value?.status)
  const isApproved = computed(() => isAuthenticated.value && user.value?.status === 'approved')

  // Helper functions
  const setLoading = (loading: boolean) => {
    isLoading.value = loading
    error.value = loading ? null : error.value
  }

  const setError = (message: string) => {
    error.value = message
    isLoading.value = false
  }

  const setTokens = (newTokens: AuthTokens) => {
    tokens.value = newTokens
    localStorage.setItem('auth_tokens', JSON.stringify(newTokens))
  }

  const setUser = (newUser: User) => {
    user.value = newUser
    localStorage.setItem('auth_user', JSON.stringify(newUser))
  }

  const clearAuth = () => {
    user.value = null
    tokens.value = null
    error.value = null
    localStorage.removeItem('auth_tokens')
    localStorage.removeItem('auth_user')
  }

  // Main auth actions
  const login = async (googleToken: string) => {
    setLoading(true)
    try {
      const response = await fetch('/api/auth/google-login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          google_token: googleToken
        })
      })

      const data = await response.json()

      if (response.ok) {
        setTokens({
          access: data.access_token,
          refresh: data.refresh_token
        })
        
        setUser({
          id: data.user.id,
          email: data.user.email,
          name: data.user.name,
          role: data.user.role,      //  Role from backend
          status: data.user.status,   //  Status from backend  
          picture: data.user.picture
        })
        
        return { success: true }
      } else {
        setError(data.error || 'Login failed')
        return { success: false, error: data.error }
      }
      
    } catch (err) {
      setError('Network error during login')
      return { success: false, error: 'Network error' }
    } finally {
      setLoading(false)
    }
  }

  return {
    // State
    user,
    tokens,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    userRole,
    userStatus,
    isApproved,
    
    // Actions
    login,
    clearAuth,
    setError
  }
})