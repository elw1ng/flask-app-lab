from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class DeleteProductForm(FlaskForm):
    pass


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[DataRequired(), Length(max=120)],
    )
    price = DecimalField(
        "Ціна",
        places=2,
        validators=[DataRequired(), NumberRange(min=0)],
    )
    description = TextAreaField(
        "Опис",
        validators=[DataRequired(), Length(max=2000)],
    )
    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Завантажте зображення JPG, PNG, GIF або WEBP.",
            )
        ],
    )
    submit = SubmitField("Зберегти товар")
