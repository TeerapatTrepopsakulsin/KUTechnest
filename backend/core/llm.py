from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from ..config import settings


class JobPostValidation(BaseModel):
    is_valid: bool = Field(description="Whether the job posting is valid for student positions")
    confidence_score: float = Field(description="Confidence score from 0.0 to 1.0")
    issues: List[str] = Field(description="List of issues found in the job posting")
    recommendations: List[str] = Field(description="List of recommendations to improve the job posting")
    reason: str = Field(description="Brief explanation of the validation result")


def get_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE
    )


def validate_job_post(
    title: str,
    work_field: str,
    employment_type: str,
    location: str,
    salary: int,
    min_year: int,
    requirement: str,
    description: str,
    long_description: str = None
) -> JobPostValidation:
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=JobPostValidation)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert job posting validator for a university career platform that connects students with companies.

Your role is to verify if job postings are legitimate, appropriate, and suitable for student positions.

Validation Criteria:
1. The job should be suitable for students or recent graduates (internships, part-time, entry-level positions)
2. Minimum experience requirement should be reasonable for students (typically 0-2 years)
3. The job description should be clear, professional, and detailed
4. Salary should be reasonable and not suspiciously low (possible scam) or unrealistically high
5. Requirements should be realistic for student skill levels
6. The posting should not contain discriminatory language or inappropriate content
7. The job should be a real position, not a pyramid scheme, MLM, or scam

Consider Thai job market standards where appropriate.

{format_instructions}"""),
        ("user", """Validate this job posting:

Title: {title}
Work Field: {work_field}
Employment Type: {employment_type}
Location: {location}
Salary: {salary} THB
Minimum Years of Experience: {min_year}
Requirements: {requirement}
Description: {description}
Long Description: {long_description}

Provide a thorough validation analysis.""")
    ])

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "title": title,
            "work_field": work_field,
            "employment_type": employment_type,
            "location": location,
            "salary": f"{salary:,}",
            "min_year": min_year,
            "requirement": requirement,
            "description": description,
            "long_description": long_description or "Not provided",
            "format_instructions": parser.get_format_instructions()
        })

        return JobPostValidation(**result)
    except Exception as e:
        return JobPostValidation(
            is_valid=False,
            confidence_score=0.0,
            issues=[f"Validation error: {str(e)}"],
            recommendations=["Please try again or contact support"],
            reason="Failed to validate job posting due to technical error"
        )
