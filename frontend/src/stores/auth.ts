import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AuthTokens } from '../types/auth'
import type { StudentRegistration, CompanyRegistration } from '../types/registration'
import router from '../router'


const backendUrl = import.meta.env.VITE_BACKEND_URL

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isRegistering = ref(false)

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

  // Registration functions
  const getGoogleLoginUrl = async (role: string) => {
    try {
      const response = await fetch(`${backendUrl}/api/auth/google/login?role=${role}`)
      const data = await response.json()
      return data.url
    } catch (e) {
      console.error('Failed to get Google login URL:', e)
      throw e
    }
  }

  const registerStudent = async (studentData: StudentRegistration) => {
    setLoading(true)
    try {
      console.log('Registering with token:', tokens.value?.access);
      console.log('Registration data:', {
        ...studentData,
        email: user.value?.email || studentData.email
      });

      const response = await fetch(`${backendUrl}/api/auth/register/student`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${tokens.value?.access}`  // Changed to uppercase Bearer
        },
        body: JSON.stringify({
          ...studentData,
          email: user.value?.email || studentData.email // Ensure we use the email from OAuth
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Registration failed:', response.status, errorData);
        throw new Error(errorData.detail || 'Failed to register student');
      }

      const data = await response.json();
      console.log('Registration successful:', data);
      user.value = data.user;
      localStorage.setItem('auth_user', JSON.stringify(data.user));
    } catch (e) {
      console.error('Failed to register student:', e)
      error.value = e instanceof Error ? e.message : 'Failed to register student'
      throw e
    } finally {
      setLoading(false)
    }
  }

  const registerCompany = async (companyData: CompanyRegistration) => {
    setLoading(true)
    try {
      const response = await fetch(`${backendUrl}/api/auth/register/company`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${tokens.value?.access}`
        },
        body: JSON.stringify(companyData)
      })

      if (!response.ok) {
        throw new Error('Failed to register company')
      }

      const data = await response.json()
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
    } catch (e) {
      console.error('Failed to register company:', e)
      error.value = e instanceof Error ? e.message : 'Failed to register company'
      throw e
    } finally {
      setLoading(false)
    }
  }

  const setError = (message: string) => {
    error.value = message
    isLoading.value = false
    console.error('Auth error:', message)
    alert('Auth error: ' + message)
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

      const pendingRole = localStorage.getItem('pending_role');
      if (!pendingRole) {
        throw new Error('No role specified for registration');
      }
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

      // Store tokens and user info
      const tokensInfo = {
        access: data.access_token,
        refresh: data.refresh_token || ''
      };
      
      // Make sure we store both tokens and user
      setTokens(tokensInfo);
      setUser(data.user);
      
      return true; // Indicate successful authentication

      // Store tokens temporarily for API access
      setTokens(tokensInfo);

      // Create base user info
      const userInfo = {
        id: data.user.id,
        email: data.user.email,
        firstName: data.user.first_name,
        lastName: data.user.last_name,
        role: data.user.role || 'user',
        status: data.user.status || 'pending',
        picture: data.user.profile_picture || ''
      };

      // Check if this is a registration flow with stored form data
      const isRegistering = localStorage.getItem('is_registering') === 'true';
      const storedFormData = localStorage.getItem('registration_form_data');
      const storedRole = localStorage.getItem('pending_role');

      if (isRegistering && storedFormData && storedRole) {
        // Store minimal user info for the registration process
        setUser(userInfo);
        
        try {
          // Parse stored form data
          const formData = JSON.parse(storedFormData);

          // Register user based on role
          if (storedRole === 'student') {
            await registerStudent(formData);
          } else {
            await registerCompany(formData);
          }

          // Clear registration data
          localStorage.removeItem('is_registering');
          localStorage.removeItem('registration_form_data');
          localStorage.removeItem('pending_role');

          // Navigate to home after successful registration
          router.push('/');
          return true;
        } catch (err) {
          // If registration fails, clear tokens and redirect to register
          console.error('Registration failed:', err);
          clearAuth();
          router.push('/register');
          throw err;
        }
      } else if (data.user.status === 'pending' || !data.user.role || data.user.role === 'user') {
        // Existing user that hasn't completed registration
        setUser(userInfo);
        router.push('/register');
        return true;
      }

      // If we get here, user is already registered

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
    isRegistering,

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
    initializeAuth,
    getGoogleLoginUrl,
    registerStudent,
    registerCompany
  }
})