from .groq_client import get_llm
from .parsers import JobPostValidation, get_job_validation_parser
from .prompts import get_job_validation_prompt


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
    parser = get_job_validation_parser()
    prompt = get_job_validation_prompt()

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
