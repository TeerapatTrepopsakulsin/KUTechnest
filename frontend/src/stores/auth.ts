import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AuthTokens } from '../types/auth'
import router from '../router'


const backendUrl = import.meta.env.VITE_BACKEND_URL

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Initialize from localStorage
  const initializeAuth = () => {
    const storedTokens = localStorage.getItem('auth_tokens')
    const storedUser = localStorage.getItem('auth_user')

    if (storedTokens) {
      try {
        tokens.value = JSON.parse(storedTokens)
      } catch (e) {
        console.error('Failed to parse stored tokens:', e)
        localStorage.removeItem('auth_tokens')
      }
    }

    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch (e) {
        console.error('Failed to parse stored user:', e)
        localStorage.removeItem('auth_user')
      }
    }
  }

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
    console.error('Auth error:', message)
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
  // Google Login - Redirect to Google
  const initiateGoogleLogin = async () => {
    try {
      setLoading(true);

      const pendingRole = localStorage.getItem('pending_role') || 'student';
      const response = await fetch(`${backendUrl}/api/auth/google/login?role=${pendingRole}`);

      if (!response.ok) {
        throw new Error('Failed to initialize Google login');
      }

      const data = await response.json();

      if (data.url) {
        window.location.href = data.url;
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to authentication service');
    } finally {
      setLoading(false);
    }
  };

  // Handle OAuth Callback
  const handleOAuthCallback = async (code: string) => {
    try {
      setLoading(true);

      const pendingRole = localStorage.getItem('pending_role') || 'student';
      var response = await fetch(
        `${backendUrl}/api/auth/google/callback?code=${encodeURIComponent(code)}&role=${pendingRole}`
      );

      localStorage.removeItem('pending_role');

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Authentication failed');
      }

      const data = await response.json();
      console.log('OAuth callback response:', data);

      if (!data.access_token) {
        throw new Error('No access token received');
      }

      // Store tokens
      const tokensInfo = {
        access: data.access_token,
        refresh: data.refresh_token || ''
      };

      // Store user info
      const userInfo = {
        id: data.user.id,
        email: data.user.email,
        firstName: data.user.first_name,
        lastName: data.user.last_name,
        // TODO: Bypass role
        // role: 'student',
        role: data.user.role || 'user',
        status: data.user.status || 'pending',
        picture: data.user.profile_picture || ''
      };

      // Persist to localStorage
      setTokens(tokensInfo);
      setUser(userInfo);

      // Navigate to home
      router.push('/');
      
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete authentication');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Initialize on store creation
  initializeAuth()

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
    initiateGoogleLogin,
    handleOAuthCallback,
    clearAuth,
    setError,
    initializeAuth
  }
})