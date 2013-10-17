import traceback

from sqlalchemy import String, Index, Boolean
from sqlalchemy import Table, MetaData, create_engine, Column
from sqlalchemy.exc import OperationalError, TimeoutError
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text as sqltext

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

    def __init__(self, config=None, sqluri=False, create_tables=False,
                 pool_size=100, pool_recycle=60, pool_timeout=30,
                 max_overflow=10, pool_reset_on_return='rollback', **kw):
        self.config = config or {}
        self.sqluri = sqluri or config['SQLURI']
        if pool_reset_on_return.lower() in ('', 'none'):
            pool_reset_on_return = None

        if self.sqluri.startswith(('mysql', 'pymysql')):
            self._engine = create_engine(
                sqluri,
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

    def _get_engine(self, service=None):
        return self._engine

    def _safe_execute(self, *args, **kwds):
        """Execute an sqlalchemy query & log + raise an exception on failure"""
        if hasattr(args[0], 'bind'):
            engine = args[0].bind
        else:
            engine = None

        if engine is None:
            engine = kwds.get('engine')
            if engine is None:
                engine = self._get_engine(kwds.get('service'))
            else:
                del kwds['engine']

        try:
            return engine.execute(*args, **kwds)
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

    def register_hash(self, addon_id, hash_):
        res = self._safe_execute(_INSERT, addonid=addon_id, sha256=hash_)
        res.close()
