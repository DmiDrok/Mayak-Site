from flask import Blueprint, render_template, request, session, redirect, url_for, g, flash, get_flashed_messages, current_app
from werkzeug.security import check_password_hash
from forms import LoginForm
import json
import sqlite3
from admin.manage_data import Data
import zipfile
import os

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

##Функция авторизации администратора
def admin_auth():
    session["admin"] = True

    #admin_login_dict = {"LoggedAdmin": session["admin"]}
    #with open("admin.json", "w") as jsonfile:
        #json.dump(admin_login_dict, jsonfile)

##Функция проверки на уже авторизованного администратора
def is_auth_admin():
    return True if session.get("admin", False) == True else False

##Проверка корректности содержимого zip-архива
def is_correct_zip(file):
    file_zip = zipfile.ZipFile(file, "r")

    for file in file_zip.infolist():
        if file.filename[-3::] in ["jpg", "png", "svg"]:
            continue
        else:
            return False
    
    return True

links = {
    "index": "",
    "add_post": "",
    "all_posts": "",
}
def reset_all_save_one(save_one: str):
    global links

    if save_one != None:
        for key in links:
            links[key] = ""
        
        links[save_one] = "active"
    else:
        for key in links:
            links[key] = ""

##Подключаем базу данных sqlite3
@admin.before_app_request
def before_first_request():
    if not hasattr(g, "conn"):
        with sqlite3.connect("data.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            conn.row_factory = sqlite3.Row

            ##Создадим БД если не существует
            cur.execute("""CREATE TABLE IF NOT EXISTS Posts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                title_search TEXT NOT NULL,
                text TEXT NOT NULL,
                image BLOB NOT NULL,
                date TEXT NOT NULL
            );""")

            g.conn = conn
            conn.commit()

##Обработчик главной страницы админки
@admin.route("/")
def index():
    ##Если пользователь не администратор - отправляем на авторизацию
    if not is_auth_admin():
        return redirect(url_for('.admin_login'))

    reset_all_save_one("index")
    admin = session.get("admin", False)

    data = Data(g.conn)
    all_posts_len = data.all_posts_len() ##Получаем кол-во всех постов


    return render_template(
        "admin/admin.html",
        all_posts_len=all_posts_len, 
        links=links,
        admin=admin
    )

##Обработчик входа в админку
@admin.route("/login", methods=["POST", "GET"])
def admin_login():
    reset_all_save_one(None)
    admin = session.get("admin", False)

    ##Если администратор уже авторизован - его перенаправит на главную страницу администрирования
    if is_auth_admin() == True:
        return redirect(url_for(".index"))

    ##Работа с формой
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            #with open("admin.json", "r") as jsonfile:
                #json_dict = json.load(jsonfile)
                #if json_dict["AdminLogged"] == False:
            #if form.login.data.strip() == "admin" and form.password.data.strip() == "12345":
            
            with open(os.path.join(current_app.root_path, "admin_data.json"), "r") as jsonfile:
                data_dict = json.load(jsonfile)

                ##Проверяем корректность введённого пароля
                if check_password_hash(data_dict["password"], form.password.data.strip()):
                    admin_auth()
                    return redirect(url_for(".index"))
                else: ##Если пользователь ошибся в данных - перенаправляем его на главную страницу
                    return redirect(url_for("index"))


    return render_template("admin/admin_login.html", form=form, links=links, admin=admin)

##Обработчик добавления новости
@admin.route("/add_post", methods=["POST", "GET"])
def add_post():

    ##Если не авторизован - отправляем авторизовываться
    if is_auth_admin() == False:
        return redirect(url_for(".admin_login"))

    data = Data(g.conn)
    reset_all_save_one("add_post")
    admin = session.get("admin", False)
    save = True

    title_post = ""
    category_post = ""
    text_content_post = ""

    ##Если пришёл POST - запрос - обрабатываем его.
    if request.method == "POST":
        ##Проверки на корректность
        if len(request.form["title"].strip()) > 3 and len(request.form["category"]) > 3 and len(request.form["text_content"].strip()) > 5:
            if len(request.form["title"].strip()) > 3:
                if len(request.form["category"].strip()) > 3:
                    if len(request.form["text_content"].strip()) > 5:
                        title = request.form["title"].strip()
                        category = request.form["category"].strip()
                        text_content = request.form["text_content"].strip()

                        ##Превью поста и проверка. Если нет загруженной картинки - ставим картинку по умолчанию
                        img = request.files["image_load"].read()
                        if not img:
                            with current_app.open_resource(os.path.join(current_app.root_path, "static", "img", "logo.png"), "rb") as file:
                                img = file.read()

                        ##Картинки внутри поста
                        imgs_post = request.files["zip_images_load"]
                        if imgs_post:
                            if not imgs_post.filename.endswith(".zip"): ##Если грузится не zip-архив
                                flash("Был загружен не zip-формат.", category="error")
                                return render_template("admin/admin_add_post.html", links=links, admin=admin, title_post=title, category_post=category, text_content_post=text_content)

                            ##Если внутри zip-архива лежат не только картинки
                            if not is_correct_zip(imgs_post):
                                flash("Внутри zip-архива содержится недопустимый формат файла", category="error")
                                return render_template("admin/admin_add_post.html", links=links, admin=admin, title_post=title, category_post=category, text_content_post=text_content)

                            if save:
                                data.save_post(category, title, text_content, img)
                                save = False
                            ##Сохраняем картинки в папку с постом
                            data.create_file_post(imgs_post, current_app.root_path)
                        else:
                            print("ZIP - архив не грузился.")
                        
                        ##Сохраняем пост и проверяем на дубликат
                        if save:
                            if data.save_post(category, title, text_content, img) != "has": ##Если поста с таким же названием нет в БД
                                flash(f"Проверить пост \"{title}\"", category="success")
                            else: ##Если пост с таким название существует - предупреждаем пользователя
                                flash(f"Пост с названием \"{title}\" уже существует", category="error")
                    else:
                        flash("Текст поста должен содержать более 5 символов!", category="error")
                else:
                    flash("Категория должна содержать более 3 символов!", category="error")
            else:
                flash("Название должно содержать более 3 символов!", category="error")
        else:
            flash("Вы не ввели ни одного поля!", category="error")

    return render_template(
    "admin/admin_add_post.html", 
    links=links, 
    admin=admin,
    title_post=title_post,
    category_post=category_post,
    text_content_post=text_content_post
    )

##Обработчик страницы всех новостей
@admin.route("/all_posts")
def all_posts():

    ##Если не авторизован - отправляем авторизовываться
    if is_auth_admin() == False:
        return redirect(url_for(".admin_login"))

    reset_all_save_one("all_posts")
    admin = session.get("admin", False)

    data = Data(g.conn)
    all_posts_len = data.all_posts_len()
    all_posts = data.get_all_posts()


    return render_template(
        "admin/admin_all_posts.html",
        links=links, 
        admin=admin,
        all_posts_len=all_posts_len,
        posts=all_posts
        )

##Обработчик переделки поста
@admin.route("/post/<post_id>/remake", methods=["POST", "GET"])
def remake_post(post_id):

    ##Если не авторизован - отправляем авторизовываться
    if is_auth_admin() == False:
        return redirect(url_for(".admin_login"))

    data = Data(g.conn)
    post = data.get_post_by_id(post_id)
    reset_all_save_one(None)
    admin = is_auth_admin()

    title_post = post["title"]
    category_post = post["category"]
    text_content_post = post["text"]

    ##Обработка POST-запроса
    if request.method == "POST":
        if len(request.form["title"].strip()) > 3 and len(request.form["category"]) > 3 and len(request.form["text_content"].strip()) > 5:
            if len(request.form["title"].strip()) > 3:
                if len(request.form["category"].strip()) > 3:
                    if len(request.form["text_content"].strip()) > 5:
                        ##Получаем чекбоксы с: удалять или не удалять
                        del_images_post = True if request.form.get("del_images") == "on" else False
                        del_prev = True if request.form.get("del_prev") == "on" else False

                        title = request.form["title"].strip()
                        category = request.form["category"].strip()
                        text_content = request.form["text_content"].strip()

                        ##Поскольку это обновление поста - если нет картинки - то не меняем её
                        img = request.files["image_load"].read()
                        if not img:
                            img = None

                        ##Картинки внутри поста
                        imgs_post = request.files["zip_images_load"]
                        if imgs_post:
                            if not imgs_post.filename.endswith(".zip"): ##Если грузится не zip-архив
                                flash("Был загружен не zip-формат.", category="error")
                                return render_template("admin/admin_add_post.html", links=links, admin=admin, title_post=title, category_post=category, text_content_post=text_content)

                            ##Если внутри zip-архива лежат не только картинки
                            if not is_correct_zip(imgs_post):
                                flash("Внутри zip-архива содержится недопустимый формат файла", category="error")
                                return render_template("admin/admin_add_post.html", links=links, admin=admin, title_post=title, category_post=category, text_content_post=text_content)

                            if save:
                                data.save_post(category, title, text_content, img)
                                save = False
                            ##Сохраняем картинки в папку с постом
                            data.resave_file_post(imgs_post, current_app.root_path)
                        
                        try:
                            data.remake_post(post_id, category, text_content, title, img)
                            flash(f"Успешно изменён пост \"{title}\"", category="success")

                            post_title = title
                            post_category = category
                            post_text = text_content
                        except:
                            flash("Произошла ошибка при изменении", category="error")
                    else:
                        flash("Текст поста должен содержать более 5 символов!", category="error")
                else:
                    flash("Категория должна содержать более 3 символов!", category="error")
            else:
                flash("Название должно содержать более 3 символов!", category="error")
        else:
            flash("Вы не ввели ни одного поля!", category="error")
    
    return render_template(
    "admin/remake_post.html",
    links=links, 
    admin=admin,
    title_post=title_post,
    category_post=category_post,
    text_content_post = text_content_post,
    )

##Обработчик удаления поста
@admin.route("del_post/<post_id>", methods=["POST", "GET"])
def del_post(post_id):
    ##Если не авторизован - отправляем авторизовываться
    if is_auth_admin() == False:
        return redirect(url_for(".admin_login"))

    data = Data(g.conn)
    post = data.get_post_by_id(post_id)
    reset_all_save_one(None)
    admin = is_auth_admin()

    ##Обрабатываем POST-запрос
    if request.method == "POST":
        if request.form["del_inp"].strip() == post["title"].strip():
            data.delete_post_by_id(post_id)
            flash(f"Пост \"{post['title']}\" успешно удалён.", category="success")

            return redirect(url_for(".all_posts"))
        else:
            flash(f"Неправильно указано название поста.", category="error")

    return render_template("admin/del_post.html", links=links, admin=admin, title_post=post["title"])

##Обработчик загрузки изображений на сервер
@admin.route("add_post/files_upload/<post_id>")
def files_upload(post_id):
    reset_all_save_one("add_post")
    admin = session.get("admin", False)
    return render_template(
        "admin/admin_upload_files.html",
        links=links,
        admin=admin
    )

##Обработчик выхода из админки
@admin.route("/pop")
def admin_pop():
    ##Если не авторизован - отправляем авторизовываться
    if is_auth_admin() == False:
        return redirect(url_for(".admin_login"))

    session.pop("admin", None)

    #admin_login_dict = {"AdminLogged": False}
    #with open("admin.json", "w") as jsonfile:
        #json.dump(admin_login_dict, jsonfile)

    return redirect(url_for("index"))

#@admin.teardown_app_request
#def teardown_app_request(exception):
    #if hasattr(g, "conn"):
        #g.conn.close()