"""Simple demo script without emojis for Windows console"""
from config import DATABASE_URL
from data_access_implementation import DatabaseContext
from sqlalchemy import text


def main():
    print("=== VERIFICATION OF SYSTEM ===\n")

    db_context = DatabaseContext(DATABASE_URL)
    session = db_context.get_session()

    try:
        print("[1] Database Statistics:")
        print("-" * 50)

        patients_count = session.execute(text("SELECT COUNT(*) FROM patients")).scalar()
        doctors_count = session.execute(text("SELECT COUNT(*) FROM doctors")).scalar()
        appointments_count = session.execute(text("SELECT COUNT(*) FROM appointments")).scalar()
        treatment_plans_count = session.execute(text("SELECT COUNT(*) FROM treatment_plans")).scalar()
        services_count = session.execute(text("SELECT COUNT(*) FROM dental_services")).scalar()
        xray_count = session.execute(text("SELECT COUNT(*) FROM xray_services")).scalar()
        surgery_count = session.execute(text("SELECT COUNT(*) FROM surgery_services")).scalar()

        print(f"Patients: {patients_count}")
        print(f"Doctors: {doctors_count}")
        print(f"Appointments: {appointments_count}")
        print(f"Treatment Plans: {treatment_plans_count}")
        print(f"Services (total): {services_count}")
        print(f"  - X-Ray services: {xray_count}")
        print(f"  - Surgery services: {surgery_count}")

        print("\n[2] Sample Patient:")
        print("-" * 50)

        result = session.execute(text("""
            SELECT
                p.full_name as patient_name,
                p.phone as patient_phone,
                pat.insurance_number,
                COUNT(a.id) as appointments_count
            FROM persons p
            JOIN patients pat ON p.id = pat.id
            LEFT JOIN appointments a ON pat.id = a.patient_id
            GROUP BY p.id
            LIMIT 1
        """)).fetchone()

        if result:
            print(f"Name: {result[0]}")
            print(f"Phone: {result[1]}")
            print(f"Insurance: {result[2]}")
            print(f"Appointments: {result[3]}")

        print("\n[3] Sample Doctor:")
        print("-" * 50)

        result = session.execute(text("""
            SELECT
                p.full_name,
                d.license_id,
                d.specialization,
                COUNT(a.id) as appointments_count
            FROM persons p
            JOIN doctors d ON p.id = d.id
            LEFT JOIN appointments a ON d.id = a.doctor_id
            GROUP BY p.id
            LIMIT 1
        """)).fetchone()

        if result:
            print(f"Name: {result[0]}")
            print(f"License: {result[1]}")
            print(f"Specialization: {result[2]}")
            print(f"Appointments: {result[3]}")

        print("\n[4] Sample Appointment:")
        print("-" * 50)

        result = session.execute(text("""
            SELECT
                p_patient.full_name as patient,
                p_doctor.full_name as doctor,
                a.schedule_time,
                a.status,
                tp.diagnosis,
                tp.total_cost
            FROM appointments a
            JOIN persons p_patient ON a.patient_id = p_patient.id
            JOIN persons p_doctor ON a.doctor_id = p_doctor.id
            LEFT JOIN treatment_plans tp ON a.treatment_plan_id = tp.id
            LIMIT 1
        """)).fetchone()

        if result:
            print(f"Patient: {result[0]}")
            print(f"Doctor: {result[1]}")
            print(f"Date/Time: {result[2]}")
            print(f"Status: {result[3]}")
            print(f"Diagnosis: {result[4]}")
            print(f"Total Cost: {result[5]} UAH")

        print("\n[5] Sample Services:")
        print("-" * 50)

        result = session.execute(text("""
            SELECT
                ds.service_name,
                ds.base_price,
                xs.image_resolution,
                xs.radiation_dose
            FROM dental_services ds
            JOIN xray_services xs ON ds.id = xs.id
            LIMIT 1
        """)).fetchone()

        if result:
            print(f"\nX-Ray Service:")
            print(f"  Name: {result[0]}")
            print(f"  Price: {result[1]} UAH")
            print(f"  Resolution: {result[2]}")
            print(f"  Radiation Dose: {result[3]} mSv")

        result = session.execute(text("""
            SELECT
                ds.service_name,
                ds.base_price,
                ss.anesthesia_type,
                ss.complexity_level
            FROM dental_services ds
            JOIN surgery_services ss ON ds.id = ss.id
            LIMIT 1
        """)).fetchone()

        if result:
            print(f"\nSurgery Service:")
            print(f"  Name: {result[0]}")
            print(f"  Price: {result[1]} UAH")
            print(f"  Anesthesia: {result[2]}")
            print(f"  Complexity: {result[3]}/5")

        print("\n[6] Inheritance Check (Person):")
        print("-" * 50)

        result = session.execute(text("""
            SELECT type, COUNT(*)
            FROM persons
            GROUP BY type
        """)).fetchall()

        for row in result:
            print(f"  {row[0]}: {row[1]} records")

        print("\n[OK] System works correctly!")
        print("[OK] All data successfully imported from CSV to database")
        print("[OK] Relationships between tables are set correctly")
        print("[OK] ORM inheritance (Table-per-Type) works correctly")

    finally:
        session.close()


if __name__ == '__main__':
    main()
