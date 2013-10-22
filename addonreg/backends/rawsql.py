import traceback

from sqlalchemy import String, Index, Boolean
from sqlalchemy import Table, MetaData, create_engine, Column
from sqlalchemy.exc import OperationalError, TimeoutError
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text as sqltext, select, or_, and_

from addonreg import logger


_GET = sqltext("""\
SELECT addonid, sha256, registered
FROM hashes
WHERE addonid = :addonid
AND sha256 = :sha256
""")

_INSERT = sqltext("""\
INSERT INTO hashes
(addonid, sha256, registered)
VALUES (:addonid, :sha256, 1)
""")

_MULTIPLE_GET = """\
SELECT addonid, sha256, registered
FROM hashes
WHERE
"""

metadata = MetaData()

hash_table = Table(
    'hashes', metadata,
    Column('addonid', String(255), nullable=False, primary_key=True),
    Column('sha256', String(64), nullable=False, primary_key=True),
    Column('registered', Boolean(), default=True),
    Index('hash_idx', 'sha256', 'addonid', unique=True),
    mysql_engine='InnoDB', mysql_charset='utf8')


class RawSQLBackend(object):
    """A backend using RAW SQL queries."""

    def __init__(self, config=None, sqluri=None, create_tables=True,
                 pool_size=100, pool_recycle=60, pool_timeout=30,
                 max_overflow=10, pool_reset_on_return='rollback', **kw):
        self.config = config or {}
        self.sqluri = sqluri or config['SQLURI']
        if pool_reset_on_return.lower() in ('', 'none'):
            pool_reset_on_return = None

        if self.sqluri.startswith(('mysql', 'pymysql')):
            self._engine = create_engine(
                self.sqluri,
                pool_size=pool_size,
                pool_recycle=pool_recycle,
                pool_timeout=pool_timeout,
                pool_reset_on_return=pool_reset_on_return,
                max_overflow=max_overflow,
                logging_name='addonreg')

        else:
            self._engine = create_engine(sqluri, poolclass=NullPool)

        self._engine.echo = kw.get('echo', False)
        self.hashes = hash_table

        self.hashes.metadata.bind = self._engine
        if create_tables:
            self.hashes.create(checkfirst=True)

    def _safe_execute(self, *args, **kwds):
        """Execute an sqlalchemy query & log + raise an exception on failure"""
        try:
            return self._engine.execute(*args, **kwds)
        except (OperationalError, TimeoutError):
            err = traceback.format_exc()
            logger.error(err)
            raise

    def hash_exists(self, addon_id, hash_):
        res = self._safe_execute(_GET, addonid=addon_id, sha256=hash_)
        try:
            item = res.fetchone()
            return item is not None
        finally:
            res.close()

    def hashes_exists(self, addons):
        where = []

        for idx, sha in addons:
            where.append(and_(hash_table.c.addonid == idx,
                              hash_table.c.sha256 == sha,
                              hash_table.c.registered == 1))

        query = select([hash_table.c.addonid,
                        hash_table.c.sha256]).where(or_(*where))
        res = self._safe_execute(query)
        try:
            return res.fetchall()
        finally:
            res.close()

    def register_hash(self, addon_id, hash_):
        res = self._safe_execute(_INSERT, addonid=addon_id, sha256=hash_)
        res.close()

    def empty(self):
        pass
