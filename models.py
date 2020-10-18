from clcrypto import hash_password
from psycopg2 import connect, OperationalError

DATABASE = "workshop"
USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"


class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, new_password):
        self.set_password(new_password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO Users(username, hashed_password)
                        VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                                   WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_data = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text, creation_date)
                        VALUES(%s, %s, %s, NOW()) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self.creation_data = cursor.fetchone()
            return True
        else:
            sql = """UPDATE Messages SET to_id=%s, from_id=%s, text=%s
                                   WHERE id=%s"""
            values = (self.to_id, self.from_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user):
        sql = f"SELECT id, from_id, to_id, text, creation_date FROM Messages WHERE to_id = {user.id}"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message.creation_data = creation_date
            messages.append(loaded_message)
        return messages


if __name__ == '__main__':
    cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    new_user = User('username', 'password')
    #(new_user.save_to_db(cursor)
    print(new_user.id)
    print(User.load_user_by_id(cursor, 3))
    second_user = User.load_user_by_id(cursor, 2)
    print(second_user.username)
    second_user.username = 'second_user'
    second_user.save_to_db(cursor)
    all_user = User.load_all_users(cursor)
    print(all_user)
    print(all_user[0].id)
    print(all_user[0].username)
    print(all_user[0].hashed_password)
    new_message = Message(2, 1, "Wiadomosc")
    answer = new_message.save_to_db(cursor)
    print(answer)
    print(Message.load_all_messages(cursor))
    print()
