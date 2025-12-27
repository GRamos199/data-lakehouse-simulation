"""
Sample data generator - creates sample CSV data for demonstration.
"""

import csv
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import RAW_CSV_PATH, TIMEZONE  # noqa: E402


def generate_sample_csv():
    """Generate sample historical weather CSV file."""

    output_file = RAW_CSV_PATH / "sample_historical.csv"

    cities = ["New York", "Los Angeles", "London", "Tokyo", "Sydney"]
    conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Partly Cloudy"]

    rows = []
    base_date = datetime.now(TIMEZONE) - timedelta(days=30)

    for day in range(30):
        current_date = base_date + timedelta(days=day)
        for city in cities:
            row = {
                "date": current_date.strftime("%Y-%m-%d"),
                "city": city,
                "temperature_high": round(random.uniform(10, 35), 1),
                "temperature_low": round(random.uniform(-5, 25), 1),
                "humidity": random.randint(30, 95),
                "precipitation_mm": round(random.uniform(0, 50), 1),
                "condition": random.choice(conditions),
                "wind_speed_kmh": round(random.uniform(5, 40), 1),
            }
            rows.append(row)

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "date",
            "city",
            "temperature_high",
            "temperature_low",
            "humidity",
            "precipitation_mm",
            "condition",
            "wind_speed_kmh",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Sample CSV created: {output_file}")
    print(f"  - {len(rows)} records")
    print(f"  - {len(cities)} cities")
    print("  - 30 days of data")


if __name__ == "__main__":
    generate_sample_csv()
