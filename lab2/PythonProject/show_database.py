"""Quick script to show database structure and sample data"""
import sqlite3

db_path = "dental_clinic.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("DATABASE STRUCTURE")
print("=" * 60)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print(f"\nTotal tables: {len(tables)}\n")

for (table_name,) in tables:
    print(f"[TABLE] {table_name}")

    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"   Rows: {count}")

    # Get columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"   Columns: {', '.join([col[1] for col in columns])}")
    print()

print("=" * 60)
print("SAMPLE DATA")
print("=" * 60)

# Sample patients
print("\n[PATIENTS] Sample Patients (first 3):")
cursor.execute("""
    SELECT p.id, p.full_name, p.phone, pat.insurance_number
    FROM persons p
    JOIN patients pat ON p.id = pat.id
    LIMIT 3
""")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Insurance: {row[3]}")

# Sample doctors
print("\n[DOCTORS] Sample Doctors:")
cursor.execute("""
    SELECT p.id, p.full_name, d.license_id, d.specialization
    FROM persons p
    JOIN doctors d ON p.id = d.id
    LIMIT 3
""")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Name: {row[1]}, License: {row[2]}, Spec: {row[3]}")

# Sample appointments
print("\n[APPOINTMENTS] Sample Appointments (first 3):")
cursor.execute("""
    SELECT a.id, a.schedule_time, a.status, p1.full_name as patient, p2.full_name as doctor
    FROM appointments a
    JOIN persons p1 ON a.patient_id = p1.id
    JOIN persons p2 ON a.doctor_id = p2.id
    LIMIT 3
""")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Date: {row[1]}, Status: {row[2]}")
    print(f"      Patient: {row[3]}, Doctor: {row[4]}")

conn.close()
print("\n" + "=" * 60)
print("Database location: C:\\Users\\vitalik\\PycharmProjects\\PythonProject\\dental_clinic.db")
print("=" * 60)
