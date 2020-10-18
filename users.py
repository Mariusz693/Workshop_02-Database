import argparse
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import User

DATABASE = "workshop"
USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()
# print(args.username)


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Password is to short")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User added")
        except UniqueViolation as e:
            print("Exception, ", e)


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("Not user in database")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is to short")
        else:
            try:
                user.hashed_password = new_pass
                user.save_to_db(cursor)
                print("Password changed")
            except Exception:
                print("Error")
    else:
        print("Incorrect password")


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("Not user in database")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User delete")
    else:
        print("Incorrect password")


def list_user(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(str(user.id) + ". " + user.username)


if __name__ == '__main__':
    try:
        cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_user(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as e:
        print("Operation error, ", e)
