# Kuantokusta Bundle Price Scraper


## Description

A Python script that scrapes product prices from [Kuantokusta](https://www.kuantokusta.pt) and calculates the cheapest combination of stores to buy a bundle of items, taking into account both product prices and shipping costs.

## Features

- Scrapes product data and prices from Kuantokusta product pages.
- Finds the best combination of stores to minimize total cost (product prices + shipping costs).
- Supports specifying multiple products and quantities.
- Automatically handles cases where multiple stores offer the same product.

## How to Run

To run the scraper, use the following command in your terminal:

```bash
python .\scrape_kq.py '<URL_1>' <QUANTITY_1> '<URL_2>' <QUANTITY_2> ...
```

- Replace <URL_n> with the product URLs you want to scrape.
- Replace <QUANTITY_n> with the desired quantity of each corresponding product.

## Output

The script will display the following information:

- Lowest price: The total minimum price for purchasing all products.
- Store breakdown: For each store in the optimal combination, it lists:
    - Store name
    - Shipping cost
    - The products purchased from that store, along with their prices and quantities.

```bash
Lowest price: 150.00 EUR
-------
Store: Store A - Shipping: 5.00 EUR
Product: Product 1 - Price: 45.00 EUR - Quantity: 2
Product: Product 2 - Price: 20.00 EUR - Quantity: 1
-------
Store: Store B - Shipping: 7.00 EUR
Product: Product 3 - Price: 28.00 EUR - Quantity: 1
```