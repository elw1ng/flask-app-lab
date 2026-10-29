from pathlib import Path
from uuid import uuid4

from flask import abort, current_app, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from . import products_bp
from .database import add_product, get_product, list_products, remove_product, update_product
from .forms import DeleteProductForm, ProductForm


def _save_image(image):
    if not image or not image.filename:
        return ""

    safe_name = secure_filename(image.filename)
    extension = Path(safe_name).suffix.lower()
    if not extension:
        return ""

    filename = f"{uuid4().hex}{extension}"
    upload_folder = Path(current_app.static_folder) / "uploads"
    upload_folder.mkdir(parents=True, exist_ok=True)
    image.save(upload_folder / filename)
    return filename


def _delete_image(filename):
    if not filename:
        return
    upload_folder = (Path(current_app.static_folder) / "uploads").resolve()
    image_path = (upload_folder / filename).resolve()
    if image_path.parent == upload_folder and image_path.is_file():
        image_path.unlink()


@products_bp.route("/")
def index():
    return render_template(
        "products.html",
        title="Товари",
        products=list_products(),
    )


@products_bp.route("/create", methods=["GET", "POST"])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = {
            "name": form.name.data.strip(),
            "price": float(form.price.data),
            "description": form.description.data.strip(),
            "image": _save_image(form.image.data),
        }
        add_product(product)
        flash("Товар успішно додано.", "success")
        return redirect(url_for("products.index"))

    if form.is_submitted():
        flash("Перевірте поля форми та виправте помилки.", "danger")
    return render_template(
        "form_product.html",
        title="Додати товар",
        form=form,
        heading="Додати товар",
    )


@products_bp.route("/<int:product_id>")
def detail(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)
    return render_template(
        "detail_product.html",
        title=product["name"],
        product=product,
        delete_form=DeleteProductForm(),
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit(product_id):
    product = get_product(product_id)
    if product is None:
        abort(404)

    form = ProductForm()
    if form.validate_on_submit():
        image_name = _save_image(form.image.data) or product.get("image", "")
        update_product(
            product_id,
            {
                "name": form.name.data.strip(),
                "price": float(form.price.data),
                "description": form.description.data.strip(),
                "image": image_name,
            },
        )
        if image_name != product.get("image", ""):
            _delete_image(product.get("image", ""))
        flash("Зміни товару збережено.", "success")
        return redirect(url_for("products.detail", product_id=product_id))

    if form.is_submitted():
        flash("Перевірте поля форми та виправте помилки.", "danger")
    else:
        form.name.data = product["name"]
        form.price.data = product["price"]
        form.description.data = product["description"]

    return render_template(
        "form_product.html",
        title="Редагувати товар",
        form=form,
        heading="Редагувати товар",
        product=product,
    )


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def delete(product_id):
    form = DeleteProductForm()
    if not form.validate_on_submit():
        abort(400)

    product = get_product(product_id)
    if product is None:
        abort(404)

    remove_product(product_id)
    _delete_image(product.get("image", ""))
    flash("Товар видалено.", "success")
    return redirect(url_for("products.index"))
