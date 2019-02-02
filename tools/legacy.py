#!/usr/bin/env python3
"""
TODO remove once a postgres time is the source of truth.
"""
import asyncio
import hashlib
import json
from pathlib import Path

from asyncpg import CharacterNotInRepertoireError
from buildpg import Values
from devtools import debug

from .commands import command


def to_json(**kwargs):
    return json.dumps({k: v for k, v in kwargs.items() if v is not None})


async def load_exec_raw(pg):
    print('loading execs...')
    extra_fields = 'help_arg', 'help_returncode', 'path', 'version_arg', 'version_returncode'
    values = []
    for p in Path('data/exec').iterdir():
        with p.open() as f:
            item = json.load(f)
        name = p.stem
        if item and name != item['name']:
            debug(p, item)
            raise RuntimeError("name doesn't match")

        hash = None
        if item:
            hash = hashlib.sha256('{help_msg}|{version_msg}'.format(**item).encode()).hexdigest()
        values.append(
            dict(
                type='exec',
                ref=name,
                name=name,
                hash=hash,
                extra=item and to_json(**{f: item.get(f) for f in extra_fields}),
                primary_text=item and item['help_msg'],
                secondary_text=item and item['version_msg'],
            )
        )

    async def insert(values):
        try:
            async with pg.acquire() as conn:
                await conn.execute_b('insert into raw_items (:values__names) values :values', values=Values(**values))
        except CharacterNotInRepertoireError:
            if 'primary_text' in values:
                values.pop('primary_text')
                values.pop('secondary_text')
                values['hash'] = None
                return await insert(values)
            raise

    async with pg.acquire() as conn:
        print(f'items before insertion: {await conn.fetchval("select count(*) from raw_items")}')

    await asyncio.gather(*[insert(v) for v in values])

    async with pg.acquire() as conn:
        print(f'items after insertion: {await conn.fetchval("select count(*) from raw_items")}')


async def load_man_raw(pg):
    with Path('data/man_metadata.json').open() as f:
        man_data = json.load(f)

    print(f'loading {len(man_data)} man pages...')
    root_dir = Path('data/man')
    values = []
    refs = set()
    for item in man_data:
        ref = '{}/{}'.format(item['man_id'], item['uri'].rsplit('/', 1)[1])
        if ref in refs:
            debug(item)
            continue
        refs.add(ref)
        raw = (root_dir / item['raw_path']).read_bytes()
        values.append(
            Values(
                ref=ref,
                name=item['name'],
                type='man',
                hash=hashlib.sha256(raw).hexdigest(),
                man_id=item['man_id'],
                extra=to_json(
                    extra1=item.get('extra1'),
                    extra2=item.get('extra2'),
                    short_description=item.get('description'),
                ),
                raw=raw
            )
        )
    del man_data

    async with pg.acquire() as conn:
        async with conn.transaction():
            print(f'items before insertion: {await conn.fetchval("select count(*) from raw_items")}')

            await conn.executemany_b('insert into raw_items (:values__names) values :values', values)

            print(f'items after insertion: {await conn.fetchval("select count(*) from raw_items")}')


async def load_package_raw(pg):
    print('loading packages...')
    extra_fields = 'automatic', 'dlocate-ls', 'dlocate-lsbin', 'dlocate-lsman', 'extra'
    values = []
    for p in Path('data/apt_packages').iterdir():
        with p.open() as f:
            item = json.load(f)
        name = p.stem
        if name != item['name']:
            debug(p, item)
            raise RuntimeError("name doesn't match")

        values.append(
            Values(
                ref=name,
                name=name,
                type='package',
                hash=hashlib.sha256(item['apt-show'].encode()).hexdigest(),
                extra=to_json(**{f: item.get(f) for f in extra_fields}),
                primary_text=item['apt-show'],
            )
        )

    async with pg.acquire() as conn:
        async with conn.transaction():
            print(f'items before insertion: {await conn.fetchval("select count(*) from raw_items")}')

            await conn.executemany_b('insert into raw_items (:values__names) values :values', values)

            print(f'items after insertion: {await conn.fetchval("select count(*) from raw_items")}')


@command
async def load_legacy(pg):
    await load_exec_raw(pg)
    await load_man_raw(pg)
    await load_package_raw(pg)
