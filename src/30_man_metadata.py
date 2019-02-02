#!/usr/bin/env python3
from textwrap import dedent

import chardet
import json
import re
from operator import itemgetter
from pathlib import Path


def decode(s, encoding='utf8', retry=False):
    try:
        return s.decode(encoding)
    except UnicodeDecodeError:
        alt_encoding = chardet.detect(s)['encoding']
        if alt_encoding and not retry:
            return decode(s, alt_encoding, True)
        else:
            raise


class ManMetadata:
    def __init__(self):
        self.raw_man = Path('data/man')
        self.data = []
        self.links = {}
        self.uris = set()
        man_id = 1
        while True:
            dir = self.raw_man / 'man{}'.format(man_id)
            if not dir.exists():
                break
            self.process_dir(dir, man_id)
            man_id += 1
        self.data.sort(key=itemgetter('uri'))
        with Path('data/man_metadata.json').open('w') as f:
            json.dump(self.data, f, indent=2, sort_keys=True)
        with Path('data/man_links.json').open('w') as f:
            json.dump(self.links, f, indent=2, sort_keys=True)

    def process_dir(self, p: Path, man_id: int):
        print('{}...'.format(p))
        for pp in p.iterdir():
            if pp.is_file():
                self.process_file(pp, man_id)

    def process_file(self, p: Path, man_id: int):
        name = p.name[:p.name.rfind('.')]
        description = revision_date = None
        extra1 = extra2 = extra3 = None
        head, man_comments = [], []
        in_description, reached_name = False, False
        with p.open('rb') as f:
            prev_line = ''
            while len(head) < 200:
                try:
                    lineb = next(f)
                except StopIteration:
                    break
                try:
                    line = prev_line + decode(lineb).strip()
                except UnicodeDecodeError:
                    print('UnicodeDecodeError for {}: {}'.format(p, lineb))
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

                line = re.sub('^\\\& ', '', line)
                if re.search('^\.s[sh] ', line, flags=re.I):
                    reached_name = True
                elif line.startswith('.TH'):
                    th_line = line[4:].strip()
                    th_items = [v.strip('"') for v in re.findall('(".*?"|\w+)(?: |$)', th_line)]
                    if len(th_items) > 2:
                        th_items = th_items[2:]
                        try:
                            extra1 = self.groff_escape(th_items[0])
                            extra2 = self.groff_escape(th_items[1].strip('\ &'))
                            extra3 = self.groff_escape(th_items[2].strip('\ &'))
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
                link_to = so_line[4:]
                link_to, link_to_man_id = link_to.split('.', 1)
                if '/' not in link_to:
                    link_to = 'man{}/{}'.format(link_to_man_id, link_to)
                self.links[self.get_uri_name(man_id, p)] = '/' + link_to.strip('/')
                return
            if len(head) < 2:
                print(f'no description for {p}: small head')
                return
            else:
                print(f'no description for {p} - not sure why!')
                return
                # raise RuntimeError('no description for {}\n"{}"'.format(p, '\n'.join(head)))

        description = re.sub(r'\\s[\-0-9]+', '', description.strip(' ')).replace('\\-', '-').strip(' -,')
        description = self.groff_escape(description)

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
        uri = self.get_uri_name(man_id, p)
        assert uri not in self.uris
        self.uris.add(uri)
        data = dict(
            name=name,
            raw_path=str(p.relative_to(self.raw_man)),
            uri=uri,
            man_id=man_id,
            doc_date=revision_date,
            description=description,
            extra1=extra1,
            extra2=extra2,
            extra3=extra3,
            man_comments=man_comments,
        )
        data = {k: v for k, v in data.items() if v}
        self.data.append(data)

    @staticmethod
    def groff_escape(s):
        s = re.sub(r'\\f[A-Z]', '', s)
        s = re.sub(r'\\&', '', s)
        s = re.sub(r'\\\(em', '', s)
        s = re.sub(r'\\s\+\d', '', s)
        s = re.sub(r'\\', '', s)
        return s

    def get_uri_name(self, man_id, p):
        uri_name = re.sub('\.{}$'.format(man_id), '', p.name)
        uri_name = re.sub('\.{}'.format(man_id), '-', uri_name)
        return '/man{}/{}'.format(man_id, uri_name)


if __name__ == '__main__':
    ManMetadata()

