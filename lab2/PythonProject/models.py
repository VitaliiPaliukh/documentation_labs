"""Data models (ORM entities)"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    pass


class AppointmentStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


# Association table for TreatmentPlan and DentalService (many-to-many)
treatment_service_association = Table(
    'treatment_service',
    Base.metadata,
    Column('treatment_plan_id', Integer, ForeignKey('treatment_plans.id')),
    Column('dental_service_id', Integer, ForeignKey('dental_services.id'))
)


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    type = Column(String, nullable=False)  # discriminator for Patient/Doctor

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person'
    }


class Patient(Person):
    __tablename__ = 'patients'

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    insurance_number = Column(String)

    appointments = relationship("Appointment", back_populates="patient")

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }


class Doctor(Person):
    __tablename__ = 'doctors'

    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    license_id = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    schedule_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    treatment_plan_id = Column(Integer, ForeignKey('treatment_plans.id'))

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    treatment_plan = relationship("TreatmentPlan", back_populates="appointment")


class TreatmentPlan(Base):
    __tablename__ = 'treatment_plans'

    id = Column(Integer, primary_key=True)
    diagnosis = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)

    appointment = relationship("Appointment", back_populates="treatment_plan", uselist=False)
    services = relationship("DentalService", secondary=treatment_service_association, back_populates="treatment_plans")


class DentalService(Base):
    __tablename__ = 'dental_services'

    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # discriminator for XRayService/SurgeryService

    treatment_plans = relationship("TreatmentPlan", secondary=treatment_service_association, back_populates="services")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'dental_service'
    }


class XRayService(DentalService):
    __tablename__ = 'xray_services'

    id = Column(Integer, ForeignKey('dental_services.id'), primary_key=True)
    image_resolution = Column(String)
    radiation_dose = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'xray_service'
    }


class SurgeryService(DentalService):
    __tablename__ = 'surgery_services'

    id = Column(Integer, ForeignKey('dental_services.id'), primary_key=True)
    anesthesia_type = Column(String)
    complexity_level = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'surgery_service'
    }
