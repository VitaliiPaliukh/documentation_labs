"""Factory helpers for choosing a storage strategy from configuration."""
from __future__ import annotations

from typing import Any, Mapping

from lab4_strategies import (
    ConsoleStorageStrategy,
    FileStorageStrategy,
    KafkaStorageStrategy,
    RedisStorageStrategy,
    StorageStrategy,
)


def create_storage_strategy(strategy_config: Mapping[str, Any]) -> StorageStrategy:
    """Create a storage strategy from a config dictionary."""
    strategy_name = str(strategy_config.get("name", "console")).lower()

    if strategy_name == "console":
        console_config = strategy_config.get("console", {})
        return ConsoleStorageStrategy(preview_rows=int(console_config.get("preview_rows", 10)))

    if strategy_name == "file":
        file_config = strategy_config.get("file", {})
        return FileStorageStrategy(output_path=str(file_config.get("path", "lab4_output/output.jsonl")))

    if strategy_name == "redis":
        redis_config = strategy_config.get("redis", {})
        return RedisStorageStrategy(
            host=str(redis_config.get("host", "localhost")),
            port=int(redis_config.get("port", 6379)),
            db=int(redis_config.get("db", 0)),
            key=str(redis_config.get("key", "lab4:data")),
        )

    if strategy_name == "kafka":
        kafka_config = strategy_config.get("kafka", {})
        return KafkaStorageStrategy(
            bootstrap_servers=list(kafka_config.get("bootstrap_servers", ["localhost:9092"])),
            topic=str(kafka_config.get("topic", "lab4.data")),
        )

    raise ValueError(f"Unsupported storage strategy: {strategy_name}")

