from pathlib import Path

from app.db import Db

DATABASE_URL = str(Path(__file__).parent) + '/../../db.sqlite.test'

def get_db():
    db = Db(DATABASE_URL)
    db.raw('DELETE FROM sales')
    db.raw('DELETE FROM products')
    return db


def extract_ids(items):
    ids = []
    for item in items:
        if hasattr(item, 'id'):
            ids.append(item.id)
        else:
            ids.append(item['id'])
    return ids
