export type JobPostForm = {
  title: string
  work_field: string
  location: string
  onsite: boolean
  salary: number | null
  min_year: number | null
  employment_type: string
  requirement: string
  description: string
  image_url: string
  long_description: string
}

export type JobPostResponse = {
  id: string
  status: string
  message: string
  data: JobPostForm
}
