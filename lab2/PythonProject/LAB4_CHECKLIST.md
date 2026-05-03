# ✅ LAB 4 — ГОТОВО ДО ЗАХИСТУ

## 📋 Чекліст (все виконано)

### Вимога 1: Завантажити датасет
- ✅ **Джерело:** Socrata (NYC Open Data - Fire Prevention Inspections)
- ✅ **Формат:** CSV
- ✅ **Зберігання:** Один локальний файл (`lab4_output/ssq6-fkht.csv`)
- ✅ **Обсяг:** 1000+ рядків
- **Файли:** `lab4_dataset_reader.py` - `SocrataDatasetFetcher`

### Вимога 2: Паттерн Strategy для різних сховищ
- ✅ **4 стратегії:** console, file, redis, kafka
- ✅ **Реалізація:** `lab4_strategies.py`
  - `ConsoleStorageStrategy` — вивід у консоль
  - `FileStorageStrategy` — запис у JSONL
  - `RedisStorageStrategy` — списки JSON
  - `KafkaStorageStrategy` — messages JSON
- ✅ **Вибір стратегії:** `lab4_factory.py`

### Вимога 3: Відділення кодів
- ✅ **Завантаження:** `lab4_dataset_reader.py` → CSV
- ✅ **Парсинг:** `CsvFileReader` → List[Dict]
- ✅ **Вивід:** `lab4_strategies.py` (незалежний від завантаження)
- ✅ **Координація:** `lab4_application.py`

### Вимога 4: Конфіг без змін коду
- ✅ **Конфіг:** `lab4_config.json`
- ✅ **Змінювати:** поле `strategy.name`
  ```json
  "strategy": { "name": "console" }
  // zmini na: redis, kafka, file
  ```
- ✅ **Код:** жодних змін в Python-файлах

### Вимога 5: Інструменти для демонстрації
- ✅ **Docker:** Redis, Kafka, Zookeeper, Kafka UI
- ✅ **Redis GUI:** RedisInsight (підключена до localhost:6379)
- ✅ **Kafka GUI:** Kafka UI (http://localhost:8080)
- ✅ **CLI перевірки:** `check_redis.py`, `check_kafka.py`

---

## 🚀 Команди для демонстрації

### Швидкий demo (все в одній команді)
```powershell
python lab4_demo.py
```

### Крок за кроком

**1. Перевірити Docker:**
```powershell
docker compose ps
```

**2. Подивитись CSV:**
```powershell
Get-Content .\lab4_output\ssq6-fkht.csv -TotalCount 11
```

**3. Запустити вивід в обидва (Redis + Kafka):**
```powershell
python run_lab4_both.py --config lab4_config.json --limit 100
```

**4. Перевірити Redis:**
```powershell
python check_redis.py lab4:fire-prevention-inspections
# або: RedisInsight (GUI) — вже відкритий
```

**5. Перевірити Kafka:**
```powershell
python check_kafka.py lab4.fire-prevention-inspections
# або: http://localhost:8080 (Kafka UI)
```

---

## 📝 Текст для викладача (готовий)

> "В Lab 4 я реалізував паттерн Strategy для експорту датасету.
> 
> Процес:
> 1. Завантажую дані з Socrata API — більш ніж 1000 записів
> 2. Зберігаю у **один** локальний CSV-файл
> 3. Читаю CSV як список словників (парсинг)
> 4. Маю 4 незалежні **стратегії** виводу:
>    - console — preview у консоль
>    - file — JSON Lines файл
>    - redis — Redis-список
>    - kafka — Kafka messages
> 
> Вибір стратегії робиться **тільки через конфіг** (`lab4_config.json`), без змін в коді.
> 
> Ось демонстрація: одна й та сама 100 записів одночасно в Redis і Kafka. Для перегляду використовую стандартні інструменти — RedisInsight для Redis (тут видно 1000+ записів), Kafka UI для Kafka (на порту 8080)."

---

## 📁 Структура Lab 4

```
PythonProject/
├── run_lab4.py                 # основний runner (одна стратегія)
├── run_lab4_both.py            # runner для Redis + Kafka одночасно
├── lab4_application.py         # координатор (download → read → store)
├── lab4_dataset_reader.py      # Socrata fetcher + CSV reader
├── lab4_strategies.py          # 4 стратегії (console, file, redis, kafka)
├── lab4_factory.py             # вибір стратегії з конфіга
├── lab4_config.json            # конфіг (змінюй strategy.name)
├── check_redis.py              # CLI для перегляду Redis
├── check_kafka.py              # CLI для перегляду Kafka
├── docker-compose.yml          # Redis, Kafka, Zookeeper, Kafka UI
├── LAB4_DEMO.md                # детальні поради для демонстрації
├── lab4_demo.py                # автоматичний demo script
└── lab4_output/
    ├── ssq6-fkht.csv           # завантажений датасет
    └── ssq6-fkht.jsonl         # вивід (якщо strategy=file)
```

---

## ✨ Висновок

**Все готово:**
- ✅ Код працює і протестований
- ✅ Docker контейнери піднялись і мають дані (RedisInsight + Kafka UI)
- ✅ Demo-скрипти готові
- ✅ Документація повна
- ✅ Жодних змін коду для переключення сховища — тільки конфіг

**Час демонстрації:** ~5 хвилин

**Готов до захисту! 🎓**

