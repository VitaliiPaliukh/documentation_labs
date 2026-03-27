# Пояснення архітектури та виконання завдання

## ✅ Чек-лист виконання завдання:

### 1. ✅ Трирівнева архітектура
- **Рівень доступу до даних** (Data Access Layer)
- **Рівень бізнес-логіки** (Business Logic Layer)
- **Презентаційний рівень** (Presentation Layer)

### 2. ✅ Зв'язок через інтерфейси
- Бізнес-логіка використовує **інтерфейси**, а не конкретні класи
- Файл `data_access_interfaces.py` містить всі інтерфейси
- Файл `business_logic.py` приймає інтерфейси в конструкторах

### 3. ✅ Інверсія управління (IoC) та Dependency Injection (DI)
- `DependencyContainer` в `main.py` створює всі залежності
- Залежності передаються через конструктори (Constructor Injection)
- Легко замінювати реалізації для тестування

### 4. ✅ ORM для роботи з БД
- Використано SQLAlchemy ORM
- Моделі в `models.py` з відношеннями
- Автоматичне створення таблиць

### 5. ✅ Читання з CSV файлу
- Реалізовано `ICSVReader` інтерфейс
- Конкретна реалізація `CSVReader` в `data_access_implementation.py`

### 6. ✅ Всі дані в одному файлі
- Файл `dental_data.csv` містить всю інформацію
- Пацієнти, лікарі, записи, діагнози, послуги - все в одному CSV

### 7. ✅ Мінімум 1000 рядків
- Згенеровано рівно 1000 записів

### 8. ✅ Окремий модуль для генерації CSV
- `csv_generator.py` - запускається з командного рядка
- Можна вказати кількість записів: `python csv_generator.py 2000`

### 9. ✅ Презентаційний рівень без логіки
- Тільки інтерфейси в `presentation_interfaces.py`
- Без конкретних реалізацій

---

## 🔍 Як це працює:

### Крок 1: Генерація даних
```bash
python csv_generator.py
```
**Що відбувається:**
- Створюються випадкові пацієнти (100 унікальних)
- Створюються 10 лікарів з різними спеціалізаціями
- Генерується 1000 записів на прийом
- Для кожного запису додається діагноз та послуга (рентген або хірургія)
- Всі дані записуються в один CSV файл

### Крок 2: Імпорт в базу даних
```bash
python main.py
```

**Що відбувається покроково:**

#### 1️⃣ Ініціалізація DependencyContainer (IoC/DI)
```
main.py → DependencyContainer.__init__()
├── Створює DatabaseContext
├── Створює Session для SQLAlchemy
├── Створює всі репозиторії (через інтерфейси!)
│   ├── PatientRepository
│   ├── DoctorRepository
│   ├── AppointmentRepository
│   ├── TreatmentPlanRepository
│   └── DentalServiceRepository
└── Створює сервіси бізнес-логіки
    ├── DataImportService (отримує інтерфейси репозиторіїв!)
    ├── PatientManagementService
    └── AppointmentManagementService
```

#### 2️⃣ Читання CSV файлу
```
DataImportService.import_from_csv()
├── Викликає ICSVReader.read_csv() (інтерфейс!)
└── CSVReader читає всі 1000 рядків
```

#### 3️⃣ Обробка кожного рядка
```
Для кожного рядка CSV:
├── Перевірка: чи існує пацієнт (patients_cache)
│   ├── Якщо НІ → створити Patient через IPatientRepository
│   └── Якщо ТАК → використати існуючий
│
├── Перевірка: чи існує лікар (doctors_cache)
│   ├── Якщо НІ → створити Doctor через IDoctorRepository
│   └── Якщо ТАК → використати існуючий
│
├── Перевірка: чи існує послуга (services_cache)
│   ├── Якщо service_type == 'xray' → створити XRayService
│   ├── Якщо service_type == 'surgery' → створити SurgeryService
│   └── Зберегти через IDentalServiceRepository
│
├── Створити TreatmentPlan
│   ├── Встановити діагноз та вартість
│   ├── Додати послугу до плану (many-to-many зв'язок)
│   └── Зберегти через ITreatmentPlanRepository
│
└── Створити Appointment
    ├── Зв'язати з пацієнтом (many-to-one)
    ├── Зв'язати з лікарем (many-to-one)
    ├── Зв'язати з планом лікування (one-to-one)
    └── Зберегти через IAppointmentRepository
```

#### 4️⃣ Збереження в БД
```
UnitOfWork.commit()
└── SQLAlchemy зберігає всі об'єкти в БД
    ├── Таблиця persons (базова для Patient/Doctor)
    ├── Таблиця patients (окремі дані пацієнтів)
    ├── Таблиця doctors (окремі дані лікарів)
    ├── Таблиця appointments
    ├── Таблиця treatment_plans
    ├── Таблиця dental_services (базова)
    ├── Таблиця xray_services (спеціалізовані дані)
    ├── Таблиця surgery_services (спеціалізовані дані)
    └── Таблиця treatment_service (many-to-many)
```

---

## 🏗️ Патерни проектування:

### 1. Repository Pattern
Кожна сутність має свій репозиторій з CRUD операціями.

### 2. Unit of Work
`UnitOfWork` координує збереження змін в одній транзакції.

### 3. Dependency Injection
```python
# ❌ Погано (жорстка залежність):
class Service:
    def __init__(self):
        self.repo = PatientRepository()  # конкретний клас!

# ✅ Добре (залежність від інтерфейсу):
class Service:
    def __init__(self, repo: IPatientRepository):  # інтерфейс!
        self.repo = repo
```

### 4. Inversion of Control
Контейнер (DependencyContainer) контролює створення об'єктів, не самі класи.

---

## 📊 Структура бази даних:

### Наслідування (Table-per-Type):

**Person (базова таблиця)**
```
persons
├── id (PK)
├── full_name
├── phone
└── type (discriminator: 'patient' або 'doctor')
```

**Patient (розширює Person)**
```
patients
├── id (PK, FK → persons.id)
└── insurance_number
```

**Doctor (розширює Person)**
```
doctors
├── id (PK, FK → persons.id)
├── license_id
└── specialization
```

**DentalService (базова таблиця)**
```
dental_services
├── id (PK)
├── service_name
├── base_price
└── type (discriminator: 'xray_service' або 'surgery_service')
```

**XRayService (розширює DentalService)**
```
xray_services
├── id (PK, FK → dental_services.id)
├── image_resolution
└── radiation_dose
```

**SurgeryService (розширює DentalService)**
```
surgery_services
├── id (PK, FK → dental_services.id)
├── anesthesia_type
└── complexity_level
```

### Зв'язки:

```
Patient 1:N Appointment N:1 Doctor
Appointment 1:1 TreatmentPlan N:M DentalService
```

---

## 🎯 Чому це правильна реалізація:

### ✅ Розділення відповідальностей
- **Data Access** - тільки робота з БД та файлами
- **Business Logic** - тільки бізнес-правила та координація
- **Presentation** - тільки інтерфейси для UI (готові до розширення)

### ✅ Тестованість
Можна легко створити mock-реалізації інтерфейсів для unit-тестів:
```python
class MockPatientRepository(IPatientRepository):
    def create(self, patient):
        return patient  # без реальної БД
```

### ✅ Масштабованість
- Легко замінити SQLite на PostgreSQL
- Легко додати XML reader замість CSV
- Легко додати REST API як презентаційний рівень

### ✅ Відповідність SOLID принципам
- **S**ingle Responsibility - кожен клас має одну відповідальність
- **O**pen/Closed - відкрито для розширення, закрито для модифікації
- **L**iskov Substitution - можна замінити реалізації інтерфейсів
- **I**nterface Segregation - інтерфейси не перевантажені
- **D**ependency Inversion - залежність від абстракцій, не від реалізацій

---

## 🚀 Що далі можна додати:

1. **Презентаційний рівень**:
   - Console UI
   - Web API (Flask/FastAPI)
   - Desktop GUI (tkinter)

2. **Розширення бізнес-логіки**:
   - Валідація даних
   - Бізнес-правила (наприклад, лікар не може мати більше 10 записів на день)
   - Генерація звітів

3. **Тестування**:
   - Unit tests для сервісів
   - Integration tests для репозиторіїв
   - Mock-об'єкти для ізольованого тестування
