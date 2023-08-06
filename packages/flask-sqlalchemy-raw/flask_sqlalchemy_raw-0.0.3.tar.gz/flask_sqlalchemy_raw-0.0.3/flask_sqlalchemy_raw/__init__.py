"""
usage:
flask_sqlalchemy execute raw sql.

sample:
from functools import partial
fetchone = partial(fetchone, db)
"""

from contextlib import contextmanager
from typing import Tuple, List, Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import ResultProxy

row_proxy_2_dict = lambda row_proxy: dict(row_proxy.items())


def fetchone(sql_str: str, db: SQLAlchemy) -> Tuple:
    return db.engine.execute(sql_str).fetchone()


def fetchone_dict(sql_str: str, db: SQLAlchemy) -> Dict:
    _records: ResultProxy = db.engine.execute(sql_str)
    return row_proxy_2_dict(_records)


def fetchall_dict(sql_str: str, db: SQLAlchemy) -> List[Dict]:
    _records: ResultProxy = db.engine.execute(sql_str)
    return list(map(row_proxy_2_dict, _records))


def total_number(sql_str: str, db: SQLAlchemy) -> int:
    """
    usage:
    total: int = total_items('select count(*) from finance_approval_list')

    used for:
    count item total number.
    :param sql_str:
    :param db:
    :return:
    """
    result: Tuple = fetchone(sql_str, db)
    return int(result[0]) if result else 0


@contextmanager
def create_cursor(engine: SQLAlchemy.engine):
    """
    usage:
    with create_cursor(url, encoding='utf-8', echo=True) as c:
        result = cursor.fetchall()
        connection.commit()

    :param engine:
    :return:
    """
    connection = engine.raw_connection()
    cursor = connection.cursor()
    try:
        yield cursor
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
