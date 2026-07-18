import unittest


def process_orders(orders, inventory):
    successful_orders = []

    for order in orders:
        product = order["product"]
        quantity = order["quantity"]

        if product not in inventory:
            raise ValueError(f"Product '{product}' not found in inventory")

        if quantity > inventory[product]:
            raise ValueError(f"Not enough stock for '{product}'")

        inventory[product] -= quantity
        successful_orders.append(order)

    return successful_orders


class TestProcessOrders(unittest.TestCase):

    def test_product_not_found(self):
        orders = [{"product": "banana", "quantity": 2}]
        inventory = {"apple": 10}

        with self.assertRaises(ValueError):
            process_orders(orders, inventory)

    def test_not_enough_stock(self):
        orders = [{"product": "apple", "quantity": 15}]
        inventory = {"apple": 10}

        with self.assertRaises(ValueError):
            process_orders(orders, inventory)

    def test_successful_order(self):
        orders = [{"product": "apple", "quantity": 4}]
        inventory = {"apple": 10}

        result = process_orders(orders, inventory)

        self.assertEqual(result, orders)
        self.assertEqual(inventory["apple"], 6)


if __name__ == "__main__":
    unittest.main()