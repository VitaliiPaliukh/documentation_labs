"""Run Lab4 pipeline and send parsed rows to BOTH Redis and Kafka.

This helper reads the same config as `run_lab4.py` but will create both
Redis and Kafka strategies and call `store` for each, so you can host both
services and push data to both at once (handy for demo).

Usage:
    python run_lab4_both.py --config lab4_config.json --limit 5

Options:
    --config PATH    path to JSON config (default: lab4_config.json)
    --limit N        optional override for dataset.download_limit
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

try:
    from lab4_dataset_reader import SocrataDatasetFetcher, CsvFileReader
    from lab4_strategies import RedisStorageStrategy, KafkaStorageStrategy
except Exception as e:
    print("Missing local modules. Make sure you run this from project root where lab4_dataset_reader.py and lab4_strategies.py exist.")
    raise


def load_config(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='lab4_config.json')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f'Config not found: {cfg_path}')
        sys.exit(2)

    cfg = load_config(cfg_path)
    ds_cfg = cfg.get('dataset', {})
    if args.limit:
        ds_cfg['download_limit'] = int(args.limit)

    source_url = ds_cfg.get('source_url')
    output_file = ds_cfg.get('output_file')
    download_limit = int(ds_cfg.get('download_limit', 100))
    page_size = int(ds_cfg.get('page_size', 200))
    timeout_seconds = int(ds_cfg.get('timeout_seconds', 30))

    print('Downloading dataset (limit={})...'.format(download_limit))
    fetcher = SocrataDatasetFetcher(source_url, download_limit=download_limit, page_size=page_size, timeout_seconds=timeout_seconds)
    saved = fetcher.fetch_to_csv(output_file)
    print('Saved to', saved)

    reader = CsvFileReader()
    rows = reader.read_rows(saved)
    print(f'Loaded {len(rows)} rows from {saved}')

    # Prepare Redis strategy (if config present)
    redis_cfg = cfg.get('strategy', {}).get('redis', {})
    kafka_cfg = cfg.get('strategy', {}).get('kafka', {})

    # instantiate strategies only if minimal settings exist
    strategies = []
    if redis_cfg:
        try:
            strategies.append(('redis', RedisStorageStrategy(
                host=str(redis_cfg.get('host', 'localhost')),
                port=int(redis_cfg.get('port', 6379)),
                db=int(redis_cfg.get('db', 0)),
                key=str(redis_cfg.get('key', 'lab4:fire-prevention-inspections'))
            )))
        except Exception as e:
            print('Failed to create Redis strategy:', e)

    if kafka_cfg:
        try:
            strategies.append(('kafka', KafkaStorageStrategy(
                bootstrap_servers=list(kafka_cfg.get('bootstrap_servers', ['localhost:9092'])),
                topic=str(kafka_cfg.get('topic', 'lab4.fire-prevention-inspections'))
            )))
        except Exception as e:
            print('Failed to create Kafka strategy:', e)

    if not strategies:
        print('No Redis/Kafka configuration found in config. Exiting.')
        sys.exit(0)

    for name, strat in strategies:
        print(f'Calling strategy: {name} -> storing {len(rows)} rows')
        try:
            strat.store(rows)
        except Exception as e:
            print(f'Error while storing to {name}:', e)

    print('Done.')


if __name__ == '__main__':
    main()

