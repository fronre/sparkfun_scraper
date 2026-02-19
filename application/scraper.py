import time
from bs4 import BeautifulSoup
from domain.product import Product


class SparkfunScraper:

    def __init__(self, http_client):
        self.http = http_client

    def scrape(self, base_url, categories):

        MAX_PRODUCTS = 2000
        MAX_PAGES = 25

        products_list = []
        seen_links = set()
        product_counter = 1

        for category_name, category_path in categories.items():

            print(f"\nStarting category: {category_name}")
            page = 1

            while True:

                # 🔥 حماية من infinite pagination
                if page > MAX_PAGES:
                    print("Reached max pages for this category.")
                    break

                print(f"Scraping {category_name} - Page {page}...")

                url = f"{base_url}{category_path}?p={page}&product_list_limit=48"

                try:
                    response = self.http.get(url)
                except:
                    print("Connection error, skipping page...")
                    page += 1
                    continue

                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                products = soup.select("li.product-item")

                real_products = [
                    p for p in products
                    if p.select_one("a.product-item-link")
                ]

                if not real_products:
                    break

                for product in real_products:

                    name_tag = product.select_one("a.product-item-link")
                    if not name_tag or not name_tag.has_attr("href"):
                        continue

                    link = name_tag["href"]

                    if link in seen_links:
                        continue

                    seen_links.add(link)

                    price_tag = product.select_one("span.price")
                    stock_tag = product.select_one("div.stock span")

                    name = name_tag.text.strip()
                    price = price_tag.text.strip() if price_tag else "N/A"
                    stock = stock_tag.text.strip() if stock_tag else "Unknown"

                    products_list.append(
                        Product(
                            id=product_counter,
                            name=name,
                            price=price,
                            stock=stock,
                            link=link,
                            category=category_name
                        )
                    )

                    product_counter += 1

                    # 🔥 نوقف عند 2000 منتج
                    if len(products_list) >= MAX_PRODUCTS:
                        print(f"\nReached {MAX_PRODUCTS} products. Stopping...")
                        return products_list

                page += 1
                time.sleep(0.5)

        return products_list
