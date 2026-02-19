from config import BASE_URL, CATEGORIES
from infrastructure.http_client import HttpClient
from application.scraper import SparkfunScraper
from infrastructure.repositories.csv_repository import save


def main():

    client = HttpClient()
    scraper = SparkfunScraper(client)

    products = scraper.scrape(BASE_URL, CATEGORIES)

    save(products, "sparkfun_products.csv")


if __name__ == "__main__":
    main()
