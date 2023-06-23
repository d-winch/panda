from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from panda import crud, schemas
from panda.database import SessionLocal
from panda.util.common_query_params import CommonQuery


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Patient])
async def get_patients(commons: CommonQuery, db: Session = Depends(get_db)):
    db_patients = crud.get_patients(
        db, offset=commons.offset, limit=commons.limit
    )
    return db_patients


@router.post("/", response_model=schemas.Patient)
async def create_patient(
    patient: schemas.PatientCreate, db: Session = Depends(get_db)
):
    return crud.create_patient(db=db, patient=patient)


# Must be above get_patient
@router.get("/getbynhsnumber", response_model=schemas.Patient)
async def get_patient_by_nhs_number(
    nhs_no: str, db: Session = Depends(get_db)
):
    return crud.get_patient_by_nhs_number(db=db, nhs_number=nhs_no)


@router.get("/{patient_id}", response_model=schemas.Patient)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_by_id(db=db, patient_id=patient_id)


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.delete_patient(db=db, patient_id=patient_id)


@router.put(
    "/{patient_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_patient(
    patient_id: int,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
):
    db_stored_patient = crud.get_patient_by_id(patient_id=patient_id, db=db)
    if not db_stored_patient:
        raise HTTPException(
            status_code=403, detail=f"No patient found for ID: {patient_id}"
        )
    db_updated_patient = crud.update_patient(
        db=db, patient_id=patient_id, patient=patient
    )
    return db_updated_patient


@router.post("/{patient_id}/address", response_model=schemas.Address)
async def create_patient_address(
    address: schemas.AddressCreate,
    patient_id: int,
    db: Session = Depends(get_db),
):
    db_address = crud.create_patient_address(
        db=db, address=address, owner_id=patient_id
    )
    if not db_address:
        raise HTTPException(
            400,
            detail=f"Cannot create an address for an unknown owner: {patient_id}",
        )
    return db_address


@router.get("/{patient_id}/address", response_model=List[schemas.Address])
async def get_patient_address(patient_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address_by_owner_id(db=db, owner_id=patient_id)
    return db_address
