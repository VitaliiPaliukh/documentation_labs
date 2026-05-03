"""Business Logic Layer"""
from typing import List, Dict, Any
from datetime import datetime
from data_access_interfaces import (
    ICSVReader, IPatientRepository, IDoctorRepository,
    IAppointmentRepository, ITreatmentPlanRepository,
    IDentalServiceRepository, IUnitOfWork
)
from models import Patient, Doctor, Appointment, TreatmentPlan, DentalService, XRayService, SurgeryService, AppointmentStatus


class DataImportService:
    """Service for importing data from CSV to database"""

    def __init__(
        self,
        csv_reader: ICSVReader,
        patient_repo: IPatientRepository,
        doctor_repo: IDoctorRepository,
        appointment_repo: IAppointmentRepository,
        treatment_plan_repo: ITreatmentPlanRepository,
        service_repo: IDentalServiceRepository,
        unit_of_work: IUnitOfWork
    ):
        self.csv_reader = csv_reader
        self.patient_repo = patient_repo
        self.doctor_repo = doctor_repo
        self.appointment_repo = appointment_repo
        self.treatment_plan_repo = treatment_plan_repo
        self.service_repo = service_repo
        self.unit_of_work = unit_of_work

    def import_from_csv(self, file_path: str) -> None:
        """Import data from CSV file to database"""
        try:
            # Read CSV data
            rows = self.csv_reader.read_csv(file_path)

            # Dictionaries to track created entities and avoid duplicates
            patients_cache = {}
            doctors_cache = {}
            services_cache = {}

            for row in rows:
                # Create or get patient
                patient_key = row['patient_insurance']
                if patient_key not in patients_cache:
                    patient = Patient(
                        full_name=row['patient_name'],
                        phone=row['patient_phone'],
                        insurance_number=row['patient_insurance']
                    )
                    self.patient_repo.create(patient)
                    patients_cache[patient_key] = patient
                else:
                    patient = patients_cache[patient_key]

                # Create or get doctor
                doctor_key = row['doctor_license']
                if doctor_key not in doctors_cache:
                    doctor = Doctor(
                        full_name=row['doctor_name'],
                        phone=row['doctor_phone'],
                        license_id=row['doctor_license'],
                        specialization=row['doctor_specialization']
                    )
                    self.doctor_repo.create(doctor)
                    doctors_cache[doctor_key] = doctor
                else:
                    doctor = doctors_cache[doctor_key]

                # Create or get dental service
                service_key = row['service_name']
                if service_key not in services_cache:
                    service_type = row['service_type']
                    if service_type == 'xray':
                        service = XRayService(
                            service_name=row['service_name'],
                            base_price=float(row['service_price']),
                            image_resolution=row['service_attr1'],
                            radiation_dose=float(row['service_attr2'])
                        )
                    elif service_type == 'surgery':
                        service = SurgeryService(
                            service_name=row['service_name'],
                            base_price=float(row['service_price']),
                            anesthesia_type=row['service_attr1'],
                            complexity_level=int(row['service_attr2'])
                        )
                    else:
                        service = DentalService(
                            service_name=row['service_name'],
                            base_price=float(row['service_price'])
                        )
                    self.service_repo.create(service)
                    services_cache[service_key] = service
                else:
                    service = services_cache[service_key]

                # Create treatment plan
                treatment_plan = TreatmentPlan(
                    diagnosis=row['diagnosis'],
                    total_cost=float(row['total_cost'])
                )
                treatment_plan.services.append(service)
                self.treatment_plan_repo.create(treatment_plan)

                # Create appointment
                appointment = Appointment(
                    schedule_time=datetime.strptime(row['appointment_date'], '%Y-%m-%d %H:%M:%S'),
                    status=AppointmentStatus[row['appointment_status']],
                    patient=patient,
                    doctor=doctor,
                    treatment_plan=treatment_plan
                )
                self.appointment_repo.create(appointment)

            # Commit all changes
            self.unit_of_work.commit()
            print(f"Successfully imported {len(rows)} records from CSV")

        except Exception as e:
            self.unit_of_work.rollback()
            print(f"Error importing data: {e}")
            raise


class PatientManagementService:
    """Service for managing patients"""

    def __init__(self, patient_repo: IPatientRepository, unit_of_work: IUnitOfWork):
        self.patient_repo = patient_repo
        self.unit_of_work = unit_of_work

    def create_patient(self, full_name: str, phone: str, insurance_number: str) -> Patient:
        """Create new patient"""
        patient = Patient(
            full_name=full_name,
            phone=phone,
            insurance_number=insurance_number
        )
        try:
            self.patient_repo.create(patient)
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise
        return patient

    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return self.patient_repo.get_all()

    def get_patient_by_id(self, patient_id: int) -> Patient:
        """Get patient by ID"""
        return self.patient_repo.get_by_id(patient_id)

    def update_patient(self, patient_id: int, full_name: str, phone: str, insurance_number: str) -> Patient:
        """Update existing patient"""
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        patient.full_name = full_name
        patient.phone = phone
        patient.insurance_number = insurance_number

        try:
            self.patient_repo.update(patient)
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise
        return patient

    def delete_patient(self, patient_id: int) -> None:
        """Delete patient"""
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        try:
            self.patient_repo.delete(patient)
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise


class AppointmentManagementService:
    """Service for managing appointments"""

    def __init__(
        self,
        appointment_repo: IAppointmentRepository,
        patient_repo: IPatientRepository,
        doctor_repo: IDoctorRepository,
        unit_of_work: IUnitOfWork
    ):
        self.appointment_repo = appointment_repo
        self.patient_repo = patient_repo
        self.doctor_repo = doctor_repo
        self.unit_of_work = unit_of_work

    def create_appointment(
        self,
        patient_id: int,
        doctor_id: int,
        schedule_time: datetime,
        status: AppointmentStatus
    ) -> Appointment:
        """Create new appointment"""
        patient = self.patient_repo.get_by_id(patient_id)
        doctor = self.doctor_repo.get_by_id(doctor_id)

        if not patient or not doctor:
            raise ValueError("Patient or Doctor not found")

        appointment = Appointment(
            schedule_time=schedule_time,
            status=status,
            patient=patient,
            doctor=doctor
        )
        self.appointment_repo.create(appointment)
        self.unit_of_work.commit()
        return appointment

    def get_all_appointments(self) -> List[Appointment]:
        """Get all appointments"""
        return self.appointment_repo.get_all()

    def get_all_doctors(self) -> List[Doctor]:
        """Get all doctors"""
        return self.doctor_repo.get_all()

