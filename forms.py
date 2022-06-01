from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    login = StringField("Login:", validators=[DataRequired("Необходимо заполнить поле Login.")])
    password = PasswordField("Password:", validators=[DataRequired("Необходимо заполнить поле Password.")])
    submit = SubmitField("Войти в систему.")

class ContactSocio(FlaskForm):
    telefon = StringField("Ваш номер телефона:", validators=[DataRequired("Необходимо заполнить поле \"Ваш номер\"")], render_kw={"placeholder": "+7977..."})
    email = StringField("Ваша контактная почта:", validators=[DataRequired("Необходимо заполнить поле \"Ваша контактная почта\""), Email("Был указан неккоректный формат почты.")], render_kw={"placeholder": "Почта@.ru"})
    textarea_msg = StringField("Если желаете, опишите вашу ситуацию:", widget=TextArea())
    submit_btn = SubmitField("Отправить заявку.")

class ContactYurist(FlaskForm):
    telefon = StringField("Ваш номер телефона:", validators=[DataRequired("Необходимо заполнить поле \"Ваш номер\"")], render_kw={"placeholder": "+7977..."})
    email = StringField("Ваша контактная почта:", validators=[DataRequired("Необходимо заполнить поле \"Ваша контактная почта\""), Email("Был указан не формат почты.")], render_kw={"placeholder": "Почта@.ru"})
    textarea_msg = StringField("Если желаете, опишите вашу ситуацию:", widget=TextArea())
    submit_btn = SubmitField("Отправить заявку.")