from typing import List

from fastapi import APIRouter, Depends
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
    prefix="/appointments",
    tags=["appointments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Appointment])
async def get_appointments(commons: CommonQuery, db: Session = Depends(get_db)):
    return crud.get_appointments(db, offset=commons.offset, limit=commons.limit)


@router.get("/{appointment_id}", response_model=schemas.Appointment)
async def get_appointment_by_id(appointment_id: int, db: Session = Depends(get_db)):
    return crud.get_appointment_by_id(db, appointment_id=appointment_id)


@router.post("/", response_model=schemas.Appointment)
async def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)


# [ ] TODO - Add cancelled_at timestamp if is_cancelled is updated
@router.put(
    "/{appointment_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_appointment(appointment_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.update_appointment(db=db, appointment_id=appointment_id, appointment=appointment)


# [ ] TODO - Add cancelled_at timestamp
@router.post(
    "/{appointment_id}/cancel",
    responses={403: {"description": "Operation forbidden"}},
)
async def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return crud.cancel_appointment(db=db, appointment_id=appointment_id)


@router.post(
    "/{appointment_id}/attended",
    responses={403: {"description": "Operation forbidden"}},
)
async def mark_appointment_attended(appointment_id: int, db: Session = Depends(get_db)):
    return crud.mark_appointment_attended(db=db, appointment_id=appointment_id)
