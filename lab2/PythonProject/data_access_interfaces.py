"""Data Access Layer - Interfaces"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models import Patient, Doctor, Appointment, TreatmentPlan, DentalService


class ICSVReader(ABC):
    """Interface for reading CSV files"""

    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        pass


class IPatientRepository(ABC):
    """Interface for Patient repository"""

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        """Create new patient"""
        pass

    @abstractmethod
    def get_by_id(self, patient_id: int) -> Patient:
        """Get patient by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Patient]:
        """Get all patients"""
        pass


class IDoctorRepository(ABC):
    """Interface for Doctor repository"""

    @abstractmethod
    def create(self, doctor: Doctor) -> Doctor:
        """Create new doctor"""
        pass

    @abstractmethod
    def get_by_id(self, doctor_id: int) -> Doctor:
        """Get doctor by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Doctor]:
        """Get all doctors"""
        pass


class IAppointmentRepository(ABC):
    """Interface for Appointment repository"""

    @abstractmethod
    def create(self, appointment: Appointment) -> Appointment:
        """Create new appointment"""
        pass

    @abstractmethod
    def get_by_id(self, appointment_id: int) -> Appointment:
        """Get appointment by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Appointment]:
        """Get all appointments"""
        pass


class ITreatmentPlanRepository(ABC):
    """Interface for TreatmentPlan repository"""

    @abstractmethod
    def create(self, treatment_plan: TreatmentPlan) -> TreatmentPlan:
        """Create new treatment plan"""
        pass

    @abstractmethod
    def get_by_id(self, plan_id: int) -> TreatmentPlan:
        """Get treatment plan by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[TreatmentPlan]:
        """Get all treatment plans"""
        pass


class IDentalServiceRepository(ABC):
    """Interface for DentalService repository"""

    @abstractmethod
    def create(self, service: DentalService) -> DentalService:
        """Create new dental service"""
        pass

    @abstractmethod
    def get_by_id(self, service_id: int) -> DentalService:
        """Get dental service by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[DentalService]:
        """Get all dental services"""
        pass


class IUnitOfWork(ABC):
    """Interface for Unit of Work pattern"""

    @abstractmethod
    def commit(self):
        """Commit transaction"""
        pass

    @abstractmethod
    def rollback(self):
        """Rollback transaction"""
        pass
