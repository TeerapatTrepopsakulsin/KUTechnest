from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List


class JobPostValidation(BaseModel):
    is_valid: bool = Field(description="Whether the job posting is valid for student positions")
    confidence_score: float = Field(description="Confidence score from 0.0 to 1.0")
    issues: List[str] = Field(description="List of issues found in the job posting")
    recommendations: List[str] = Field(description="List of recommendations to improve the job posting")
    reason: str = Field(description="Brief explanation of the validation result")


def get_job_validation_parser():
    return JsonOutputParser(pydantic_object=JobPostValidation)
