# Dental Clinic Management System - Lab 2

Трирівнева серверна аплікація для управління стоматологічною клінікою.

## Архітектура

### 1. Рівень доступу до даних (Data Access Layer)
- **Інтерфейси**: `data_access_interfaces.py`
  - ICSVReader - читання CSV файлів
  - IPatientRepository, IDoctorRepository, IAppointmentRepository, ITreatmentPlanRepository, IDentalServiceRepository
  - IUnitOfWork - патерн Unit of Work

- **Імплементація**: `data_access_implementation.py`
  - SQLAlchemy ORM для роботи з базою даних
  - Конкретні реалізації репозиторіїв
  - DatabaseContext для управління з'єднаннями

### 2. Рівень бізнес-логіки (Business Logic Layer)
- **Файл**: `business_logic.py`
- **Сервіси**:
  - DataImportService - імпорт даних з CSV
  - PatientManagementService - управління пацієнтами
  - AppointmentManagementService - управління записами

### 3. Презентаційний рівень (Presentation Layer)
- **Файл**: `presentation_interfaces.py`
- Інтерфейси без імплементації (для майбутнього розширення)

## Моделі даних (models.py)
- Person (базовий клас)
  - Patient - пацієнти
  - Doctor - лікарі
- Appointment - записи на прийом
- TreatmentPlan - плани лікування
- DentalService (базовий клас)
  - XRayService - рентген послуги
  - SurgeryService - хірургічні послуги

## Інверсія управління та впровадження залежностей
Реалізовано через `DependencyContainer` у `main.py`:
- Бізнес-логіка використовує інтерфейси, а не конкретні класи
- Всі залежності ін'єктуються через конструктори
- Легко замінювати імплементації для тестування

## Використання

### 1. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 2. Генерація CSV файлу з даними (1000+ записів)
```bash
python csv_generator.py
```

Або з кастомною кількістю записів:
```bash
python csv_generator.py 2000
```

### 3. Запуск імпорту даних у базу
```bash
python main.py
```

## Структура CSV файлу
Всі дані зберігаються в одному файлі `dental_data.csv` з наступними полями:
- patient_name, patient_phone, patient_insurance
- doctor_name, doctor_phone, doctor_license, doctor_specialization
- appointment_date, appointment_status
- diagnosis, total_cost
- service_name, service_price, service_type, service_attr1, service_attr2

## База даних
SQLite база даних створюється автоматично: `dental_clinic.db`

## Особливості реалізації
- ✅ Трирівнева архітектура
- ✅ Інтерфейси для зв'язку між рівнями
- ✅ Інверсія управління (IoC)
- ✅ Впровадження залежностей (DI)
- ✅ ORM (SQLAlchemy)
- ✅ Читання з CSV
- ✅ Всі дані в одному файлі
- ✅ 1000+ записів
- ✅ Окремий модуль генерації даних
