import unittest

from app import app
from app.products.database import Product, get_product, list_products, products_table


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.csrf_enabled = app.config.get("WTF_CSRF_ENABLED", True)
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def tearDown(self):
        app.config["WTF_CSRF_ENABLED"] = self.csrf_enabled

    def test_products_page_lists_all_products(self):
        products = list_products()
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        for product in products:
            self.assertIn(product["name"].encode(), response.data)

    def test_product_detail_page_displays_product(self):
        products = list_products()
        if not products:
            self.skipTest("No products are stored in TinyDB")
        product = products[0]
        response = self.client.get(f"/products/{product['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(product["name"].encode(), response.data)
        expected_price = f"{float(product['price']):.2f}".encode()
        self.assertIn(expected_price, response.data)

    def test_missing_product_returns_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)

    def test_product_can_be_created_updated_and_deleted(self):
        name = "Temporary lab product"
        products_table.remove(Product.name == name)
        response = self.client.post(
            "/products/create",
            data={
                "name": name,
                "price": "25.50",
                "description": "Temporary product description",
            },
        )
        self.assertEqual(response.status_code, 302)

        product = next(item for item in products_table.all() if item["name"] == name)
        product_id = product.doc_id
        response = self.client.post(
            f"/products/{product_id}/edit",
            data={
                "name": "Updated lab product",
                "price": "30.00",
                "description": "Updated product description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_product(product_id)["name"], "Updated lab product")

        response = self.client.post(f"/products/{product_id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(get_product(product_id))


if __name__ == "__main__":
    unittest.main()
