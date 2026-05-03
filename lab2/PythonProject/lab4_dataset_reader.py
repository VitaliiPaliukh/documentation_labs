"""Dataset reader utilities for Lab 4."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SocrataDatasetFetcher:
    """Downloads the Socrata dataset into a single local CSV file."""

    def __init__(self, source_url: str, download_limit: int = 1000, page_size: int = 200, timeout_seconds: int = 30):
        self.source_url = source_url
        self.download_limit = max(1, download_limit)
        self.page_size = max(1, page_size)
        self.timeout_seconds = timeout_seconds

    def _build_request_url(self, offset: int, limit: int) -> str:
        query = urlencode({"$limit": limit, "$offset": offset})
        separator = "&" if "?" in self.source_url else "?"
        return f"{self.source_url}{separator}{query}"

    def fetch_to_csv(self, output_file: str) -> str:
        """Fetch rows from the dataset and write them into one CSV file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        fieldnames: List[str] | None = None

        with output_path.open("w", newline="", encoding="utf-8") as file_handle:
            writer: csv.DictWriter | None = None

            while downloaded < self.download_limit:
                current_limit = min(self.page_size, self.download_limit - downloaded)
                request_url = self._build_request_url(downloaded, current_limit)
                request = Request(request_url, headers={"Accept": "text/csv"})

                rows_written = 0
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    text_stream = (line.decode("utf-8") for line in response)
                    reader = csv.DictReader(text_stream)

                    if fieldnames is None:
                        fieldnames = list(reader.fieldnames or [])
                        if not fieldnames:
                            raise RuntimeError("The dataset response does not contain CSV headers.")
                        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
                        writer.writeheader()

                    for row in reader:
                        assert writer is not None
                        writer.writerow(row)
                        rows_written += 1
                        downloaded += 1
                        if downloaded >= self.download_limit:
                            break

                if rows_written == 0:
                    break

        return str(output_path)


class CsvFileReader:
    """Reads rows from the local CSV file that was downloaded from Socrata."""

    def read_rows(self, file_path: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        with open(file_path, "r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                rows.append(dict(row))
        return rows

