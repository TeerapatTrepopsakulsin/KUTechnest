export type User = {
    id: number
    email: string
    firstName: string
    lastName: string
    role: 'student' | 'company' | 'user'
    status: 'pending' | 'approved' | 'rejected'
    picture: string
}

export type AuthTokens = {
    access: string
    refresh: string
}

export type LoginCredentials = {
    googleToken: string
}

export type RegisterData = {
    email: string
    firstName: string
    lastName: string
    password: string
    confirmPassword: string
}
