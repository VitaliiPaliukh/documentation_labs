#!/usr/bin/env python3
"""Quick demo script for Lab 4 — run this to show everything working."""
import subprocess
import sys
import time

def run(cmd, desc=""):
    """Run command and print description."""
    if desc:
        print(f"\n{'='*60}")
        print(f"📍 {desc}")
        print(f"{'='*60}")
    print(f"$ {cmd}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"⚠️ Command failed with code {result.returncode}")
    time.sleep(1)
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("🚀 LAB 4 DEMO — Strategy Pattern for Dataset Export")
    print("="*60)
    
    # Step 1: Docker status
    run("docker compose ps", "Step 1: Check Docker containers (Redis, Kafka, etc.)")
    
    # Step 2: Show CSV
    run("Get-Content .\\lab4_output\\ssq6-fkht.csv -TotalCount 11", 
        "Step 2: Show downloaded CSV (first 11 lines)")
    
    # Step 3: Run demo
    run("python run_lab4_both.py --config lab4_config.json --limit 50",
        "Step 3: Run export to BOTH Redis and Kafka (50 records)")
    
    # Step 4: Check Redis
    run("python check_redis.py lab4:fire-prevention-inspections",
        "Step 4a: Verify data in Redis")
    
    # Step 5: Check Kafka
    run("python check_kafka.py lab4.fire-prevention-inspections",
        "Step 4b: Verify data in Kafka")
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("="*60)
    print("\n📊 Open these in browser for GUI:")
    print("  • Redis: RedisInsight (already open?)")
    print("  • Kafka: http://localhost:8080 (Kafka UI)")
    print("\n📖 For more info: see LAB4_DEMO.md")

if __name__ == '__main__':
    main()

