import json
import sqlite3
import config
from vedis import Vedis


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False


def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            print('{} with {}'.format(user_id, db[user_id]))
            return db[user_id]
        except KeyError:
            return config.States.S_START.value  # значение по умолчанию - начало диалога


class SessionDb:

    def create_session_with_crypto(self, user_id, crypto):
        value = {
            'crypto': crypto,
            'price': '',
            'cur_site': '',
            'city': '',
            'marginality': ''
        }
        value = json.dumps(value)
        with Vedis(config.session_file) as db:
            try:
                db[user_id] = value
                return True
            except:
                # тут желательно как-то обработать ситуацию
                return False


    def get_session(self, user_id):
        with Vedis(config.session_file) as db:
            try:
                print('{} with {}'.format(user_id, db[user_id]))
                value = json.loads(db[user_id])
                return value
            except KeyError:
                return 'no session for this user'


    def update_session(self, user_id, crypto=None, price=None, cur_site=None, city=None, marginality=None):
        with Vedis(config.session_file) as db:
            try:
                print('{} with {}'.format(user_id, db[user_id]))
                value = db[user_id]
                value = json.loads(value)
                if crypto is not None:
                    value['crypto'] = crypto
                elif price is not None:
                    value['price'] = price
                elif cur_site is not None:
                    value['cur_site'] = cur_site
                elif city is not None:
                    value['city'] = city
                elif marginality is not None:
                    value['marginality'] = marginality
                value = json.dumps(value)
                db[user_id] = value
                return db[user_id]
            except KeyError:
                return 'no session for this user'


class DBHelper:
    def __init__(self, dbname="data.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.setup()

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS orders (id integer primary key, " \
                   "user text, " \
                   "crypto text, " \
                   "price text, " \
                   "cur_site text," \
                   "city text," \
                   "marginality text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_order(self, user, crypto, price, cur_site, city, marginality):
        stmt = "INSERT INTO orders (user, crypto, price, cur_site, city, marginality) VALUES (?, ?, ?, ?, ?, ?)"
        args = (user, crypto, price, cur_site, city, marginality)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_own_orders(self, username):
        stmt = "SELECT * FROM orders where user = (?)"
        args = (username,)
        items = []
        for row in self.conn.execute(stmt, args):
            items.append(row)
        print(items)
        return items

    def delete_order(self, id):
        stmt = "DELETE FROM orders WHERE id = (?)"
        args = (id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_all(self):
        stmt = "DELETE * FROM orders"
        self.conn.execute(stmt)
        self.conn.commit()

    def get_orders(self):
        stmt = "SELECT * FROM orders"
        items = []
        for row in self.conn.execute(stmt):
            items.append(row)
        print(items)
        return items

    def drop_table(self):
        stmt = "DROP TABLE orders"
        self.conn.execute(stmt)
        print('dropped')
        return 'done'
