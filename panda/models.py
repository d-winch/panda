from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from panda.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    nhs_number = Column(String, unique=True, index=True)
    name = Column(String)
    dob = Column(Date)
    sex = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    address = relationship("Address", back_populates="owner", cascade="all,delete")
    appointments = relationship("Appointment", back_populates="patient")  # [ ] TODO Cascade type


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    owner_type = Column(String)
    owner_id = Column(Integer, ForeignKey("patients.id"), index=True)
    line1 = Column(String)
    line2 = Column(String, default="")
    town = Column(String)
    county = Column(String)
    postcode = Column(String)
    country = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    owner = relationship("Patient", back_populates="address")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    # clinician_id = Column(Integer, ForeignKey("clinicians.id"), index=True)
    # department_id = Column(Integer, ForeignKey("departments.id"), index=True)
    # location_id = Column(Integer, ForeignKey("locations.id"), index=True)
    # organisation_id = Column(Integer, ForeignKey("organisations.id"), index=True)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    attended_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    ended_at = Column(DateTime)
    is_cancelled = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    patient = relationship("Patient", back_populates="appointments")
