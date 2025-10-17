export type Job = {
    id: number
    title: string
    company_name: string
    description: string
    image_url?: string | null
    [key: string]: any
  }

export type JobSearch = {
    title?: string
    category?: string
    location?: string
}
