from flask import flash, redirect, render_template, request, session, url_for

from . import users_bp


DEMO_USERNAME = "student"
DEMO_PASSWORD = "flask123"


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template(
        "hi.html",
        title="Greeting Page",
        name=name,
        age=age,
    )


@users_bp.route("/admin")
def admin():
    greeting_url = url_for(
        "users.greetings",
        name="administrator",
        age=45,
        _external=True,
    )
    return redirect(greeting_url)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username", "").strip()

    if request.method == "POST":
        password = request.form.get("password", "")
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session.clear()
            session["username"] = username
            flash("Вхід виконано успішно.", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильне ім’я користувача або пароль.", "danger")

    return render_template("login.html", title="Вхід", username=username)


@users_bp.route("/profile")
def profile():
    username = session.get("username")
    if username is None:
        flash("Спочатку увійдіть у систему, щоб відкрити профіль.", "warning")
        return redirect(url_for("users.login"))

    return render_template("profile.html", title="Профіль", username=username)


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))
