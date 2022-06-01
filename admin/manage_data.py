from datetime import datetime
import sqlite3
import os
from tkinter import EXCEPTION
import zipfile
import re


class Data:
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    ##Взять длину таблицы с постами
    def all_posts_len(self):
        try:
            sql = "SELECT count(*) FROM Posts"
            self.cur.execute(sql)

            result = self.cur.fetchone()[0]
            return result

        except:
            return False

    ##Записать пост
    def save_post(self, category, title, text, image):
        
        sql = "SELECT title FROM Posts WHERE title = ?"
        self.cur.execute(sql, (title, ))

        check = self.cur.fetchone()
        if check != None:
            return "has"

        sql = "INSERT INTO Posts (category, title, title_search, text, image, date) VALUES (?, ?, ?, ?, ?, ?)"
        date = datetime.now().strftime("%d-%m-%Y")
        image_b = sqlite3.Binary(image)

        title_search = re.sub(r"[?<>\\/:*\"]", "", title).strip()
        
        self.cur.execute(sql, (category, title, title_search, text, image_b, date))
        self.conn.commit()


        return True

    ##Взять все посты
    def get_all_posts(self):
        try:
            sql = "SELECT * FROM Posts ORDER BY ID DESC;"
            self.cur.execute(sql)

            result = self.cur.fetchall()
            return result

        except:
            return False

    ##Взять пост по его айди
    def get_post_by_id(self, post_id):
        try:
            sql = "SELECT * FROM Posts WHERE id = ?"
            self.cur.execute(sql, (post_id))

            result = self.cur.fetchone()
            return result
        except Exception as err:
            print(err)
            return False

    ##Взять картинку по айди поста
    def get_image_by_id(self, post_id):
        try:
            sql = "SELECT image FROM Posts WHERE id = ?"
            self.cur.execute(sql, (post_id))

            result = self.cur.fetchone()[0]
            return result
        except:
            return False

    ##Создать папку с постом и его внутренностями
    def create_file_post(self, file_zip, root_path):
        try:
            sql = "SELECT * FROM Posts ORDER BY id DESC LIMIT 1;"
            self.cur.execute(sql)

            result = self.cur.fetchone()
            post_id = int(result["id"]) + 1
            post_title = re.sub(r"[?<>\\/:*\"]", "", result["title"]).strip()
            
            path_to_post = os.path.join(root_path, "static", "posts", f"{post_title}")

            ##Если нет папки где хранятся все посты - создаём её
            if not os.path.exists(os.path.join(root_path, "static", "posts")):
                os.mkdir(os.path.join(root_path, "static", "posts"))

            ##Если нет папки с постом - создаём её
            if not os.path.exists(path_to_post):
                os.mkdir(os.path.join(path_to_post))
            else: ##Если папка есть - удаляем и создаём заново
                os.remove(os.path.join(path_to_post))
                os.mkdir(os.path.join(path_to_post))
            

            ##Открываем zip и перекладываем картинки в папки
            with zipfile.ZipFile(file_zip, "r") as file_zip:
                for file in file_zip.infolist():
                    with file_zip.open(file, "r") as file_img:
                        binary_img = file_img.read()
                        with open(os.path.join(root_path, "static", "posts", f"{post_title}", f"{file.filename}"), "wb") as file_bin:
                            file_bin.write(binary_img)

            return True

        except Exception as err:
            print(err)
            return False

    ##Взять текст поста по айди
    def get_text_by_id(self, post_id):
        try:
            sql = "SELECT text FROM Posts WHERE id = ?"
            self.cur.execute(sql, (post_id))

            result = self.cur.execute()[0]
            return result
        except Exception as err:
            print(err)
            return False

    ##Изменить содержимое поста
    def remake_post(self, post_id, category, text, title, image):
        result = None
        print(post_id, " !!!!!")
        try:          
            title_search = re.sub(r"[?<>\\/:*\"]", "", title).strip()
            if image != None:
                sql = "UPDATE Posts SET title = ?, title_search = ?, text = ?, image = ? WHERE id LIKE ?;"
                image = sqlite3.Binary(image)
                result = self.cur.execute(sql, (title, title_search, text, image, post_id))
            else:
                sql = "UPDATE Posts SET title = ?, title_search = ?, text = ? WHERE id LIKE ?;"
                result = self.cur.execute(sql, (title, title_search, text, post_id))
            
            self.conn.commit()

            print(result)
            print("-------")

            return True
        except Exception as err:
            print(err)
            return False

    ##Удалить пост по айди
    def delete_post_by_id(self, id):
        try:
            sql = "DELETE FROM Posts WHERE id == ?"
            self.cur.execute(sql, (id, ))
            self.conn.commit()
            return True
        except:
            return False
