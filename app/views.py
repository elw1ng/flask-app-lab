import logging
from pathlib import Path

from flask import flash, redirect, render_template, request, url_for

from . import app
from .forms import ContactForm


def _get_contact_logger():
    log_dir = Path(app.root_path).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("contact_form")
    if not logger.handlers:
        handler = logging.FileHandler(log_dir / "contact.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


@app.route("/")
def main():
    return render_template("index.html", title="Головна")


@app.route("/homepage")
def home():
    agent = request.user_agent.string or "Браузер не визначено"
    return render_template("homepage.html", title="Домашня сторінка", agent=agent)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            _get_contact_logger().info(
                "Contact form: name=%r email=%r topic=%r message=%r",
                form.name.data,
                form.email.data,
                form.topic.data,
                form.message.data,
            )
            flash("Дякуємо! Ваше повідомлення прийнято.", "success")
            return redirect(url_for("contacts"))

        flash("Перевірте поля форми та виправте помилки.", "danger")

    return render_template(
        "contacts.html",
        title="Контакти",
        form=form,
    )
