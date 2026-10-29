from pathlib import Path

from tinydb import Query, TinyDB

from .. import app


Path(app.instance_path).mkdir(parents=True, exist_ok=True)
db = TinyDB(Path(app.instance_path) / "products.json")
products_table = db.table("products")
Product = Query()


def seed_products():
    """Add the original demonstration products to an empty database."""
    if products_table.all():
        return

    products_table.insert_multiple(
        [
            {
                "name": "Laptop",
                "price": 1200,
                "description": "Powerful laptop with Intel Core i7 processor, 16GB RAM, and 512GB SSD.",
                "image": "",
            },
            {
                "name": "Phone",
                "price": 800,
                "description": "Modern smartphone with a 6.5-inch OLED display and a high-quality camera.",
                "image": "",
            },
            {
                "name": "PC",
                "price": 1800,
                "description": "Desktop computer with RTX 4070 graphics, 32GB RAM, and 1TB SSD.",
                "image": "",
            },
        ]
    )


def list_products():
    return [
        {**dict(product), "id": product.doc_id}
        for product in products_table.all()
    ]


def get_product(product_id):
    product = products_table.get(doc_id=product_id)
    if product is None:
        return None
    return {**dict(product), "id": product.doc_id}


def add_product(product):
    return products_table.insert(product)


def update_product(product_id, product):
    return products_table.update(product, doc_ids=[product_id])


def remove_product(product_id):
    return products_table.remove(doc_ids=[product_id])


seed_products()
