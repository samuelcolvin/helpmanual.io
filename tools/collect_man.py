#!/usr/bin/env python3
import gzip
import hashlib
import re
from pathlib import Path
from textwrap import dedent

import chardet
from buildpg import Values

from .commands import command
from .db import to_json


@command
async def collect_man(pg):
    src = Path('/usr/share/man').resolve()

    man_id = 1
    async with pg.acquire() as conn:
        async with conn.transaction():
            print(f'items before insertion: {await conn.fetchval("select count(*) from raw_items")}')
            while True:
                checked, added, updated = 0, 0, 0
                man_dir = src / f'man{man_id}'
                if not man_dir.exists():
                    break
                for p in man_dir.iterdir():
                    if p.is_file() and p.suffix == '.gz':
                        v = await process_file(man_id, p, conn)
                        checked += 1
                        if v == 'updated':
                            updated += 1
                        elif v == 'added':
                            added += 1
                print(f'man={man_id} checked={checked} added={added} updated={updated}')
                man_id += 1

            print(f'items after insertion: {await conn.fetchval("select count(*) from raw_items")}')


async def process_file(man_id, path, conn):
    with gzip.open(str(path), mode='r') as f:
        raw = f.read()

    # if you're running it on ./data, also need to remove `and p.suffix == '.gz'` above
    # raw = path.read_bytes()
    new_hash = hashlib.sha256(raw).hexdigest()
    ref = get_ref(man_id, path)

    r = await conn.fetchrow(
        """
        select hash, version
        from raw_items 
        where type='man' and ref=$1 
        order by version desc 
        limit 1
        """, ref
    )
    if r:
        old_hash, version = r
    else:
        old_hash, version = None, -1
    if old_hash and new_hash == old_hash:
        # unchanged, not continuing
        return
    name = path.stem
    await conn.execute_b('insert into raw_items (:values__names) values :values', values=Values(
        type='man',
        ref=ref,
        version=version + 1,
        name=name,
        hash=new_hash,
        man_id=man_id,
        extra=to_json(get_extra(raw, name, man_id)),
        raw=raw
    ))
    return 'updated' if old_hash else 'added'


def get_ref(man_id, p):
    uri_name = re.sub(fr'\.{man_id}$', '', p.name)
    uri_name = re.sub(fr'\.{man_id}', '-', uri_name)
    return f'{man_id}/{uri_name}'


def get_extra(raw, name, man_id: int):
    description = revision_date = None
    extra1 = extra2 = extra3 = None
    head, man_comments = [], []
    in_description, reached_name = False, False
    prev_line = ''
    for lineb in raw.split(b'\n'):
        if len(head) >= 200:
            break

        try:
            line = prev_line + decode(lineb).strip()
        except UnicodeDecodeError:
            print(f'UnicodeDecodeError for {name}: {lineb}')
            break
        prev_line = ''
        if not line:
            continue
        elif line.startswith('.\\"'):
            if not head:
                # we only want the first comment
                man_comments.append(line[3:])
            continue
        elif line.startswith(('\'\\" ', '\\}', '\\{', '.if', '.  ')):
            continue
        elif line.startswith("'br") or line.startswith('.br'):
            prev_line = line[3:]
            continue

        line = re.sub(r'^\\& ', '', line)
        if re.search(r'^\.s[sh] ', line, flags=re.I):
            reached_name = True
        elif line.startswith('.TH'):
            th_line = line[4:].strip()
            th_items = [v.strip('"') for v in re.findall(r'(".*?"|\w+)(?: |$)', th_line)]
            if len(th_items) > 2:
                th_items = th_items[2:]
                try:
                    extra1 = groff_escape(th_items[0])
                    extra2 = groff_escape(th_items[1].strip('\\ &'))
                    extra3 = groff_escape(th_items[2].strip('\\ &'))
                except IndexError:
                    pass
        if revision_date is None and line.startswith('.Dd'):
            revision_date = line[4:]
            revision_date = re.sub(r'\$Mdocdate:(.*)\$', r'\1', revision_date).strip(' ')

        if reached_name:
            if in_description:
                if line.startswith('.Nm'):
                    description += line[4:]
                elif line.startswith('.Nd'):
                    description += ' - ' + line[4:]
                elif line.startswith('.'):
                    in_description = False
                else:
                    description += line
            elif description:
                pass
            elif not line.startswith('.'):
                description = line
                in_description = True
            elif line.startswith('.Nm'):
                description = line[4:]
                in_description = True
            elif line.startswith('.Nd'):
                description = line[4:]
                in_description = True
        head.append(line)

    if description is None and man_id == 3:
        # some man3 pages really don't have descriptions, eg. pcredemo
        description = name

    if description is None:
        so_line = next((l for l in head if l.startswith('.so ')), None)
        if so_line:
            # link_to = so_line[4:]
            # link_to, link_to_man_id = link_to.split('.', 1)
            # if '/' not in link_to:
            #     link_to = 'man{}/{}'.format(link_to_man_id, link_to)
            # self.links[self.get_uri_name(man_id, p)] = '/' + link_to.strip('/')
            return
        if len(head) < 2:
            # print(f'no description for {name}: small head')
            return
        else:
            # print(f'no description for {name} - not sure why!')
            return
            # raise RuntimeError('no description for {}\n"{}"'.format(p, '\n'.join(head)))

    description = re.sub(r'\\s[\-0-9]+', '', description.strip(' ')).replace('\\-', '-').strip(' -,')
    description = groff_escape(description)

    man_comments = (
        '\n'.join(man_comments)
            .replace('\"', '"')
            .replace('\r\n', '\n')
            .replace('-*- nroff -*-', '')
            .strip('\n"')
    )
    man_comments = dedent(man_comments)
    if len(man_comments) > 500:
        man_comments = man_comments[:497] + '...'

    auto_gen = ' Automatically generated by Pod', 'DO NOT MODIFY THIS FILE! ', 'auto-generated by docbook2man'
    if man_comments.startswith(auto_gen):
        man_comments = ''
    return dict(
        doc_date=revision_date,
        description=description,
        extra1=extra1,
        extra2=extra2,
        extra3=extra3,
        man_comments=man_comments,
    )


def decode(s, encoding='utf8', retry=False):
    try:
        return s.decode(encoding)
    except UnicodeDecodeError:
        alt_encoding = chardet.detect(s)['encoding']
        if alt_encoding and not retry:
            return decode(s, alt_encoding, True)
        else:
            raise


def groff_escape(s):
    s = re.sub(r'\\f[A-Z]', '', s)
    s = re.sub(r'\\&', '', s)
    s = re.sub(r'\\\(em', '', s)
    s = re.sub(r'\\s\+\d', '', s)
    s = re.sub(r'\\', '', s)
    return s
