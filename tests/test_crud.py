from datetime import date
from typing import List

import pytest
from faker import Faker
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from panda import crud, models
from panda.enums import AddressOwnerType, Sex
from panda.models import Address, Appointment, Patient
from panda.schemas import AddressCreate, PatientCreate

Faker.seed(0)
fake: Faker = Faker("en-GB")

SQLALCHEMY_DATABASE_URL = "sqlite:///tests/panda_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # check_same_thread required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# Drop the tables if they exist
if engine.dialect.has_table(engine.connect(), "patients"):
    Patient.__table__.drop(engine)
if engine.dialect.has_table(engine.connect(), "addresses"):
    Address.__table__.drop(engine)
if engine.dialect.has_table(engine.connect(), "appointments"):
    Appointment.__table__.drop(engine)

# Create the tables from out models
db: Session = get_db()
models.Base.metadata.create_all(bind=engine)

@pytest.fixture(name="valid_nhs_numbers")
def fixture_valid_nhs_numbers() -> List[str]:
    """ Returns a list of valid nhs numbers """
    return [
        '4609571471',
        '4524408592',
        '4959181745',
        '1565022955',
        '6607313191',
        '2469139341',
        '1451773986',
        '0849244285',
        '8663598831',
        '7133568055',
    ]

@pytest.fixture(name="invalid_nhs_numbers")
def fixture_invalid_nhs_numbers() -> List[str]:
    """ Returns a list of invalid nhs numbers """
    return [
        '4609571472',
        '4524408593',
        '4959181746',
        '1565022956',
        '6607313192',
        '2469139342',
        '1451773987',
        '0849244286',
        '8663598832',
        '7133568056',
    ]


@pytest.fixture(name="invalid_format_nhs_numbers")
def fixture_invalid_format_nhs_numbers() -> List[str]:
    """ Returns a list of badly formatted but valid nhs numbers """
    return [
        ' 4609571471',
        '452 440 8592',
        '495-918-1745',
    ]


@pytest.fixture(name="valid_patient")
def valid_patient() -> PatientCreate:
    """ Returns a valid patient create object"""
    return PatientCreate(
        nhs_number="350 416 5898",
        name="David Winch",
        dob=date(1988, 12, 25),
        sex=Sex.MALE,
    )


@pytest.fixture(name="valid_address")
def valid_address() -> AddressCreate:
    """ Returns a valid address create object """
    return AddressCreate(
        owner_type=AddressOwnerType.PATIENT,
        line1="69 Pendragon Crescent",
        line2="",
        town="Newquay",
        county="Cornwall",
        postcode="TR7 2SS",
        country="UK"
    )


def test_create_patient(valid_patient: PatientCreate):
    """
    Test creating a patient with valid values and NHS number which isn't in the DB
    """
    crud.create_patient(db=get_db(), patient=valid_patient)


def test_create_patient_with_existing_nhs_no(valid_patient: PatientCreate):
    """
    Test creating a patient with an existing nhs no
    """
    nhs_number = valid_patient.nhs_number
    patient = PatientCreate(
        nhs_number=nhs_number,
        name=fake.name(),
        dob=fake.date_of_birth(),
        sex=fake.enum(Sex),
    )
    with pytest.raises(HTTPException) as execinfo:
        crud.create_patient(db=get_db(), patient=patient)
    assert execinfo.value.status_code == 403


def test_get_patient_by_nhs_number(valid_patient: PatientCreate):
    """
    Test getting a patient by an nhs number
    """
    crud.get_patient_by_nhs_number(db=get_db(), nhs_number=valid_patient.nhs_number)


def test_get_patient_by_id(valid_patient: PatientCreate):
    """
    Test getting a patient by an id
    """
    patient_by_nhs = crud.get_patient_by_nhs_number(db=get_db(), nhs_number=valid_patient.nhs_number)
    patient_by_id = crud.get_patient_by_id(db=get_db(), patient_id=int(patient_by_nhs.id))
    assert str(patient_by_id.nhs_number) == str(patient_by_nhs.nhs_number)

def test_add_patient_address(valid_address: AddressCreate, valid_patient: Patient):
    """
    Test adding an address to a valid patient id
    """
    patient_by_nhs = crud.get_patient_by_nhs_number(db=get_db(), nhs_number=str(valid_patient.nhs_number))
    crud.create_patient_address(db=get_db(), address=valid_address, patient_id=int(patient_by_nhs.id))


def test_add_patient_address_for_nonexistent_patient(valid_address: AddressCreate):
    """
    Test adding an address to an invalid patient id
    """
    with pytest.raises(HTTPException) as execinfo:
        crud.create_patient_address(db=get_db(), address=valid_address, patient_id=999999999)
    assert execinfo.value.status_code == 403
