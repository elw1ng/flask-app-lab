from urllib.parse import quote, unquote

from flask import (
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import users_bp


DEMO_USERNAME = "student"
DEMO_PASSWORD = "flask123"


def _login_redirect():
    if session.get("username") is None:
        flash("Спочатку увійдіть у систему, щоб керувати профілем.", "warning")
        return redirect(url_for("users.login"))
    return None


def _profile_cookies():
    session_cookie = current_app.config["SESSION_COOKIE_NAME"]
    return {
        key: unquote(value)
        for key, value in request.cookies.items()
        if key != session_cookie
    }


def _valid_cookie_name(key):
    return bool(key) and all(
        character.isascii() and (character.isalnum() or character in "_-")
        for character in key
    )


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
    login_redirect = _login_redirect()
    if login_redirect:
        return login_redirect

    theme = request.cookies.get("profile_theme", "light")
    if theme not in {"light", "dark"}:
        theme = "light"

    return render_template(
        "profile.html",
        title="Профіль",
        username=session["username"],
        cookies=_profile_cookies(),
        theme=theme,
    )


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/cookies/add", methods=["POST"])
def add_cookie():
    login_redirect = _login_redirect()
    if login_redirect:
        return login_redirect

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age_text = request.form.get("max_age", "").strip()
    session_cookie = current_app.config["SESSION_COOKIE_NAME"]

    if not _valid_cookie_name(key) or key == session_cookie:
        flash("Вкажи допустимий ключ cookie (літери, цифри, _ або -).", "danger")
        return redirect(url_for("users.profile"))

    try:
        max_age = int(max_age_text)
    except ValueError:
        max_age = 0

    if not value or max_age <= 0:
        flash("Вкажи значення та термін дії в секундах, більший за нуль.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        key,
        quote(value, safe=""),
        max_age=max_age,
        path="/",
        httponly=True,
        samesite="Lax",
    )
    flash(f"Cookie «{key}» додано.", "success")
    return response


@users_bp.route("/cookies/delete", methods=["POST"])
def delete_cookie():
    login_redirect = _login_redirect()
    if login_redirect:
        return login_redirect

    key = request.form.get("key", "").strip()
    if not key or key == current_app.config["SESSION_COOKIE_NAME"]:
        flash("Вибери cookie зі списку користувацьких cookies.", "warning")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash(f"Cookie «{key}» не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key, path="/")
    flash(f"Cookie «{key}» видалено.", "success")
    return response


@users_bp.route("/cookies/delete-all", methods=["POST"])
def delete_all_cookies():
    login_redirect = _login_redirect()
    if login_redirect:
        return login_redirect

    cookies = _profile_cookies()
    response = make_response(redirect(url_for("users.profile")))
    for key in cookies:
        response.delete_cookie(key, path="/")

    if cookies:
        flash("Усі користувацькі cookies видалено.", "success")
    else:
        flash("Немає користувацьких cookies для видалення.", "warning")
    return response


@users_bp.route("/theme", methods=["POST"])
def choose_theme():
    login_redirect = _login_redirect()
    if login_redirect:
        return login_redirect

    theme = request.form.get("theme", "")
    if theme not in {"light", "dark"}:
        flash("Вибери світлу або темну схему.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        "profile_theme",
        theme,
        max_age=60 * 60 * 24 * 365,
        path="/",
        httponly=True,
        samesite="Lax",
    )
    flash("Кольорову схему збережено.", "success")
    return response
