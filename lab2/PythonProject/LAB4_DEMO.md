# Lab 4 — Strategy Pattern для експорту датасету

## ✅ Що реалізовано

### 1. Завантаження датасету
- **Джерело:** NYC Open Data — Bureau of Fire Prevention Inspections Historical (`ssq6-fkht`)
- **Метод:** Socrata API з посторінковою завантажень
- **Зберігання:** Один локальний CSV-файл (`lab4_output/ssq6-fkht.csv`)
- **Обсяг:** 1000+ рядків за замовчуванням

### 2. Парсинг даних
- CSV читається як список словників (dict[str, Any])
- Кожен рядок — це набір полів (колонки) датасету

### 3. Паттерн Strategy
Чотири стратегії виводу без змін в основному коді:
- **Console** — print у консоль (preview 10 рядків)
- **File** — запис у JSON Lines (`lab4_output/*.jsonl`)
- **Redis** — зберігання в Redis-списку (JSON-рядки)
- **Kafka** — відправка повідомлень у topic (JSON)

### 4. Конфігурація
Файл `lab4_config.json` визначає:
```json
{
  "dataset": {
    "source_url": "https://data.cityofnewyork.us/resource/ssq6-fkht.csv",
    "download_limit": 1000,
    "output_file": "lab4_output/ssq6-fkht.csv"
  },
  "strategy": {
    "name": "console",  // ← змінити на: redis, kafka, file
    "redis": { ... },
    "kafka": { ... }
  }
}
```

### 5. Інструменти для перегляду
- **Redis:** RedisInsight (графічний клієнт)
- **Kafka:** Kafka UI (веб-інтерфейс, http://localhost:8080)
- **CSV:** Локальний файл або Excel
- **JSONL:** Текстовий редактор

## 🚀 Готові команди для демонстрації

### Запуск в консоль
```bash
python run_lab4.py --config lab4_config.json
```

### Запуск в обидва сховища одночасно (Redis + Kafka)
```bash
python run_lab4_both.py --config lab4_config.json --limit 500
```

### Перегляд результатів
```bash
# CSV
Get-Content .\lab4_output\ssq6-fkht.csv -TotalCount 11

# Redis (CLI)
python check_redis.py lab4:fire-prevention-inspections

# Kafka (CLI)
python check_kafka.py lab4.fire-prevention-inspections

# Redis (GUI)
# Відкрити RedisInsight, підключено до localhost:6379

# Kafka (GUI)
# Відкрити http://localhost:8080 (Kafka UI)
```

## 📋 Сценарій для захисту (5 хвилин)

**Крок 1 — Показати Docker контейнери**
```powershell
docker compose ps
```
Показати: zookeeper, kafka, redis, kafka-ui в UP статусі.

**Крок 2 — Показати локальний CSV**
```powershell
Get-Content .\lab4_output\ssq6-fkht.csv -TotalCount 11
```
«Ось дані скачані з Socrata в один файл, як вимагалось.»

**Крок 3 — Запустити процес**
```powershell
python run_lab4_both.py --config lab4_config.json --limit 100
```
Видно вивід: download → save → load → store в Redis та Kafka.

**Крок 4 — Показати результати**

**Redis:**
```powershell
python check_redis.py lab4:fire-prevention-inspections
```
Або RedisInsight (вже відкритий).

**Kafka:**
Відкрити в браузері: http://localhost:8080
Показати topic `lab4.fire-prevention-inspections` і messages.

## 📝 Текст для викладача

> "У Lab 4 я реалізував паттерн Strategy. Програма:
> 1. Завантажує датасет з Socrata API в один локальний CSV
> 2. Читає CSV як список рядків (парсинг)
> 3. Має чотири стратегії виводу: console, file, Redis, Kafka
> 4. Стратегія вибирається через конфіг, без змін коду
> 
> Ось демонстрація: одна й та сама 100 записів одночасно в Redis (як список JSON) і в Kafka (як messages). Для перегляду використовую стандартні інструменти — RedisInsight для Redis, Kafka UI для Kafka."

## 📁 Файли Lab 4

- `run_lab4.py` — основний runner (одна стратегія)
- `run_lab4_both.py` — runner для обох Redis + Kafka
- `lab4_config.json` — конфіг (змінювати `strategy.name`)
- `lab4_dataset_reader.py` — завантаження та парсинг
- `lab4_strategies.py` — реалізація всіх стратегій
- `lab4_factory.py` — вибір стратегії з конфіга
- `lab4_application.py` — координатор
- `check_redis.py` — перегляд Redis
- `check_kafka.py` — перегляд Kafka
- `docker-compose.yml` — Redis, Kafka, Zookeeper, Kafka UI

## ✅ Вимоги завдання (все виконано)

- ✅ Вичитати дані з датасету
- ✅ Записати в один файл
- ✅ Паттерн Strategy для різних сховищ
- ✅ Відділення коду завантаження від коду виводу
- ✅ Конфіг без змін основного коду
- ✅ Мінімальні/нульові зміни для переключення сховища

