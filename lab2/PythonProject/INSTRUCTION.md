# 📖 ІНСТРУКЦІЯ ДЛЯ ЗАПУСКУ ТА ДЕМОНСТРАЦІЇ

## 🎯 Покрокова інструкція для показу викладачу

---

## Крок 1: Підготовка середовища

### Перейти в папку проєкту
```bash
# У PowerShell або CMD
cd C:\Users\vitalik\Desktop\documentation\lab2\PythonProject
```

### Створити та активувати віртуальне середовище
```bash
# Створити venv
python -m venv venv

# Активувати (PowerShell)
venv\Scripts\Activate.ps1

# Або активувати (CMD)
venv\Scripts\activate.bat

# Встановити залежності
pip install -r requirements.txt
```

---

## Крок 2: Генерація CSV файлу з даними

```bash
# Запуск генератора (створить 1000 записів)
python csv_generator.py
```

**Альтернативно**, якщо Python запускається не з venv:
```bash
venv\Scripts\python.exe csv_generator.py
```

**Що побачите:**
```
Generating 1000 records...
Generated 100 records...
Generated 200 records...
...
Generated 1000 records...
Successfully generated 1000 records in dental_data.csv
```

**Можна згенерувати більше записів:**
```bash
python csv_generator.py 2000    # створить 2000 записів
```

---

## Крок 3: Імпорт даних у базу

```bash
# Запуск головної програми
python main.py
```

**Альтернативно:**
```bash
venv\Scripts\python.exe main.py
```

**Що побачите:**
```
=== Dental Clinic Management System ===

Importing data from dental_data.csv...
Successfully imported 1000 records from CSV

=== Database Statistics ===
Total Patients: 100
Total Appointments: 1000

Sample Patient: [Ім'я пацієнта], Phone: +380...
Sample Appointment: 2025-03-26 15:45:00, Status: SCHEDULED

=== Data import completed successfully ===
```

---

## Крок 4: Перевірка результатів

```bash
# Запуск демонстраційного скрипта
python test_demo_simple.py
```

**Альтернативно:**
```bash
venv\Scripts\python.exe test_demo_simple.py
```

**Що побачите:**
```
=== VERIFICATION OF SYSTEM ===

[1] Database Statistics:
--------------------------------------------------
Patients: 100
Doctors: 10
Appointments: 1000
Treatment Plans: 1000
Services (total): 11
  - X-Ray services: 5
  - Surgery services: 6

[2] Sample Patient:
...

[OK] System works correctly!
[OK] All data successfully imported from CSV to database
[OK] Relationships between tables are set correctly
[OK] ORM inheritance (Table-per-Type) works correctly
```

---

## 🎬 СЦЕНАРІЙ ДЕМОНСТРАЦІЇ ВИКЛАДАЧУ

### 1️⃣ Показ структури проєкту (30 сек)

```bash
# Показати файли проєкту
dir
```

**Пояснити:**
- `models.py` - ORM моделі (відповідає діаграмі класів з Лаб 1)
- `data_access_interfaces.py` - **ІНТЕРФЕЙСИ** рівня доступу до даних
- `data_access_implementation.py` - **РЕАЛІЗАЦІЇ** інтерфейсів
- `business_logic.py` - бізнес-логіка (використовує **тільки інтерфейси**)
- `presentation_interfaces.py` - інтерфейси презентаційного рівня
- `main.py` - **DependencyContainer** (IoC/DI)
- `csv_generator.py` - генератор даних

---

### 2️⃣ Показ трирівневої архітектури (1 хв)

**Відкрити в IDE або показати в командному рядку:**

```bash
# Показати інтерфейси
type data_access_interfaces.py | more
```

**Пояснити:**
> "Це рівень доступу до даних. Тут я створив інтерфейси для кожної сутності:
> IPatientRepository, IDoctorRepository, ICSVReader тощо."

```bash
# Показати бізнес-логіку
type business_logic.py | more
```

**Пояснити (показати на код):**
> "Дивіться, клас DataImportService приймає в конструкторі **ІНТЕРФЕЙСИ**,
> а не конкретні класи. Це і є Dependency Injection."

```python
def __init__(
    self,
    csv_reader: ICSVReader,              # ← Інтерфейс!
    patient_repo: IPatientRepository,    # ← Інтерфейс!
    ...
):
```

---

### 3️⃣ Показ IoC/DI контейнера (1 хв)

```bash
# Показати main.py
type main.py | more
```

**Пояснити (показати на DependencyContainer):**
> "Ось контейнер інверсії управління. Він створює всі об'єкти
> та впроваджує залежності через конструктори. Бізнес-логіка не знає,
> які саме реалізації вона отримує - тільки інтерфейси."

---

### 4️⃣ Демонстрація генерації CSV (30 сек)

```bash
# Видалити старий файл (для чистоти)
del dental_data.csv

# Згенерувати новий
python csv_generator.py
```

**Показати файл:**
```bash
# Перші 5 рядків
type dental_data.csv | more
```

**Підрахувати кількість рядків:**
```bash
# PowerShell
(Get-Content dental_data.csv).Count - 1
```

**Пояснити:**
> "Всі дані (пацієнти, лікарі, записи, діагнози, послуги) зберігаються
> в **одному файлі**. Файл містить 1000+ записів."

---

### 5️⃣ Демонстрація імпорту в БД (1 хв)

```bash
# Видалити стару БД (для чистоти)
del dental_clinic.db

# Запустити імпорт
python main.py
```

**Пояснити, що відбувається:**
> "Зараз система:
> 1. Читає CSV через ICSVReader
> 2. DataImportService обробляє дані
> 3. Перевіряє дублікати (пацієнти, лікарі, послуги)
> 4. Створює об'єкти ORM
> 5. Встановлює зв'язки між таблицями
> 6. Зберігає все в БД через repositories"

---

### 6️⃣ Перевірка результатів (1 хв)

```bash
# Запустити демо
python test_demo_simple.py
```

**Пояснити результат:**
> "Дивіться:
> - 100 унікальних пацієнтів
> - 10 лікарів
> - 1000 записів на прийом
> - Працює наслідування (Person → Patient/Doctor)
> - Працюють всі зв'язки (1:N, N:1, 1:1, N:M)"

---

### 7️⃣ Показ ORM моделей (1 хв)

```bash
# Показати models.py
type models.py | more
```

**Пояснити важливі моменти:**

1. **Наслідування (Table-per-Type):**
```python
class Person(Base):
    # базова таблиця
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person'
    }

class Patient(Person):
    # окрема таблиця для Patient
    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }
```

2. **Відношення:**
```python
# 1:N
appointments = relationship("Appointment", back_populates="patient")

# N:M
services = relationship("DentalService",
                       secondary=treatment_service_association)
```

---

### 8️⃣ Показ структури БД (опціонально, 1 хв)

**Якщо викладач питає про таблиці:**

```bash
# Встановити sqlite3 (якщо немає)
# Або використати Python:
python -c "from data_access_implementation import DatabaseContext; from config import DATABASE_URL; from sqlalchemy import inspect; ctx = DatabaseContext(DATABASE_URL); inspector = inspect(ctx.engine); tables = inspector.get_table_names(); print('\n'.join(sorted(tables)))"
```

**Результат:**
```
appointments
dental_services
doctors
patients
persons
surgery_services
treatment_plans
treatment_service
xray_services
```

**Пояснити:**
> "9 таблиць:
> - persons (базова для Patient/Doctor)
> - patients, doctors (окремі таблиці для спеціалізацій)
> - dental_services (базова для послуг)
> - xray_services, surgery_services (спеціалізації послуг)
> - appointments, treatment_plans
> - treatment_service (Many-to-Many зв'язок)"

---

## 🎯 ШВИДКИЙ ЗАПУСК (для повторної демонстрації)

```bash
# 1. Очистити старі дані
del dental_data.csv
del dental_clinic.db

# 2. Згенерувати нові дані
python csv_generator.py

# 3. Імпортувати в БД
python main.py

# 4. Перевірити
python test_demo_simple.py
```

**Час виконання:** ~10-15 секунд

---

## ❓ ВІДПОВІДІ НА МОЖЛИВІ ПИТАННЯ ВИКЛАДАЧА

### Q: Де реалізовано IoC/DI?
**A:** Відкрити `main.py`, показати `DependencyContainer` (рядки 10-48)

### Q: Як бізнес-логіка використовує інтерфейси?
**A:** Відкрити `business_logic.py`, показати конструктор `DataImportService` (рядки 18-26)

### Q: Чому всі дані в одному файлі?
**A:** Показати `dental_data.csv` - кожен рядок містить пацієнта, лікаря, запис, діагноз і послугу

### Q: Як уникаєте дублікатів при імпорті?
**A:** Показати `business_logic.py`, метод `import_from_csv` (рядки 38-39):
```python
patients_cache = {}  # кешування створених пацієнтів
if patient_key not in patients_cache:
    # створити нового
else:
    # використати існуючого
```

### Q: Як працює наслідування в ORM?
**A:** Показати `models.py`, класи Person/Patient/Doctor з `polymorphic_identity`

### Q: Чи можна легко замінити CSV на XML?
**A:** Так! Створити клас `XMLReader(ICSVReader)` та в контейнері замінити:
```python
self.csv_reader = XMLReader()  # замість CSVReader()
```

### Q: Де презентаційний рівень?
**A:** Показати `presentation_interfaces.py` - тільки інтерфейси, без логіки

---

## 🔧 УСУНЕННЯ ПРОБЛЕМ

### Проблема: "ModuleNotFoundError: No module named 'sqlalchemy'"
**Рішення:**
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Проблема: Кирилиця відображається некоректно
**Рішення:** Використовувати `test_demo_simple.py` замість `test_demo.py`

### Проблема: "File not found: dental_data.csv"
**Рішення:**
```bash
python csv_generator.py
```

---

## 📊 ЩО ПОКАЗАТИ В ДОКУМЕНТАЦІЇ

Якщо викладач хоче переглянути документацію:

1. **README.md** - загальний опис проєкту
2. **ARCHITECTURE_EXPLANATION.md** - детальне пояснення архітектури
3. **HOW_IOC_DI_WORKS.md** - пояснення IoC/DI з прикладами
4. **CHECKLIST.md** - перевірка всіх вимог завдання
5. **RESULTS.md** - результати виконання

---

## ⏱️ ОРІЄНТОВНИЙ ЧАС ДЕМОНСТРАЦІЇ

- **Швидка демо (3-5 хв):** Кроки 4, 5, 6
- **Повна демо (10-12 хв):** Всі кроки 1-8
- **З питаннями (15-20 хв):** Всі кроки + відповіді на питання

---

## 🎓 КЛЮЧОВІ МОМЕНТИ ДЛЯ НАГОЛОШЕННЯ

1. ✅ **Трирівнева архітектура** - показати 3 файли (interfaces, implementation, business_logic)
2. ✅ **Інтерфейси між рівнями** - показати параметри конструктора
3. ✅ **IoC/DI** - показати DependencyContainer
4. ✅ **ORM** - показати models.py з наслідуванням
5. ✅ **1000+ рядків в 1 файлі** - показати CSV і підрахунок
6. ✅ **Логіка імпорту** - пояснити кешування та зв'язки

---

**Успіхів на захисті! 🚀**
