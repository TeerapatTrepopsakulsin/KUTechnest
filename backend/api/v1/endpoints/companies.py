from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from ....core.database import get_db
from ....schemas.company import CompanyCreate, CompanyResponse
from ....crud import company as crud_company
from ....core.llm import validate_company_profile

router = APIRouter()

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    companies = crud_company.get_companies(db, search)
    
    result = []
    for company in companies:
        company_dict = CompanyResponse.from_orm(company)
        company_dict.posts_count = len(company.posts)
        result.append(company_dict)
    
    return result

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = crud_company.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    response = CompanyResponse.from_orm(company)
    response.posts_count = len(company.posts)
    return response

@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company after verifying it with the LLM.
    """
    validation_result = validate_company_profile(**company.model_dump())

    if not validation_result.is_valid or validation_result.confidence_score < 0.7:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "company validation failed",
                "reason": validation_result.reason,
                "issues": validation_result.issues,
                "recommendations": validation_result.recommendations,
                "confidence_score": validation_result.confidence_score
            }
        )
    
    db_company = crud_company.create_company(db, company)

    response = CompanyResponse.model_validate(db_company)
    response.posts_count = 0
    return response