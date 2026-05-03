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

## Lab 3 - MVC Web Application

### Основна сутність
- `Patient` (пацієнт) - головна сутність для CRUD у веб-інтерфейсі.

### MVC структура
- **Model**: ORM-моделі в `models.py` + бізнес-сервіси в `business_logic.py`.
- **Controller**: `web/controllers/patient_controller.py`.
- **View**: Jinja2-шаблони в `web/templates/`.

### Що реалізовано
- Перегляд списку пацієнтів (`GET /patients/`)
- Перегляд деталей пацієнта (`GET /patients/<id>`)
- Додавання пацієнта (`GET/POST /patients/create`)
- Редагування пацієнта (`GET/POST /patients/<id>/edit`)
- Видалення пацієнта (`POST /patients/<id>/delete`)
- Візуалізація записів на прийом (`GET /appointments`)

Важливо: контролери не працюють напряму з репозиторіями, а використовують класи бізнес-логіки через DI контейнер.

### Запуск веб-додатку
```bash
python run_web.py
```

Після запуску відкрийте `http://127.0.0.1:5000`.

## Lab 4 - Strategy pattern

### Призначення
- Завантаження датасету `ssq6-fkht` з NYC Open Data
- Збереження отриманих даних у локальний CSV-файл
- Вивід даних через паттерн `Strategy`

### Де лежить код
Усі файли для Lab 4 лежать у корені проєкту:
- `run_lab4.py`
- `lab4_application.py`
- `lab4_dataset_reader.py`
- `lab4_factory.py`
- `lab4_strategies.py`
- `lab4_config.json`

### Запуск
```bash
python run_lab4.py
```

### Стратегії виводу (паттерн Strategy)
4 варіанти без змін основного коду — змінюєш тільки `lab4_config.json`:
- `console`
- `file`
- `redis`
- `kafka`

### Запуск в обидва сховища (Redis + Kafka) одночасно
```bash
python run_lab4_both.py --config lab4_config.json --limit 500
```

### Додатково
Для Redis/Kafka потрібні додаткові пакети:
```bash
pip install redis kafka-python
```

### Docker (Redis, Kafka, Zookeeper, Kafka UI)
```bash
docker compose up -d
```
- Redis: `localhost:6379` (RedisInsight)
- Kafka: `localhost:9092` (Kafka UI на `http://localhost:8080`)
- Zookeeper: `localhost:2181`

### Демонстрація результатів
- **CSV:** `Get-Content .\lab4_output\ssq6-fkht.csv -TotalCount 11`
- **Redis:** `python check_redis.py` або RedisInsight
- **Kafka:** `python check_kafka.py` або http://localhost:8080

### Більше інформації
Див. `LAB4_DEMO.md` для готового сценарію демонстрації викладачу.

