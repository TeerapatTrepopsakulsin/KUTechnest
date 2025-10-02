from sqlalchemy.orm import Session
from ..models.company import Company
from ..schemas.company import CompanyCreate

def get_companies(db: Session, search: str = None):
    query = db.query(Company)
    if search:
        query = query.filter(
            Company.name.contains(search) |
            Company.location.contains(search)
        )
    return query.all()

def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
