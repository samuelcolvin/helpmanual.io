import asyncio
import os
from pathlib import Path

from buildpg import asyncpg

from .commands import command

pg_dsn = 'postgres://postgres@localhost:5432/helpmanual'


@command
async def reset_database(pg):
    if not (os.getenv('CONFIRM_DATABASE_RESET') == 'confirm' or input('Confirm database reset? [yN] ') == 'y'):
        print('cancelling')
    else:
        print('resetting database...')
        sql = Path('models.sql').read_text()
        async with pg.acquire() as conn:
            await conn.execute(sql)
        print('done.')


async def with_db(coro):
    async with asyncpg.create_pool_b(dsn=pg_dsn, min_size=2, max_size=200) as pg:
        async with pg.acquire() as conn:
            v = await conn.fetchval('select version()')
            print(f'pg version: {v}')
        await coro(pg)


def db_main(coro):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(with_db(coro))
