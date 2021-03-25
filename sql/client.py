import json

from aiosqlite import connect

from .dataclasses import ChangeDict, User


class AsyncSQLiteClient:

    @property
    def execute(self):
        return self.conn.execute

    @property
    def users(self):
        return self.cache.values()

    def __init__(self, path: str = "database.sqlite.db"):
        self.conn = connect(path, isolation_level=None)
        self.cache = {}
        self.options = ChangeDict()

    async def create(self):
        async with self.conn.execute(
                """CREATE TABLE IF NOT EXISTS BANK(USER_ID INTEGER PRIMARY KEY, BALANCE INTEGER NOT NULL, STOCK INTEGER NOT NULL)"""):
            pass
        async with self.conn.execute("""CREATE TABLE IF NOT EXISTS OPTIONS(NAME TEXT PRIMARY KEY, VALUE TEXT NOT NULL)"""):
            pass

    async def load(self):
        async with self.conn.execute("""SELECT USER_ID, BALANCE, STOCK FROM BANK""") as cursor:
            async for row in cursor:
                user_id, bal, stock = row
                self.cache[user_id] = User(user_id, stock, bal)
                self.cache[user_id]._new = False
        async with self.conn.execute("""SELECT NAME, VALUE FROM OPTIONS""") as cursor:
            self.options = ChangeDict({k: json.loads(v) async for k, v in cursor})

    async def _await(self, actual_await=None):
        if actual_await is not None:
            await actual_await
        return self

    def __await__(self):
        to_await = None
        if not self.conn._connection:
            to_await = self.conn
        return self._await(to_await).__await__()

    def get(self, user_id: int):
        return self.cache.setdefault(user_id, User(user_id, 0, 0))

    async def save(self):
        changed_users = []
        for user in self.cache.values():
            if user._changed or user._new:
                changed_users.append((user.user_id, user.balance, user.stock))
                user._changed = False
                user._new = False
        async with self.conn.executemany("""INSERT OR REPLACE INTO BANK(USER_ID, BALANCE, STOCK) VALUES(?, ?, ?)""", changed_users):
            pass
        if self.options.changed:
            async with self.conn.executemany("""INSERT OR REPLACE INTO OPTIONS(NAME, VALUE) VALUES (?, ?)""",
                                             [((k, json.dumps(v)) for k, v in self.options.items())]):
                pass
            self.options.changed = False
        await self.conn.commit()
