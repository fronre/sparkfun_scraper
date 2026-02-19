import csv
from dataclasses import asdict


def save(products, filename):

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "name", "price", "stock", "link", "category"]
        )

        writer.writeheader()

        for product in products:
            writer.writerow(asdict(product))

    print(f"\n✅ Saved {len(products)} products to {filename}")
