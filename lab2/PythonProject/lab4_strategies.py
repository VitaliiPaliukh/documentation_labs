"""Output strategies for Lab 4."""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Mapping, Sequence


class StorageStrategy(ABC):
    """Base strategy for writing rows into a storage backend."""

    @abstractmethod
    def store(self, records: Sequence[Mapping[str, Any]]) -> None:
        """Store a batch of records."""
        raise NotImplementedError


class ConsoleStorageStrategy(StorageStrategy):
    """Prints rows to console."""

    def __init__(self, preview_rows: int = 10):
        self.preview_rows = max(0, preview_rows)

    def store(self, records: Sequence[Mapping[str, Any]]) -> None:
        total = len(records)
        print(f"[console] Received {total} rows from dataset")
        preview = records if self.preview_rows == 0 else records[: self.preview_rows]

        for index, record in enumerate(preview, start=1):
            print(f"[console] Row {index}: {json.dumps(dict(record), ensure_ascii=False)}")

        if self.preview_rows and total > self.preview_rows:
            print(f"[console] ... {total - self.preview_rows} more rows omitted from preview")


class FileStorageStrategy(StorageStrategy):
    """Writes rows into a JSON Lines file."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)

    def store(self, records: Sequence[Mapping[str, Any]]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", encoding="utf-8") as file_handle:
            for record in records:
                file_handle.write(json.dumps(dict(record), ensure_ascii=False))
                file_handle.write("\n")
        print(f"[file] Wrote {len(records)} rows to {self.output_path}")


class RedisStorageStrategy(StorageStrategy):
    """Stores rows in Redis as JSON strings in a list."""

    def __init__(self, host: str, port: int, db: int, key: str):
        self.host = host
        self.port = port
        self.db = db
        self.key = key

    def store(self, records: Sequence[Mapping[str, Any]]) -> None:
        try:
            import redis  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Redis support requires the 'redis' package. Install it or switch strategy to console/file."
            ) from exc

        client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        client.delete(self.key)
        payloads = [json.dumps(dict(record), ensure_ascii=False) for record in records]
        if payloads:
            client.rpush(self.key, *payloads)
        print(f"[redis] Stored {len(payloads)} rows in Redis list '{self.key}'")


class KafkaStorageStrategy(StorageStrategy):
    """Sends rows to Kafka as JSON messages."""

    def __init__(self, bootstrap_servers: Sequence[str], topic: str):
        self.bootstrap_servers = list(bootstrap_servers)
        self.topic = topic

    def store(self, records: Sequence[Mapping[str, Any]]) -> None:
        try:
            from kafka import KafkaProducer  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Kafka support requires the 'kafka-python' package. Install it or switch strategy to console/file."
            ) from exc

        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: json.dumps(value, ensure_ascii=False).encode("utf-8"),
        )

        sent = 0
        try:
            for record in records:
                producer.send(self.topic, value=dict(record))
                sent += 1
            producer.flush()
        finally:
            producer.close()

        print(f"[kafka] Sent {sent} rows to topic '{self.topic}'")

