from datetime import datetime, timedelta, timezone
from typing import List

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from panda import crud, models
from panda.enums import AddressOwnerType, Sex
from panda.models import Address, Appointment, Patient
from panda.schemas import AddressCreate, AppointmentCreate, PatientCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./panda_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False  # check_same_thread required for SQLite
    },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()()


# Dependency
def get_db():
    db_session = SessionLocal()
    try:
        return db_session
    finally:
        db_session.close()


Faker.seed(0)
fake: Faker = Faker("en-GB")

NHS_NOS = [
    "4609571471",
    "4524408592",
    "4959181745",
    "1565022955",
    "6607313191",
    "2469139341",
    "1451773986",
    "0849244285",
    "8663598831",
    "7133568055",
]

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

# Create lists to hold our fake data
fake_patients: List[PatientCreate] = []
fake_addresses: List[AddressCreate] = []
fake_appointments: List[AppointmentCreate] = []

# Create 10 for each model type
for i in range(10):
    fake_patients.append(
        PatientCreate(
            nhs_number=NHS_NOS[i],
            name=fake.name(),
            dob=fake.date_of_birth(),
            sex=fake.enum(Sex).value,
        )
    )

    fake_addresses.append(
        AddressCreate(
            owner_type=fake.enum(AddressOwnerType).value,
            line1=fake.secondary_address(),
            line2=fake.street_address(),
            town=fake.city(),
            county=fake.county(),
            country=fake.current_country_code(),
            postcode=fake.postcode(),
        )
    )

    # Create a random start time today, between now and 9 hours away
    start_time: datetime = fake.date_time_between(
        datetime.utcnow(),
        datetime.utcnow() + timedelta(hours=fake.random_number(digits=1)),
    ).replace(tzinfo=timezone.utc)
    end_time: datetime = (start_time + timedelta(hours=1))

    fake_appointments.append(
        AppointmentCreate(patient_id=i + 1, start_at=start_time, end_at=end_time)
    )


# Add our fake data to the database
print("\nCreating fake patients...")
for patient in fake_patients:
    print(patient)
    crud.create_patient(db=db, patient=patient)

print("\nCreating fake addresses...")
for i, address in enumerate(fake_addresses, 1):
    print(i, address)
    crud.create_patient_address(db=db, address=address, patient_id=i)

print("\nCreating fake appointments...")
for appointment in fake_appointments:
    print(appointment)
    crud.create_appointment(db=db, appointment=appointment)
