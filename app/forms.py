from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім’я",
        validators=[
            DataRequired(message="Введіть ім’я."),
            Length(max=80, message="Ім’я має містити не більше 80 символів."),
        ],
    )
    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Regexp(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                message="Введіть адресу електронної пошти у правильному форматі.",
            ),
        ],
    )
    topic = SelectField(
        "Тема повідомлення",
        choices=[
            ("", "Оберіть тему"),
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("feedback", "Відгук"),
        ],
        validators=[DataRequired(message="Оберіть тему повідомлення.")],
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(
                min=10,
                max=2000,
                message="Повідомлення має містити від 10 до 2000 символів.",
            ),
        ],
    )
    submit = SubmitField("Надіслати повідомлення")
