class Store:
    def __init__(self, name, shipping_cost):
        self.name = name
        self.shipping_cost = shipping_cost

    def __repr__(self):
        return f"{self.name} - Shipping: {self.shipping_cost} EUR"

    def update_shipping_price(self, new_price):
        if new_price < self.shipping_cost:
            self.shipping_cost = new_price
