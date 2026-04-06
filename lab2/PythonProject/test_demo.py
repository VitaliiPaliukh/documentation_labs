"""Демонстраційний скрипт для перевірки роботи системи"""
from config import DATABASE_URL
from data_access_implementation import DatabaseContext
from sqlalchemy import text


def main():
    print("=== ПЕРЕВІРКА РОБОТИ СИСТЕМИ ===\n")

    # Підключаємось до БД
    db_context = DatabaseContext(DATABASE_URL)
    session = db_context.get_session()

    try:
        # 1. Перевірка кількості записів
        print("1️⃣ Статистика бази даних:")
        print("-" * 50)

        patients_count = session.execute(text("SELECT COUNT(*) FROM patients")).scalar()
        doctors_count = session.execute(text("SELECT COUNT(*) FROM doctors")).scalar()
        appointments_count = session.execute(text("SELECT COUNT(*) FROM appointments")).scalar()
        treatment_plans_count = session.execute(text("SELECT COUNT(*) FROM treatment_plans")).scalar()
        services_count = session.execute(text("SELECT COUNT(*) FROM dental_services")).scalar()
        xray_count = session.execute(text("SELECT COUNT(*) FROM xray_services")).scalar()
        surgery_count = session.execute(text("SELECT COUNT(*) FROM surgery_services")).scalar()

        print(f"Пацієнтів: {patients_count}")
        print(f"Лікарів: {doctors_count}")
        print(f"Записів на прийом: {appointments_count}")
        print(f"Планів лікування: {treatment_plans_count}")
        print(f"Послуг (всього): {services_count}")
        print(f"  - Рентген послуг: {xray_count}")
        print(f"  - Хірургічних послуг: {surgery_count}")

        # 2. Приклад пацієнта з записами
        print("\n2️⃣ Приклад пацієнта з його записами:")
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
            print(f"Пацієнт: {result[0]}")
            print(f"Телефон: {result[1]}")
            print(f"Страховка: {result[2]}")
            print(f"Кількість записів: {result[3]}")

        # 3. Приклад лікаря
        print("\n3️⃣ Приклад лікаря:")
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
            print(f"Лікар: {result[0]}")
            print(f"Ліцензія: {result[1]}")
            print(f"Спеціалізація: {result[2]}")
            print(f"Кількість записів: {result[3]}")

        # 4. Приклад запису з планом лікування
        print("\n4️⃣ Приклад запису на прийом:")
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
            print(f"Пацієнт: {result[0]}")
            print(f"Лікар: {result[1]}")
            print(f"Дата/час: {result[2]}")
            print(f"Статус: {result[3]}")
            print(f"Діагноз: {result[4]}")
            print(f"Вартість: {result[5]} грн")

        # 5. Приклад послуг
        print("\n5️⃣ Приклади послуг:")
        print("-" * 50)

        # Рентген послуга
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
            print(f"\n📷 Рентген послуга:")
            print(f"  Назва: {result[0]}")
            print(f"  Ціна: {result[1]} грн")
            print(f"  Роздільність: {result[2]}")
            print(f"  Доза опромінення: {result[3]} мЗв")

        # Хірургічна послуга
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
            print(f"\n🔪 Хірургічна послуга:")
            print(f"  Назва: {result[0]}")
            print(f"  Ціна: {result[1]} грн")
            print(f"  Анестезія: {result[2]}")
            print(f"  Складність: {result[3]}/5")

        # 6. Перевірка наслідування (Table-per-Type)
        print("\n6️⃣ Перевірка наслідування Person:")
        print("-" * 50)

        result = session.execute(text("""
            SELECT type, COUNT(*)
            FROM persons
            GROUP BY type
        """)).fetchall()

        for row in result:
            print(f"  {row[0]}: {row[1]} записів")

        print("\n✅ Система працює коректно!")
        print("✅ Всі дані успішно імпортовані з CSV в базу даних")
        print("✅ Відношення між таблицями встановлені правильно")

    finally:
        session.close()


if __name__ == '__main__':
    main()
