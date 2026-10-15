from flask import render_template, request

from . import app


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
    submitted = request.method == "POST"
    form_data = request.form if submitted else {}
    return render_template(
        "contacts.html",
        title="Контакти",
        submitted=submitted,
        form_data=form_data,
    )
