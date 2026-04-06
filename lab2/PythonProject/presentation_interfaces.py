"""Presentation Layer - Interfaces only (no implementation yet)"""
from abc import ABC, abstractmethod
from typing import List


class IPatientView(ABC):
    """Interface for patient view"""

    @abstractmethod
    def display_patients(self, patients: List) -> None:
        """Display list of patients"""
        pass

    @abstractmethod
    def display_patient_details(self, patient) -> None:
        """Display detailed information about patient"""
        pass

    @abstractmethod
    def get_patient_input(self) -> dict:
        """Get patient input from user"""
        pass


class IAppointmentView(ABC):
    """Interface for appointment view"""

    @abstractmethod
    def display_appointments(self, appointments: List) -> None:
        """Display list of appointments"""
        pass

    @abstractmethod
    def display_appointment_details(self, appointment) -> None:
        """Display detailed information about appointment"""
        pass

    @abstractmethod
    def get_appointment_input(self) -> dict:
        """Get appointment input from user"""
        pass


class IDoctorView(ABC):
    """Interface for doctor view"""

    @abstractmethod
    def display_doctors(self, doctors: List) -> None:
        """Display list of doctors"""
        pass

    @abstractmethod
    def display_doctor_details(self, doctor) -> None:
        """Display detailed information about doctor"""
        pass


class ITreatmentPlanView(ABC):
    """Interface for treatment plan view"""

    @abstractmethod
    def display_treatment_plans(self, plans: List) -> None:
        """Display list of treatment plans"""
        pass

    @abstractmethod
    def display_treatment_plan_details(self, plan) -> None:
        """Display detailed information about treatment plan"""
        pass


class IMainMenuView(ABC):
    """Interface for main menu view"""

    @abstractmethod
    def display_menu(self) -> None:
        """Display main menu"""
        pass

    @abstractmethod
    def get_user_choice(self) -> int:
        """Get user menu choice"""
        pass
