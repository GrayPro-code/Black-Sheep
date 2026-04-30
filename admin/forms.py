from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class PortfolioForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    category = SelectField(
        "Категория",
        choices=[
                        ("web", "Web"), 
                        ("design", "Design"),
                        ("games", "Games"),
                        ("development", "Development"), 
                        ],
        validators=[DataRequired()]
    )
    year = IntegerField("Год", validators=[Optional()])
    tech1 = StringField("Технология 1", validators=[Optional()])
    tech2 = StringField("Технология 2", validators=[Optional()])
    image = FileField("Изображение", validators=[
        FileAllowed(["png", "jpg", "jpeg", "gif"], "Только изображения!")
    ])
    submit = SubmitField("Сохранить")
