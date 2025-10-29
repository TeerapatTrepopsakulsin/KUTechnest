export interface StudentRegistration {
  name: string;
  nick_name: string;
  pronoun: string;
  age: number | null;
  year: number | null;
  ku_generation: number | null;
  faculty: string;
  major: string;
  about_me: string;
  email: string;
}

export interface CompanyRegistration {
  name: string;
  website: string;
  logo_url: string;
  location: string;
  description: string;
  contacts: string;
}