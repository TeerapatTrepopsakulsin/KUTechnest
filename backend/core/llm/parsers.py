from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List


class ValidationReport(BaseModel):
    is_valid: bool = Field(description="Whether the result of the validation is valid")
    confidence_score: float = Field(description="Confidence score from 0.0 to 1.0")
    issues: List[str] = Field(description="List of issues found")
    recommendations: List[str] = Field(description="List of recommendations to improve")
    reason: str = Field(description="Brief explanation of the validation result")


def get_validation_report_parser():
    return JsonOutputParser(pydantic_object=ValidationReport)
