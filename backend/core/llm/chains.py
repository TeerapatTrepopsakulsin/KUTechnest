from .groq_client import get_llm
from .parsers import ValidationReport, get_validation_report_parser
from .prompts import get_job_validation_prompt, get_company_verification_prompt


def validate_job_post(
    title: str,
    work_field: str,
    employment_type: str,
    location: str,
    onsite: bool,
    salary: int,
    min_year: int,
    requirement: str,
    description: str,
    long_description: str = None,
    *args, **kwargs
) -> ValidationReport:
    llm = get_llm()
    parser = get_validation_report_parser()
    prompt = get_job_validation_prompt()

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "title": title,
            "work_field": work_field,
            "employment_type": employment_type,
            "location": location,
            "onsite": onsite,
            "salary": f"{salary:,}",
            "min_year": min_year,
            "requirement": requirement,
            "description": description,
            "long_description": long_description or "Not provided",
            "format_instructions": parser.get_format_instructions()
        })

        return ValidationReport(**result)
    except Exception as e:
        return ValidationReport(
            is_valid=False,
            confidence_score=0.0,
            issues=[f"Validation error: {str(e)}"],
            recommendations=["Please try again or contact support"],
            reason="Failed to validate job posting due to technical error"
        )


def validate_company_profile(
    name: str,
    website: str,
    description: str,
    contacts: str,
    location: str = None,
    *args, **kwargs
) -> ValidationReport:
    llm = get_llm()
    parser = get_validation_report_parser()
    prompt = get_company_verification_prompt()

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "name": name,
            "website": website,
            "description": description,
            "contacts": contacts,
            "location": location or "Not provided",
            "format_instructions": parser.get_format_instructions()
        })

        return ValidationReport(**result)
    except Exception as e:
        return ValidationReport(
            is_valid=False,
            confidence_score=0.0,
            issues=[f"Validation error: {str(e)}"],
            recommendations=["Please try again or contact support"],
            reason="Failed to validate job posting due to technical error"
        )
