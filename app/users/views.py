from flask import redirect, render_template, request, url_for

from . import users_bp


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
