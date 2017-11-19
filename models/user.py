#slajd 41

from clcrypto import password_hash, generate_salt
from mysql.connector import connect


cnx = connect(user="root", password="coderslab",
              host="127.0.0.1", database="Baza")
cursor = cnx.cursor()

class User:
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return  self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password
    def set_password(self, password):
        salt = generate_salt()
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO Users(email, username, hashed_password)
                    VALUES(%s, %s, %s);"""
            values = (self.email, self.username, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.lastrowid
            #cnx.commit()
            return True
        else:
            sql = """UPDATE Users SET email='%s', username='%s', 
            hashed_password='%s' WHERE id=%s;"""
            values = (self.email, self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True
        return False

    @staticmethod
    def load_user_by_id(cursor, id):
        #sql = "SELECT * FROM Users WHERE id='%s'"
        sql = "SELECT * FROM Users WHERE id={}".format(id)
        #cursor.execute(sql, (id))
        cursor.execute(sql)
        data = cursor.fetchone()
        print(data)
        if data is not None:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT * FROM Users"
        ret=[]
        cursor.execute(sql)
        result = cursor.fetchall()

        #cursor.execute(sql)
        #results = str([row for row in cursor])
        #print(results)

        for row in result:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[2]
            loaded_user.email = row[1]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user.username)
            ret.append(loaded_user.email)
        return ret


u=User()
u.email = "ani@an"
u.username = "ann"
#print(u.id)
#print(u.hashed_password)
#print(u.set_password('kotek'))
#print(u.save_to_db(cursor))
#u.load_user_by_id(cursor,5)
print(u.load_all_users(cursor))

cnx.commit()
cursor.close()
cnx.close()

