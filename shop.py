import sqlite3
import re
from hashlib import md5


class QueryData:
    def __init__(self, connect, cursor):
        self.con = connect
        self.cur = cursor
        self.vars = dict()

    def valid_num(self, name_var):
        while True:
            num = input(name_var + ": ")
            if num.isdigit():
                if int(num) >= 0:
                    break
                else:
                    print("Ошибка: вы ввели отрицательное число")
            else:
                print("Ошибка: вы ввели не число .")
        return num

    def valid_phone(self, name_var):
        while True:
            phone = input(name_var + ": ")
            patt = (r"^(\+7|8)[-(]?([0-9]{3})[-)]?([0-9]{3})[-]?"
                    r"([0-9]{2})[-]?([0-9]{2})$")
            if re.search(patt, phone):
                break
            else:
                print("Ошибка: вы ввели номер телефона не правильно.")
        return re.sub(patt, r"8\2\3\4\5", phone)

    def valid_email(self, name_var):
        while True:
            email = input(name_var + ": ")
            patt = "[A-Za-z1-9._-]+@[A-Za-z1-9._-]+[.][a-z]"
            if re.search(patt, email):
                break
            else:
                print("Ошибка: вы ввели email не правильно.")
        return email

    def valid_passw(self, name_var):
        while True:
            passw = input(name_var + ": ")
            patt = "[A-Za-z1-9!@#$%^&*()_+-={}\[\]\\\|/<>,.:;~]{6,}"
            if re.search(patt, passw):
                break
            else:
                print("Ошибка: пароль меньше 6 символов или символы не в ascii")
        return md5(bytes(passw, "ascii")).hexdigest()

    def pattern_insert(self, name_tab):
        sql = (
                "INSERT INTO " + name_tab + " (" +
                ", ".join(self.vars.keys()) + ") " +
                "VALUES (" + "?, " * (len(self.vars) - 1) + "?)"
        )
        print("Введите данные ", name_tab, ".", sep="")
        data = []
        for key in self.vars:
            if self.vars[key] == "int":
                data.append(self.valid_num(key))
            elif self.vars[key] == "phone":
                data.append(self.valid_phone(key))
            elif self.vars[key] == "email":
                data.append(self.valid_email(key))
            elif self.vars[key] == "passw":
                data.append(self.valid_passw(key))
            elif self.vars[key] == "str":
                data.append(input(key + ": "))

        try:
            self.cur.execute(sql, data)
        except sqlite3.DatabaseError as error:
            print("Ошибка", error)
        else:
            print("Запрос успешно выполнен")
            self.con.commit()

    def insert_catalog(self):
        self.vars = {"name": "str"}
        self.pattern_insert("catalog")

    def insert_subcatalog(self):
        self.vars = {
            "id_catalog": "int",
            "name": "str"
        }
        self.pattern_insert("subcatalog")

    def insert_product(self):
        self.vars = {
            "id_subcatalog": "int",
            "name": "str",
            "description": "str",
            "price": "int",
            "old_price": "int",
            "new": "int"
        }
        self.pattern_insert("product")

    def insert_image(self):
        self.vars = {
            "id_product": "int",
            "image": "str"
        }
        self.pattern_insert("image")

    def insert_size(self):
        self.vars = {
            "size": "str"
        }
        self.pattern_insert("size")

    def insert_count(self):
        self.vars = {
            "id_product": "int",
            "id_size": "int",
            "count": "int",
        }
        self.pattern_insert("count")

    def insert_user(self):
        self.vars = {
            "username": "str",
            "name": "str",
            "surname": "str",
            "email": "email",
            "password": "passw",
            "address": "str",
            "phone": "phone",
            "is_superuser": "int"
        }
        self.pattern_insert("user")

    def insert_order_shop(self):
        self.vars = {
            "id_user": "int",
            "name": "str",
            "surname": "str",
            "email": "email",
            "address": "str",
            "date": "str",
            "comment": "str",
            "delivery_price": "int",
            "total": "int"
        }
        self.pattern_insert("order_shop")

    def insert_product_order(self):
        self.vars = {
            "id_product": "int",
            "id_order_shop": "int",
            "size": "int",
            "count": "int",
        }
        self.pattern_insert("product_order")

    def __del__(self):
        print("this is __del__")


if __name__ == '__main__':
    con = sqlite3.connect("store.db")
    with con:
        cur = con.cursor()
        query = QueryData(con, cur)

        print(
            "-------------------------------------",
            "1) Добавить данные в catalog;",
            "2) Добавить данные в subcatalog;",
            "3) Добавить данные в product;",
            "4) Добавить данные в image;",
            "5) Добавить данные в size;",
            "6) Добавить данные в count;",
            "7) Добавить данные в user;",
            "8) Добавить данные в order_shop;",
            "9) Добавить данные в prodcut_order;",
            "Для выхода введите quit.",
            "--------------------------------------",
            sep="\n"
        )
        while True:
            remote = input("Введите число: ")
            if remote == "1":
                query.insert_catalog()
            elif remote == "2":
                query.insert_subcatalog()
            elif remote == "3":
                query.insert_product()
            elif remote == "4":
                query.insert_image()
            elif remote == "5":
                query.insert_size()
            elif remote == "6":
                query.insert_count()
            elif remote == "7":
                query.insert_user()
            elif remote == "8":
                query.insert_order_shop()
            elif remote == "9":
                query.insert_product_order()
            elif remote.lower() == "quit":
                break
            else:
                print("Неизвестное значение.")

        cur.close()
