# pylint: disable=expression-not-assigned
from datetime import datetime
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.orm import Session

from panda import models, schemas


class ErrorsEng(Enum):
    NO_PATIENT_FOR_ID = "No patient found for ID, ID: "
    NO_PATIENT_FOR_NHS = "No patient found for NHS Number, NHS No: "
    NHS_NO_VALUE_ERROR = (
        "Please ensure NHS Number is a 10 digit numeric string, NHS No: "
    )
    NHS_NO_INVALID = "NHS Number failed validation, NHS No.: "
    PATIENT_ALREADY_EXISTS = (
        "There is already a patient with this NHS Number, NHS No.: "
    )
    NO_APPT_FOR_ID = "No appointment found for ID: "
    CANNOT_EDIT_CANCELLED_APPT = "Cannot edit a cancelled appointment ID: "
    APPT_ALREADY_CANCELLED = "Appointment is already cancelled ID: "
    CANNOT_MARK_CANCELLED_APPT_ATTENDED = (
        "Cannot mark a cancelled appointment as attended ID: "
    )
    CANNOT_MARK_APPT_ATTENDED_PAST_END = (
        "Cannot mark an appointment as attended after the end time, ID: "
    )
    APPT_MARKED_AS_ATTENDED = "Appointment already marked as attended, ID: "
    NHS_NUMBER_CONFLICT = (
        "A patient already exists with this NHS Number, NHS No.: "
    )
    APPT_ALREADY_ATTENDED = "Cannot alter an attended appointment, ID: "


def get_patient_by_id(db: Session, patient_id: int):
    db_stored_patient = (
        db.query(models.Patient)
        .filter(models.Patient.id == patient_id)
        .first()
    )
    if not db_stored_patient:
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.NO_PATIENT_FOR_ID.value}{patient_id}",
        )
    return db_stored_patient


def get_patient_by_nhs_number(db: Session, nhs_number: str):
    db_patient = (
        db.query(models.Patient)
        .filter(models.Patient.nhs_number == nhs_number)
        .first()
    )
    if not db_patient:
        raise HTTPException(
            404, detail=f"{ErrorsEng.NO_PATIENT_FOR_NHS.value}{nhs_number}"
        )
    return db_patient


def get_patients(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(offset).limit(limit).all()


def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = (
        db.query(models.Patient)
        .filter(models.Patient.nhs_number == patient.nhs_number)
        .first()
    )
    if db_patient:
        raise HTTPException(
            403,
            detail=f"{ErrorsEng.PATIENT_ALREADY_EXISTS.value}{patient.nhs_number}",
        )
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(
    db: Session, patient_id: int, patient: schemas.PatientCreate
):
    db_stored_patient_by_id = get_patient_by_id(db=db, patient_id=patient_id)
    if not db_stored_patient_by_id:
        raise HTTPException(
            404, detail=f"{ErrorsEng.NO_PATIENT_FOR_ID.value}'{patient_id}'"
        )

    db_stored_patient_by_nhs_no = get_patient_by_nhs_number(
        db=db, nhs_number=patient.nhs_number
    )
    if bool(db_stored_patient_by_nhs_no.id != db_stored_patient_by_id.id):
        raise HTTPException(
            403,
            detail=f"{ErrorsEng.NHS_NUMBER_CONFLICT.value}'{patient.nhs_number}'",
        )
    for var, value in patient:
        setattr(db_stored_patient_by_id, var, value) if value or str(
            value
        ) == "False" else None
    db.commit()
    db.refresh(db_stored_patient_by_id)
    return db_stored_patient_by_id


def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient_by_id(db=db, patient_id=patient_id)
    db.delete(db_patient)
    db.commit()
    return


def get_addresses(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Address).offset(offset).limit(limit).all()


def create_patient_address(
    db: Session, address: schemas.AddressCreate, owner_id: int
):
    owner = (
        db.query(models.Patient).filter(models.Patient.id == owner_id).first()
    )
    if not owner:
        raise HTTPException(
            403, detail=f"{ErrorsEng.NO_PATIENT_FOR_ID.value}'{owner_id}'"
        )
    db_address = models.Address(**address.dict(), owner_id=owner_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_by_owner_id(db: Session, owner_id: int):
    owner = (
        db.query(models.Patient).filter(models.Patient.id == owner_id).first()
    )
    if not owner:
        raise HTTPException(
            403, detail=f"{ErrorsEng.NO_PATIENT_FOR_ID.value}'{owner_id}'"
        )
    return (
        db.query(models.Address)
        .filter(models.Address.owner_id == owner_id)
        .all()
    )


def get_address_by_id(db: Session, address_id: int):
    return (
        db.query(models.Address)
        .filter(models.Address.id == address_id)
        .first()
    )


def get_appointments(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(offset).limit(limit).all()


def get_appointment_by_id(db: Session, appointment_id):
    db_stored_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not db_stored_appointment:
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.NO_APPT_FOR_ID.value}{appointment_id}",
        )
    return db_stored_appointment


def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update_appointment(
    db: Session, appointment_id: int, appointment: schemas.AppointmentCreate
):
    # Guard against non existent appointment
    db_stored_appointment = get_appointment_by_id(
        db=db, appointment_id=appointment_id
    )
    if bool(db_stored_appointment.is_cancelled):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.CANNOT_EDIT_CANCELLED_APPT.value}{appointment_id}",
        )

    # Guard against non-existent patient
    db_stored_appointment_patient = get_patient_by_id(
        patient_id=appointment.patient_id, db=db
    )
    if not db_stored_appointment_patient:
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.NO_PATIENT_FOR_ID.value}{appointment.patient_id}",
        )

    # Guard against appointment already attended
    if bool(db_stored_appointment.attended_at):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.APPT_ALREADY_ATTENDED.value}{appointment_id}",
        )

    for var, value in appointment:
        setattr(db_stored_appointment, var, value) if value or str(
            value
        ) == "False" else None
    db.commit()
    db.refresh(db_stored_appointment)
    return db_stored_appointment


def cancel_appointment(db: Session, appointment_id: int):
    # Guard against cancelled appointment
    db_stored_appointment = get_appointment_by_id(
        db=db, appointment_id=appointment_id
    )
    if bool(db_stored_appointment.attended_at):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.APPT_ALREADY_ATTENDED.value}{appointment_id}",
        )
    if bool(db_stored_appointment.is_cancelled):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.APPT_ALREADY_CANCELLED.value}{appointment_id}",
        )

    setattr(db_stored_appointment, "is_cancelled", True)
    setattr(db_stored_appointment, "cancelled_at", datetime.utcnow())
    db.commit()
    db.refresh(db_stored_appointment)
    return db_stored_appointment


def mark_appointment_attended(db: Session, appointment_id: int):
    # Guard against cancelled appointment
    db_stored_appointment = get_appointment_by_id(
        db=db, appointment_id=appointment_id
    )
    if bool(db_stored_appointment.is_cancelled):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.CANNOT_MARK_CANCELLED_APPT_ATTENDED.value}{appointment_id}",
        )
    if bool(datetime.now() > db_stored_appointment.end_at):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.CANNOT_MARK_APPT_ATTENDED_PAST_END.value}{appointment_id}",
        )
    if bool(db_stored_appointment.attended_at):
        raise HTTPException(
            status_code=403,
            detail=f"{ErrorsEng.APPT_MARKED_AS_ATTENDED.value}{appointment_id}",
        )
    # Should we allow this? Disallows running early
    # if datetime.now() < db_stored_appointment.start_at:
    #     raise HTTPException(
    #         status_code=403, detail="Cannot mark an appointment as attended before the start time"
    #     )
    setattr(db_stored_appointment, "attended_at", datetime.utcnow())
    db.commit()
    db.refresh(db_stored_appointment)
    return db_stored_appointment
