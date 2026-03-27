# Як працює Інверсія управління (IoC) і Впровадження залежностей (DI)

## ❌ БЕЗ IoC/DI (погано):

```python
# business_logic.py
from data_access_implementation import CSVReader, PatientRepository, DoctorRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataImportService:
    def __init__(self):
        # ❌ Сервіс САМ створює свої залежності
        engine = create_engine("sqlite:///db.db")
        session = sessionmaker(bind=engine)()

        # ❌ Жорстко прив'язані до конкретних класів
        self.csv_reader = CSVReader()
        self.patient_repo = PatientRepository(session)
        self.doctor_repo = DoctorRepository(session)

    def import_data(self, file_path):
        data = self.csv_reader.read_csv(file_path)
        # ...
```

### Проблеми:
1. ❌ Неможливо тестувати (не можна підставити mock-об'єкти)
2. ❌ Важко змінити реалізацію (наприклад, з CSV на XML)
3. ❌ Порушується принцип Dependency Inversion (залежність від конкретних класів)
4. ❌ Клас знає ЯК створювати свої залежності (не його відповідальність!)

---

## ✅ З IoC/DI (добре):

### Крок 1: Створюємо ІНТЕРФЕЙСИ

```python
# data_access_interfaces.py
from abc import ABC, abstractmethod

class ICSVReader(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict]:
        pass

class IPatientRepository(ABC):
    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        pass
```

### Крок 2: Сервіс приймає ІНТЕРФЕЙСИ в конструкторі

```python
# business_logic.py
class DataImportService:
    def __init__(
        self,
        csv_reader: ICSVReader,        # ✅ Інтерфейс, не клас!
        patient_repo: IPatientRepository,  # ✅ Інтерфейс, не клас!
        doctor_repo: IDoctorRepository     # ✅ Інтерфейс, не клас!
    ):
        # ✅ Приймаємо залежності ззовні (Dependency Injection)
        self.csv_reader = csv_reader
        self.patient_repo = patient_repo
        self.doctor_repo = doctor_repo

    def import_data(self, file_path):
        # ✅ Працюємо з інтерфейсами
        data = self.csv_reader.read_csv(file_path)
        # ...
```

### Крок 3: Створюємо РЕАЛІЗАЦІЇ інтерфейсів

```python
# data_access_implementation.py
class CSVReader(ICSVReader):
    def read_csv(self, file_path: str) -> List[Dict]:
        # Конкретна реалізація
        with open(file_path, 'r') as f:
            return list(csv.DictReader(f))

class PatientRepository(IPatientRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, patient: Patient) -> Patient:
        self.session.add(patient)
        return patient
```

### Крок 4: IoC Container створює і з'єднує все

```python
# main.py
class DependencyContainer:
    def __init__(self, connection_string: str):
        # ✅ Контейнер КОНТРОЛЮЄ створення об'єктів (Inversion of Control)

        # 1. Створюємо низькорівневі залежності
        self.db_context = DatabaseContext(connection_string)
        self.session = self.db_context.get_session()

        # 2. Створюємо реалізації інтерфейсів
        self.csv_reader = CSVReader()
        self.patient_repository = PatientRepository(self.session)
        self.doctor_repository = DoctorRepository(self.session)

        # 3. ВПРОВАДЖУЄМО (inject) залежності в сервіс
        self.data_import_service = DataImportService(
            csv_reader=self.csv_reader,           # ✅ Передаємо готові об'єкти
            patient_repo=self.patient_repository,
            doctor_repo=self.doctor_repository
        )
```

### Крок 5: Використання

```python
# main.py
def main():
    # 1. Створюємо контейнер (він створить ВСІ залежності)
    container = DependencyContainer(DATABASE_URL)

    # 2. Просто використовуємо готові сервіси
    container.data_import_service.import_from_csv("data.csv")
```

---

## 🎯 Переваги IoC/DI:

### 1️⃣ Легко тестувати

```python
# test_business_logic.py
class MockCSVReader(ICSVReader):
    def read_csv(self, file_path: str):
        # Повертаємо тестові дані без читання файлу
        return [
            {'patient_name': 'Test Patient', 'phone': '123'}
        ]

class MockPatientRepository(IPatientRepository):
    def __init__(self):
        self.patients = []

    def create(self, patient):
        self.patients.append(patient)
        return patient

# Тест
def test_import_service():
    # ✅ Підставляємо mock-об'єкти
    service = DataImportService(
        csv_reader=MockCSVReader(),
        patient_repo=MockPatientRepository(),
        doctor_repo=MockDoctorRepository()
    )

    service.import_data("fake.csv")
    # Перевіряємо результати без реальної БД!
```

### 2️⃣ Легко змінити реалізацію

```python
# Хочемо читати з XML замість CSV?
class XMLReader(ICSVReader):  # Той самий інтерфейс!
    def read_csv(self, file_path: str):
        # Читаємо XML, але повертаємо той самий формат
        return parse_xml(file_path)

# У контейнері змінюємо одну лінію:
self.csv_reader = XMLReader()  # ✅ Все інше працює без змін!
```

### 3️⃣ Легко замінити БД

```python
# Хочемо PostgreSQL замість SQLite?
class DependencyContainer:
    def __init__(self):
        # Змінюємо тільки тут:
        self.db_context = DatabaseContext("postgresql://...")
        # ✅ Вся інша логіка працює без змін!
```

---

## 📊 Діаграма залежностей:

```
main.py (DependencyContainer)
    │
    ├─ створює → DatabaseContext
    │               └─ створює → Session
    │
    ├─ створює → CSVReader (implements ICSVReader)
    │
    ├─ створює → PatientRepository (implements IPatientRepository)
    │               └─ потребує → Session
    │
    ├─ створює → DoctorRepository (implements IDoctorRepository)
    │               └─ потребує → Session
    │
    └─ створює → DataImportService
                    ├─ отримує → ICSVReader
                    ├─ отримує → IPatientRepository
                    └─ отримує → IDoctorRepository

❗ DataImportService НЕ ЗНАЄ про конкретні класи!
❗ Він знає тільки про ІНТЕРФЕЙСИ!
```

---

## 🔄 Порівняння:

| Аспект | БЕЗ IoC/DI | З IoC/DI |
|--------|-----------|----------|
| **Створення залежностей** | Клас сам створює | Контейнер створює |
| **Тип залежностей** | Конкретні класи | Інтерфейси |
| **Тестування** | Важко (потрібна реальна БД) | Легко (mock-об'єкти) |
| **Зміна реалізації** | Треба редагувати багато файлів | Змінити в контейнері |
| **SOLID принципи** | Порушуються | Дотримуються |

---

## 🎓 Теорія:

### Інверсія управління (IoC)
**"Не ти викликаєш фреймворк, фреймворк викликає тебе"**

Раніше:
- Клас сам вирішує, ЯК створювати залежності
- Клас **контролює** процес створення

З IoC:
- Зовнішній контейнер вирішує, ЯК створювати залежності
- **Контроль інвертовано** до контейнера

### Впровадження залежностей (DI)
**"Не шукай залежності, прийми їх ззовні"**

3 типи DI:
1. **Constructor Injection** (✅ використовуємо) - через конструктор
2. **Setter Injection** - через setter методи
3. **Interface Injection** - через спеціальний інтерфейс

---

## ✅ Підсумок по нашому проєкту:

1. **Інтерфейси** (`data_access_interfaces.py`):
   - Визначають ЩО потрібно робити
   - Не залежать від деталей реалізації

2. **Реалізації** (`data_access_implementation.py`):
   - Визначають ЯК робити
   - Можна легко замінити

3. **Бізнес-логіка** (`business_logic.py`):
   - Залежить тільки від ІНТЕРФЕЙСІВ
   - Не знає про конкретні реалізації

4. **Контейнер** (`main.py` - DependencyContainer):
   - Створює всі об'єкти
   - З'єднує їх разом
   - Один центр конфігурації

✅ **Це і є правильна реалізація IoC/DI!**
