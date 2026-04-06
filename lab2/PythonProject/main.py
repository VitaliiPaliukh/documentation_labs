"""Main application entry point with Dependency Injection"""
from config import DATABASE_URL, CSV_FILE_PATH
from data_access_implementation import (
    DatabaseContext, CSVReader, PatientRepository, DoctorRepository,
    AppointmentRepository, TreatmentPlanRepository, DentalServiceRepository,
    UnitOfWork
)
from business_logic import DataImportService, PatientManagementService, AppointmentManagementService


class DependencyContainer:
    """Dependency Injection Container"""

    def __init__(self, connection_string: str):
        # Database context
        self.db_context = DatabaseContext(connection_string)
        self.session = self.db_context.get_session()

        # Data access layer (repositories)
        self.csv_reader = CSVReader()
        self.patient_repository = PatientRepository(self.session)
        self.doctor_repository = DoctorRepository(self.session)
        self.appointment_repository = AppointmentRepository(self.session)
        self.treatment_plan_repository = TreatmentPlanRepository(self.session)
        self.dental_service_repository = DentalServiceRepository(self.session)
        self.unit_of_work = UnitOfWork(self.session)

        # Business logic layer (services)
        self.data_import_service = DataImportService(
            csv_reader=self.csv_reader,
            patient_repo=self.patient_repository,
            doctor_repo=self.doctor_repository,
            appointment_repo=self.appointment_repository,
            treatment_plan_repo=self.treatment_plan_repository,
            service_repo=self.dental_service_repository,
            unit_of_work=self.unit_of_work
        )

        self.patient_management_service = PatientManagementService(
            patient_repo=self.patient_repository,
            unit_of_work=self.unit_of_work
        )

        self.appointment_management_service = AppointmentManagementService(
            appointment_repo=self.appointment_repository,
            patient_repo=self.patient_repository,
            doctor_repo=self.doctor_repository,
            unit_of_work=self.unit_of_work
        )

    def cleanup(self):
        """Cleanup resources"""
        self.session.close()


def main():
    """Main application entry point"""
    print("=== Dental Clinic Management System ===\n")

    # Initialize dependency container
    container = DependencyContainer(DATABASE_URL)

    try:
        # Import data from CSV
        print(f"Importing data from {CSV_FILE_PATH}...")
        container.data_import_service.import_from_csv(CSV_FILE_PATH)

        # Display statistics
        print("\n=== Database Statistics ===")
        patients = container.patient_management_service.get_all_patients()
        appointments = container.appointment_management_service.get_all_appointments()

        print(f"Total Patients: {len(patients)}")
        print(f"Total Appointments: {len(appointments)}")

        # Display sample data
        if patients:
            print(f"\nSample Patient: {patients[0].full_name}, Phone: {patients[0].phone}")

        if appointments:
            print(f"Sample Appointment: {appointments[0].schedule_time}, Status: {appointments[0].status.value}")

        print("\n=== Data import completed successfully ===")

    except FileNotFoundError:
        print(f"\nError: CSV file '{CSV_FILE_PATH}' not found!")
        print("Please run 'python csv_generator.py' first to generate the data file.")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        container.cleanup()


if __name__ == '__main__':
    main()
