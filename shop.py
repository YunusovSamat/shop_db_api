import sqlite3


class InsertData:
    def __init__(self, connect, cursor):
        self.con = connect
        self.cur = cursor
        self.sql = ""
        self.vars = dict()

    def valid_num(self, name_num):
        while True:
            num = input(name_num + ": ")
            if num.isdigit():
                if int(num) >= 0:
                    break
            else:
                print("Ошибка: введите число.")
        return num

    def pattern_insert(self):
        data = []
        for key in self.vars:
            if self.vars[key] == "int":
                data.append(self.valid_num(key))
            elif self.vars[key] == "str":
                data.append(input(key + ": "))

        try:
            self.cur.execute(self.sql, data)
        except sqlite3.DatabaseError as error:
            print("Ошибка", error)
        else:
            print("Запрос успешно выполнен")
            self.con.commit()

    def insert_catalog(self):
        self.sql = """\
        INSERT INTO catalog (name) 
        VALUES (?)
        """
        self.vars = {"name": "str"}
        print("Введите данные catalog.")
        self.pattern_insert()

    def insert_subcatalog(self):
        self.sql = """\
        INSERT INTO subcatalog (id_catalog, name) 
        VALUES (?, ?) 
        """
        self.vars = {
            "id_catalog": "int",
            "name": "str"
        }
        print("Введите данные subcatalog.")
        self.pattern_insert()


if __name__ == '__main__':
    con = sqlite3.connect("store.db")
    with con:
        cur = con.cursor()
        insert_data = InsertData(con, cur)
        # insert_data.insert_catalog()
        insert_data.insert_subcatalog()
        cur.close()
