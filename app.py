from flask import Flask, render_template, url_for, session, redirect, g, make_response, current_app, request, flash, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from admin.admin import admin
from admin.manage_data import Data
import sqlite3
import os
import json
from forms import ContactSocio, ContactYurist
import re
from manage_mails.send import Sender

##WSGI - приложение
app = Flask(__name__, template_folder="templates", static_folder="static")
app.register_blueprint(admin, url_prefix="/admin") ##Регистрируем blueprint админки

##Конфиг
SECRET_KEY = "0ewaf0asdfjao90j32f03kfoasd,coamda-0e1=-efo=asdkcaskcoasdjf0329qgj=q20=0=rcvb,cvolmbolasamfoasdf-sadf-#$#$$)@_R)KIFJSDFJ9ojasdgj"
CSRF_ENABLED = True
app.config.from_object(__name__)

##Объект с помощью которого будем отсылать сообщения
Sender = Sender()

##Для класса .active_link в навигации
links = {
    "index": "",
    "gym": "",
    "school_dance": "",
    "dom": "",
}

##Для того, чтобы сделать ссылку активной и пользователь по навигации мог понять где он находится
def reset_all_save_one(save_one: str) -> None:
    global links

    if save_one != None:
        for key in links:
            links[key] = ""

        links[save_one] = "active_link"
    else:
        for key in links:
            links[key] = ""

##Проверка на администратора
def is_admin() -> bool:
    return True if session.get("admin", False) == True else False

admin = False
data = None
@app.before_request
def before_request():
    global admin
    admin = is_admin()

    ##Создаём папку где будут храниться посты для блога если она ещё не сделана
    if not os.path.exists(os.path.join(current_app.root_path, "static", "posts")):
        os.mkdir(os.path.join(current_app.root_path, "static", "posts"))

    ##Если не сделан файл где мы храним данные админа - делаем его и засовываем туда логин с паролем
    if not os.path.exists(os.path.join(current_app.root_path, "admin_data.json")):
        login = "admin"

        with open(os.path.join(current_app.root_path, "admin_data.json"), "w") as jsonfile:
            dict_data = {
                "login": f"{login}",
                "password": f"{generate_password_hash('12345')}"
            }

            json.dump(dict_data, jsonfile)


    ##Сохраняем подключение в контексте запроса
    if not hasattr(g, "conn"):
        with sqlite3.connect("Posts.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            conn.row_factory = sqlite3.Row

            g.conn = conn

    #data = Data(g.conn)

##Обработчик главной страницы
@app.route("/main")
@app.route("/index")
@app.route("/")
def index():
    reset_all_save_one(None)
    return render_template("index.html", title="Главная", links=links, admin=admin)

##Обработчик страницы тренажёрного зала
@app.route("/gym")
def gym():
    reset_all_save_one("gym")
    return render_template("gym.html", title="Тренажёрный зал", links=links, admin=admin)

##Обработчик страницы Школы Танца
@app.route("/school_dance")
def school_dance():
    reset_all_save_one("school_dance")
    return render_template("school_dance.html", title="Школа Танца", links=links, admin=admin)

##Обработчик страницы МООМ ДОМА
@app.route("/moom_dom")
def dom():
    reset_all_save_one("dom")
    return render_template("dom.html", title="МООМ ДОМ", links=links, admin=admin)

##Обработчик страницы психологов
@app.route("/socio_psych", methods=["POST", "GET"])
def socio_psych():
    reset_all_save_one(None)
    form = ContactSocio() ##Форма для контакта

    telefon_user = ""
    email_user = ""
    message_user = ""

    ##Обрабатываем форму
    if request.method == "POST":
        if form.validate_on_submit():
            telefon_user = form.telefon.data.replace("(", "").replace(")", "").replace("-", "").replace("+", "")
            email_user = form.email.data.strip()
            message_user = form.textarea_msg.data.strip()

            ##Проверяем корректность введённых данных пользователем
            if len(re.findall(r"^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$", telefon_user)) > 0:
                print(f"Пользователь указал корректный телефон: {telefon_user}")

                ##Отправляем и выкидываем флеш-сообщение
                Sender.send_socio_psych("Социально-психологическая помощь.", telefon_user, email_user, message_user)
                flash("Заявка будет рассмотрена в течении 2-х дней.", category="success")

            else:
                print(f"Пользователь указал НЕкорректный телефон: {telefon_user}")
                flash("Указан неккоректный формат телефона!", category="error")


    return render_template(
        "socio_psych.html",
        title="Социально-психологическая помощь",
        links=links, admin=admin,
        form=form,
        telefon_user=telefon_user,
        email_user=email_user,
        message_user=message_user
        )

##Обработчик страницы юристов
@app.route("/yurist", methods=["POST", "GET"])
def yurist():
    reset_all_save_one(None)

    form = ContactYurist()

    if request.method == "POST":
        if form.validate_on_submit():
            telefon_user = form.telefon.data.replace("(", "").replace(")", "").replace("-", "").replace("+", "")
            email_user = form.email.data.strip()
            message_user = form.textarea_msg.data.strip()

            ##Проверяем корректность введённых данных пользователем
            if len(re.findall(r"^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$", telefon_user)) > 0:
                print(f"Пользователь указал корректный телефон: {telefon_user}")

                ##Отправляем и выкидываем флеш-сообщение
                Sender.send_socio_psych("Юридические услуги.", telefon_user, email_user, message_user)
                flash("Заявка будет рассмотрена в течении 2-х дней.", category="success")
            else:
                print(f"Пользователь указал НЕкорректный телефон: {telefon_user}")
                flash("Указан неккоректный формат телефона!", category="error")

    return render_template("yurist.html", title="Юридическая помощь", links=links, admin=admin, form=form)

@app.route("/send_mail_socio_psych")
def send_mail_socio_psych():
    return render_template("send_mail.html")

##Обработчик страницы с отзывами о юристах
@app.route("/yurist/feedback")
def yurist_feedback():
    reset_all_save_one(None)
    return render_template("yurist_feedback.html", title="Юридическая помощь (отзывы)", links=links, admin=admin)

##Обработчик страницы с командой юристов
@app.route("/yurist/team")
def yurist_team():
    reset_all_save_one(None)
    return render_template("yurist_team.html", title="Команда юристов", links=links, admin=admin)

##Обработчик отображения страницы с постами
@app.route("/all_posts")
@app.route("/posts")
def all_posts():
    reset_all_save_one(None)

    data = Data(g.conn)
    all_posts = data.get_all_posts()
    if len(all_posts) < 0:
        all_posts = None

    return render_template("all_posts.html", links=links, posts=all_posts, admin=admin)

##Обработчик отображения одного из постов
@app.route("/post/<post_id>")
def post(post_id):
    reset_all_save_one(None)

    data = Data(g.conn)
    post_to_display = data.get_post_by_id(post_id)

    return render_template("post.html", links=links, admin=admin, post=post_to_display)

##Обработчик для вывода картинки в блок поста
@app.route("/post_img/<post_id>")
def post_image(post_id):

    data = Data(g.conn)
    image = data.get_image_by_id(post_id)

    response = make_response(image, 200)
    response.headers["Content-Type"] = "image/png"

    return response

##Сработает когда произойдёт уничтожение контекста приложения
@app.teardown_appcontext
def teardown(exception):
    if hasattr(g, "conn"):
        g.conn.close()

##Переход на несуществующую страницу
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("index")) ##Перенаправляем на главную страницу

##Точка входа
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
