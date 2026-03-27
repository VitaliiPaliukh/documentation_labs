"""Data Access Layer - Implementation"""
import csv
from typing import List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from data_access_interfaces import (
    ICSVReader, IPatientRepository, IDoctorRepository,
    IAppointmentRepository, ITreatmentPlanRepository,
    IDentalServiceRepository, IUnitOfWork
)
from models import Base, Patient, Doctor, Appointment, TreatmentPlan, DentalService


class CSVReader(ICSVReader):
    """CSV file reader implementation"""

    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data


class PatientRepository(IPatientRepository):
    """Patient repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, patient: Patient) -> Patient:
        self.session.add(patient)
        return patient

    def get_by_id(self, patient_id: int) -> Patient:
        return self.session.query(Patient).filter(Patient.id == patient_id).first()

    def get_all(self) -> List[Patient]:
        return self.session.query(Patient).all()


class DoctorRepository(IDoctorRepository):
    """Doctor repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, doctor: Doctor) -> Doctor:
        self.session.add(doctor)
        return doctor

    def get_by_id(self, doctor_id: int) -> Doctor:
        return self.session.query(Doctor).filter(Doctor.id == doctor_id).first()

    def get_all(self) -> List[Doctor]:
        return self.session.query(Doctor).all()


class AppointmentRepository(IAppointmentRepository):
    """Appointment repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, appointment: Appointment) -> Appointment:
        self.session.add(appointment)
        return appointment

    def get_by_id(self, appointment_id: int) -> Appointment:
        return self.session.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_all(self) -> List[Appointment]:
        return self.session.query(Appointment).all()


class TreatmentPlanRepository(ITreatmentPlanRepository):
    """TreatmentPlan repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, treatment_plan: TreatmentPlan) -> TreatmentPlan:
        self.session.add(treatment_plan)
        return treatment_plan

    def get_by_id(self, plan_id: int) -> TreatmentPlan:
        return self.session.query(TreatmentPlan).filter(TreatmentPlan.id == plan_id).first()

    def get_all(self) -> List[TreatmentPlan]:
        return self.session.query(TreatmentPlan).all()


class DentalServiceRepository(IDentalServiceRepository):
    """DentalService repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, service: DentalService) -> DentalService:
        self.session.add(service)
        return service

    def get_by_id(self, service_id: int) -> DentalService:
        return self.session.query(DentalService).filter(DentalService.id == service_id).first()

    def get_all(self) -> List[DentalService]:
        return self.session.query(DentalService).all()


class UnitOfWork(IUnitOfWork):
    """Unit of Work implementation"""

    def __init__(self, session: Session):
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class DatabaseContext:
    """Database context for managing session and repositories"""

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()
