import sqlite3


class Db:
    _instance = None

    _url = None

    def __init__(self, db_url):
        self._url = db_url

    def _open_db(self):
        db = sqlite3.connect(self._url)
        db.row_factory = sqlite3.Row
        return db

    def validate_table_or_column_name(self, name):
        name_alnum = list(filter(lambda c: c.isalnum() or c == '_', name))

        is_valid = len(name_alnum) == len(name)
        if not is_valid:
            raise Exception(
                f"Table {name} is not valid table name, "
                "only alphanumerical characters and underscore in table names is allowed"
            )

    def _add_sorting_part(self, sql, sorting):
        if sorting is None:
            sorting = {
                'column': 'id',
                'order': 'DESC'
            }
        else:
            self.validate_table_or_column_name(sorting['column'])
            if sorting['order'] != 'ASC':
                sorting['order'] = 'DESC'

        sql += f" ORDER BY {sorting['column']} {sorting['order']}"
        return sql

    def find(self, table, item_id, *, with_deleted=False):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            sql = f"SELECT * FROM {table} WHERE id = :id";
            if not with_deleted:
                sql += " AND deleted=0"
            item = db.cursor().execute(sql, {'id': item_id}).fetchone()
            return item

    def find_all(self, table, sorting=None, *, with_deleted=False):
        self.validate_table_or_column_name(table)

        with self._open_db() as db:
            sql = f"SELECT * FROM {table}"
            if not with_deleted:
                sql += " WHERE deleted=0"
            sql = self._add_sorting_part(sql, sorting)
            items = db.cursor().execute(sql).fetchall()
            return items

    def find_by_column(self, table, *, column, value, sorting=None, with_deleted=False):
        self.validate_table_or_column_name(table)
        self.validate_table_or_column_name(column)

        with self._open_db() as db:
            sql = f"SELECT * FROM {table} WHERE {column} = :value"
            if not with_deleted:
                sql += " AND deleted=0"
            sql = self._add_sorting_part(sql, sorting)
            items = db.cursor().execute(sql, {'value': value}).fetchall()
            return items

    def find_by_column_like(self, table, *, column, value, sorting=None, with_deleted=False):
        self.validate_table_or_column_name(table)
        self.validate_table_or_column_name(column)
        with self._open_db() as db:
            sql = f"SELECT * FROM {table}"
            sql += f" WHERE {column} LIKE :value"
            if not with_deleted:
                sql += " AND deleted = 0"
            sql = self._add_sorting_part(sql, sorting)
            items = db.cursor().execute(sql, {'value': '%' + value + '%'}).fetchall()
            return items

    def insert(self, table, item):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            if type(item) is not dict:
                item = item.__dict__

            cols_str = ",".join(item.keys())
            vals_str = ":" + ", :".join(item.keys())
            sql = f"INSERT INTO {table} ({cols_str}) VALUES({vals_str})"
            cursor = db.cursor();
            cursor.execute(sql, item)
            return cursor.lastrowid

    def update(self, table, item):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            if type(item) is not dict:
                item = item.__dict__

            sql_set = []
            for key in item.keys():
                if key == 'id':
                    continue
                sql_set.append(key + ' = :' + key)

            sql = f"UPDATE {table} SET " + ",".join(sql_set) + " WHERE id = :id"
            db.cursor().execute(sql, item)

    def mark_deleted(self, table, item_id):
        self.update(table, {
            'deleted': 1,
            'id': item_id
        })

    def delete(self, table, item_id):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            sql = f"DELETE FROM {table} WHERE id = :id"
            db.cursor().execute(sql, {'id': item_id})

    def raw(self, sql, params=None):
        with self._open_db() as db:
            if params is None:
                params={}
            stmt=db.cursor().execute(sql, params)
            return stmt