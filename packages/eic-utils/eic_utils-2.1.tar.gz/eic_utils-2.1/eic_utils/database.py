import sqlite3, pickle, time

from eic_utils.colorful_str import colorful_str
from eic_utils.procedure import procedure

one_million_years = 1e6 * 365.2422 * 86400

dict_factory = lambda cursor, row: {
        col[0]: row[idx] for idx, col in enumerate(cursor.description)}

class DataBase(object):
    def __init__(self, path, tables=[], *, log_mode='cmd', log_file=None):  # {{{
        """ initialize databse """

        self.path = path
        self.log_mode = log_mode
        self.log_file = log_file
        self.log_file_f = None
        with procedure('init database \'(#y){}(#)\''.format(
            self.path), same_line=False):

            self.conn = sqlite3.connect(self.path, check_same_thread=False)
            self.conn.row_factory = dict_factory
            self.cursor = self.conn.cursor()

        with procedure('init global table'):
            self.create_table('global', ['key TEXT NOT NULL PRIMARY KEY',
                'value BLOB', 'time DOUBLE'])
    # }}}

    def __del__(self):  # {{{
        if self.log_file_f:
            self.log_file_f.close()
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
    # }}}

    def add_log(self, cmd, *args, limitation=200):  # {{{
        if self.log_mode == 'cmd':
            print(colorful_str(
                '(#g)SQL(#): >> (#b){} {}'.format(cmd, args)[:limitation]))
        if self.log_file:
            if self.log_file_f is None:
                self.log_file_f = open(self.log_file, 'a')
                self.cnt = 0
            self.cnt += 1
            self.log_file_f.write('#{}: {} {}\n'.format(self.cnt, cmd, args))
    # }}}

    def sync(self):  # {{{
        self.conn.commit()
    # }}}

    def execute(self, cmd, *args, sync=True):  # {{{
        self.add_log(cmd, *args)
        result = self.cursor.execute(cmd, *args)
        if sync:
            self.sync()
        return result
    # }}}

    def select(self, name, limitation=None, keys='*', return_dict=True, extra=None):  # {{{
        """ select from table

            Args:
                name: table name
                limitation: dict follow this format example:
                    limitation = {
                        'a>': 2,
                        'b=': 3,
                        'c<=', 4,
                    }
                keys: list, tuple or set, return which keys of values
                return_dict: return list of dict or list of list
        """
        if isinstance(keys, str):
            keys = [keys]
        cmd = 'SELECT {} FROM \'{}\''.format(','.join(keys), name)
        values = []
        if limitation is not None:
            where = 'WHERE {}'.format(
                ' and '.join(['{}?'.format(key) for key in limitation.keys()])
            )
            cmd = ' '.join([cmd, where])
            values = list(limitation.values())
        if isinstance(extra, str):
            cmd = ' '.join([cmd, extra])

        result = self.execute(cmd, values).fetchall()
        if not return_dict:
            result = [list(x.values()) for x in result]
        return result
    # }}}

    def insert(self, name, rows, force=False):  # {{{
        """ insert into table
            Args:
                name: table name
                rows: dict or list of dict, keys and values of dict are
                    keys and values in tables
        """
        if isinstance(rows, dict):
            rows = [rows]

        data = rows[0]
        place_holder = ','.join([
            '(' + ','.join(['?'] * len(data.keys())) + ')'] * len(rows))

        cmd = 'INSERT OR {} INTO \'{}\' ({}) VALUES {}'.format(
            'REPLACE' if force else 'IGNORE',
            name, ','.join(data.keys()), place_holder
        )

        values = []
        for data in rows:
            values += data.values()
        return self.execute(cmd, tuple(values), sync=True)
    # }}}

    def update(self, name, data, limitation=None):  # {{{
        """ update table set
            Args:
                name: table name
                rows: dict, keys and values of dict are keys and values in tables
                limitation: dict follow this format example:
                    limitation = {
                        'a>': 2,
                        'b=': 3,
                        'c<=', 4,
                    }
        """
        cmd = 'UPDATE {} SET {}'.format(
            name, ','.join(['{}=?'.format(key) for key in data.keys()])
        )
        values = list(data.values())
        if limitation is not None:
            where = 'WHERE {}'.format(
                ' and '.join(['{}?'.format(key) for key in limitation.keys()])
            )
            cmd = ' '.join([cmd, where])
            values += list(limitation.values())
        return self.execute(cmd, values, sync=True)

    # }}}

    def delete(self, name, limitation=None):  # {{{
        """ delete from table
            Args:
                name: table name
                limitation: dict follow this format example:
                    limitation = {
                        'a>': 2,
                        'b=': 3,
                        'c<=', 4,
                    }
        """
        cmd = 'DELETE FROM {}'.format(name)
        values = []
        if limitation is not None:
            where = 'WHERE {}'.format(
                ' and '.join(['{}?'.format(key) for key in limitation.keys()])
            )
            cmd = ' '.join([cmd, where])
            values += list(limitation.values())
        return self.execute(cmd, values, sync=True)
    # }}}

    def count(self, name, limitation=None):  # {{{
        """ select from table

            Args:
                name: table name
                limitation: dict follow this format example:
                    limitation = {
                        'a>': 2,
                        'b=': 3,
                        'c<=', 4,
                    }
        """
        cmd = 'SELECT COUNT(*) FROM \'{}\''.format(name)
        values = []
        if limitation is not None:
            where = 'WHERE {}'.format(
                ' and '.join(['{}?'.format(key) for key in limitation.keys()])
            )
            cmd = ' '.join([cmd, where])
            values = list(limitation.values())

        return self.execute(cmd, values).fetchall()[0][0]
    # }}}

    def create_table(self, name, sql):  # {{{
        """ CREATE TABLE IF NOT EXISTS """
        if isinstance(sql, str):
            sql = [sql]
        cmd = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(name, ','.join(sql))
        self.execute(cmd, sync=True)
    # }}}

    def drop_table(self, name):  # {{{
        """ DROP TABLE """
        cmd = 'DROP TABLE {}'.format(name)
        return self.execute(cmd, sync=True)
    # }}}

    def get_global(self, key, default=None):  # {{{
        """ get value of key in db, if not exists return default """
        data = self.select('global', keys='value', limitation={
            'key=': key, 'time>': time.time()}, return_dict=False)
        if len(data) == 0:
            return default
        return pickle.loads(data[0][0])
    # }}}

    def set_global(self, key, value, expired_time=one_million_years):  # {{{
        """ set value of key in db, expired in expired_time later """
        self.insert('global', {'key': key, 'value': pickle.dumps(value),
                               'time': time.time() + expired_time}, force=True)
    # }}}
