from langchain_core.prompts import ChatPromptTemplate


def get_job_validation_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert job posting validator for a university career platform that connects students with companies.

Your role is to verify if job postings are legitimate, appropriate, and suitable for student positions. Don't care about the attractiveness of the job; focus on legitimate context.

Validation Criteria:
1. The job should be suitable for students or recent graduates (internships, part-time, full-time, entry-level positions)
2. Minimum experience requirement should be reasonable for students (typically 0-2 years)
3. The job description should be clear, professional, and detailed enough to understand the role
4. Salary should be reasonable and not unrealistically high (Can be zero for unpaid internships)
5. Requirements should be realistic for student skill levels (e.g., basic programming skills for tech roles)
6. The posting should not contain discriminatory language or inappropriate content
7. The job should be a real position, not a pyramid scheme, MLM, or scam
8. The job location should be specified if not remote, reasonable, and not contradict with the job description

Consider Thai job market standards where appropriate.

{format_instructions}"""),
        ("user", """Validate this job posting:

Title: {title}
Work Field: {work_field}
Employment Type: {employment_type}
Location: {location}
Onsite: {onsite}
Monthly Salary: {salary} THB
Minimum Years of Experience: {min_year}
Requirements: {requirement}
Description: {description}
Long Description: {long_description}

Provide a thorough validation analysis.""")
    ])


def get_company_verification_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert company profile validator for a university career platform that connects students with companies.
Your role is to verify if company profiles are legitimate, appropriate, and suitable for student job seekers.

Validation Criteria:
1. The company should be a real and registered business entity.
2. The company contacts should be valid and professional (e.g., no personal email addresses).
3. The company description should be clear, professional, and detailed enough to understand the business.
4. The company should not be involved in illegal or unethical activities.
5. The company website should be a functional link and not a placeholder.
6. The company should provide clear and honest information about its operations and values, student should understand the overall information.
7. The company location should be specified and reasonable.
8. The company should not be a pyramid scheme, MLM, or scam.
Consider Thai business standards where appropriate.
         
{format_instructions}"""),
        ("user", """Validate this company profile:
         
Name: {name}
Website: {website}
Description: {description}
Contacts: {contacts}
Location: {location}
         
Provide a thorough validation analysis.""")
    ])


def get_student_profile_validation_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert student profile validator for a university career platform that connects students with companies.
Your role is to verify if student profiles are legitimate, appropriate, and suitable for job seekers.
Validation Criteria:
1. The student's name should be realistic and appropriate.
2. The academic background should be valid and correspond to the university's standards.
3. The contacts should be professional and valid (e.g., university email addresses).
4. The "About Me" section should be clear, professional, and detailed enough to understand
    the student's background and aspirations.
5. The date of birth should indicate that the student is of legal age to work.
6. The profile should not contain any inappropriate content or language.
7. The profile should be complete and provide enough information for potential employers to assess the student's suitability for job opportunities.
8. KU Generation should be a valid number corresponding to the student's enrollment year (i.e., if the student enrolled in 2023, the KU Generation should be 83).
9. The student ID should follow the standard format used by the university. (i.e., 10 digits long)
Consider Thai academic standards where appropriate.
         
{format_instructions}"""),
        ("user", """Validate this student profile:
         
Name: {name}
Academic Background: {academic_background}
Contacts: {contacts}
About Me: {about_me}
Date of Birth: {date_of_birth}
         
Provide a thorough validation analysis.""")
    ])
