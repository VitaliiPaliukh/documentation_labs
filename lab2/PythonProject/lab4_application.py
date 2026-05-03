"""Lab 4 application bootstrap."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from lab4_dataset_reader import CsvFileReader, SocrataDatasetFetcher
from lab4_factory import create_storage_strategy


class Lab4Application:
    """Coordinates dataset download, reading, and storage."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config(self.config_path)

        dataset_config = self.config["dataset"]
        self.fetcher = SocrataDatasetFetcher(
            source_url=str(dataset_config["source_url"]),
            download_limit=int(dataset_config.get("download_limit", 1000)),
            page_size=int(dataset_config.get("page_size", 200)),
            timeout_seconds=int(dataset_config.get("timeout_seconds", 30)),
        )
        self.reader = CsvFileReader()
        self.strategy = create_storage_strategy(self.config["strategy"])

    @staticmethod
    def _load_config(config_path: Path) -> Dict[str, Any]:
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)

    def run(self) -> None:
        dataset_config = self.config["dataset"]
        output_file = str(dataset_config["output_file"])

        print("=== Lab 4: Strategy-based export ===")
        print(f"Downloading dataset from {dataset_config['source_url']} ...")
        downloaded_file = self.fetcher.fetch_to_csv(output_file)
        print(f"Saved dataset into local file: {downloaded_file}")

        rows = self.reader.read_rows(downloaded_file)
        print(f"Loaded {len(rows)} rows from the local CSV file")

        self.strategy.store(rows)
        print("Lab 4 finished successfully")

