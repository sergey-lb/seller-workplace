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

    def _process_sorting_data(self, sorting):
        if sorting is None:
            sorting = {
                'column': 'id',
                'order': 'DESC'
            }
        else:
            self.validate_table_or_column_name(sorting['column'])
            if sorting['order'] != 'ASC':
                sorting['order'] = 'DESC'
        return sorting

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
        sorting = self._process_sorting_data(sorting)

        with self._open_db() as db:
            sql = f"SELECT * FROM {table}"
            if not with_deleted:
                sql += " WHERE deleted=0"
            sql += f" ORDER BY {sorting['column']} {sorting['order']}"
            items = db.cursor().execute(sql).fetchall()
            return items

    def find_by_column(self, table, *, column, value, sorting=None, with_deleted=False):
        self.validate_table_or_column_name(table)
        self.validate_table_or_column_name(column)
        sorting = self._process_sorting_data(sorting)

        with self._open_db() as db:
            sql = f"SELECT * FROM {table} WHERE {column} = :value"
            if not with_deleted:
                sql += " WHERE deleted=0"
            sql += f" ORDER BY {sorting['column']} {sorting['order']}"
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
            sql += f" ORDER BY {sorting['column']} {sorting['order']}"
            items = db.cursor().execute(sql, {'value': '%' + value + '%'}).fetchall()
            return items

    def insert(self, table, obj):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            attrs = obj.__dict__
            cols_str = ",".join(attrs.keys())
            vals_str = ":" + ", :".join(attrs.keys())
            sql = f"INSERT INTO {table} ({cols_str}) VALUES({vals_str})"
            cursor = db.cursor();
            cursor.execute(sql, attrs)
            return cursor.lastrowid

    def update(self, table, obj):
        self.validate_table_or_column_name(table)
        with self._open_db() as db:
            attrs = obj.__dict__
            sql_set = []
            for key, val in attrs.items():
                if key == 'id':
                    continue
                sql_set.append(key + ' = :' + val)

            sql = f"UPDATE {table} SET " + ",".join(sql_set) + " WHERE id = :id"
            db.cursor().execute(sql, attrs)

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