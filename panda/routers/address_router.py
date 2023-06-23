from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from panda import crud, schemas
from panda.database import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Address])
async def get_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db=db)


@router.get("/{address_id}", response_model=schemas.Address)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    return crud.get_address_by_id(db=db, address_id=address_id)
