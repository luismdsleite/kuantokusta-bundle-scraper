class Product:
    def __init__(self, name, quantity=1):
        self.name = name
        self.stores = []  # Using a dictionary to map store instances to prices
        self.store_options = 0
        self.quantity = quantity

    def add_store(self, store, price):
        self.stores.append((store, price))
        self.store_options += 1

    def __repr__(self):
        return f"{self.name}"
