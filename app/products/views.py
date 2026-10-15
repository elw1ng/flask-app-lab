from flask import abort, render_template

from . import products_bp

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "description": "Powerful laptop with Intel Core i7 processor, 16GB RAM, and 512GB SSD.",
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "description": "Modern smartphone with a 6.5-inch OLED display and a high-quality camera.",
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "description": "Desktop computer with RTX 4070 graphics, 32GB RAM, and 1TB SSD.",
    },
]


@products_bp.route("/")
def index():
    return render_template("products/products.html", title="Products", products=products)


@products_bp.route("/<int:product_id>")
def detail(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product is None:
        abort(404)
    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product,
    )
