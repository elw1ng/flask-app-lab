from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    submitted = request.method == "POST"
    return render_template("contacts.html", title="Контакти", submitted=submitted)


if __name__ == "__main__":
    app.run(debug=True)
