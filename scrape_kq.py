import argparse
import itertools
import requests
from bs4 import BeautifulSoup
import time
import json
from store import Store
from product import Product


# Set up headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


def fetch_html(url):
    """Fetch HTML content from a given URL."""
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Optional sleep to prevent spamming requests
            time.sleep(0.25)
            return response.text
        else:
            print(f"Error: Received status code {
                  response.status_code} for URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for URL '{url}': {e}")
        return None


def extract_product_offers(html_content, stores, products, quantity=1):
    """Parse the HTML content to extract product offers and shipping costs."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the script tag containing the __NEXT_DATA__ JSON
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        # Extract the JSON content from the script
        json_data = json.loads(script_tag.text)

        product = Product(json_data['props']['pageProps']
                          ['productPage']['product']['name'], quantity)

        for offer in json_data['props']['pageProps']['productPage']['product']['offers']:
            store = offer['storeName']
            price = offer['price']
            price_shipping = offer['shipping']['minimumPrice']
            # price_total = offer['totalPrice']

            if stores.get(store):
                stores[store].update_shipping_price(price_shipping)
            else:
                stores[store] = Store(store, price_shipping)

            product.add_store(stores[store], price)
        products.append(product)
        return True
    else:
        print("Failed to find the __NEXT_DATA__ script in the HTML.")
        return False


def calculate_total_price(combo, products, lowest_price=float('inf')):
    """Calculates the total price for a combination of store-product selections."""
    item_price_sum = 0
    unique_stores = set()

    for i in range(len(combo)):
        store, price = products[i].stores[combo[i]]
        item_price_sum += price * products[i].quantity
        unique_stores.add(store)

        # Early exit if item_price_sum already exceeds lowest_price
        if item_price_sum >= lowest_price:
            return None

    shipping_sum = sum([store.shipping_cost for store in unique_stores])

    return item_price_sum + shipping_sum


def output_results(lowest_combo, lowest_price, products):
    """Outputs the results of the lowest price calculation."""
    # Dictionary where the key is a store and the value is a list of products
    chosen_stores = {}
    for i, j in enumerate(lowest_combo):
        store = products[i].stores[j][0]
        chosen_stores.setdefault(store, []).append(products[i])

    print(f"Lowest price: {lowest_price}")
    for store, products in chosen_stores.items():
        print("-------")
        print(f"Store: {store.name} - Shipping: {store.shipping_cost} EUR")
        for product in products:
            price = product.stores[lowest_combo[products.index(product)]][1]
            print(f"Product: {
                  product.name} - Price: {price} EUR - Quantity: {product.quantity}")


def main(urls_with_quantities):
    products = []
    stores = {}

    for (url, quantity) in urls_with_quantities:
        extract_product_offers(fetch_html(url), stores, products, quantity)

    # Create a list of the lengths of each list
    lengths = [len(product.stores) for product in products]

    # Generate all possible index combinations using itertools.product
    index_combinations = itertools.product(
        *[range(length) for length in lengths])

    lowest_price = float('inf')
    lowest_combo = None

    for combo in index_combinations:
        total_price = calculate_total_price(combo, products, lowest_price)
        if total_price is not None and total_price < lowest_price:
            lowest_price = total_price
            lowest_combo = combo

    if lowest_combo:
        output_results(lowest_combo, lowest_price, products)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Fetch product data from kuantokusta.pt')
    parser.add_argument('inputs', nargs='+', type=str,
                        help='The URLs of the product pages followed by their quantities')
    args = parser.parse_args()

    if len(args.inputs) % 2 != 0:
        raise ValueError(
            "Each URL must be followed by its corresponding quantity.")

    urls_with_quantities = [(args.inputs[i], int(args.inputs[i + 1]))
                            for i in range(0, len(args.inputs), 2)]

    main(urls_with_quantities)
