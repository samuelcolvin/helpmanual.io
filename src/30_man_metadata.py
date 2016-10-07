import json
import re
from operator import itemgetter
from pathlib import Path


class ManMetadata:
    def __init__(self):
        self.raw_man = Path('./raw/man')
        self.data = []
        for man_id in range(1, 9):
            dir = self.raw_man / 'man{}'.format(man_id)
            self.process_dir(dir, man_id)
            # break
        self.data.sort(key=itemgetter('uri'))
        with Path('man_metadata.json').open('w') as f:
            json.dump(self.data, f, indent=2, sort_keys=True)

    def process_dir(self, p: Path, man_id: int):
        print('processing {}...'.format(p))
        for pp in p.iterdir():
            if pp.is_file():
                self.process_file(pp, man_id)

    def process_file(self, p: Path, man_id: int):
        name = p.name[:p.name.rfind('.')]
        description = revision_date = None
        extra1 = extra2 = extra3 = None
        head, man_comments = [], []
        in_description, reached_name = False, False
        with p.open() as f:
            prev_line = ''
            while len(head) < 200:
                try:
                    line = prev_line + next(f).strip()
                except UnicodeDecodeError:
                    print('UnicodeDecodeError for {}'.format(p))
                    break
                except StopIteration:
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
                            extra1 = th_items[0]
                            extra2 = th_items[1].strip('\ &')
                            extra3 = th_items[2].strip('\ &')
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
            if next((l for l in head if l.startswith('.so ')), None):
                return
            if len(head) < 2:
                return
            raise RuntimeError('no description for {}\n"{}"'.format(p, '\n'.join(head)))

        description = description.strip(' ')
        description = re.sub(r'\\s[\-0-9]+', '', description)
        description = description.replace('\\-', '-')
        # if description.lower().startswith(name + ' '):
        #     description = description[len(name) + 1:]
        # elif ' - ' in description[:30]:
        #     description = description[description.index(' - ') + 3:]
        description = description.strip(' -,')

        man_comments = (
            '\n'.join(man_comments)
            .replace('\"', '"')
            .replace('\r\n', '\n')
            .replace('-*- nroff -*-', '')
            .strip('\n"')
        )
        if len(man_comments) > 400:
            man_comments = man_comments[:397] + '...'

        if '\n' not in man_comments:
            man_comments = man_comments.strip(' ')

        auto_gen = ' Automatically generated by Pod', 'DO NOT MODIFY THIS FILE! ', 'auto-generated by docbook2man'
        if man_comments.startswith(auto_gen):
            man_comments = ''

        data = dict(
            name=name,
            raw_path=str(p.relative_to(self.raw_man)),
            uri='/man{}/{}'.format(man_id, name),
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


if __name__ == '__main__':
    ManMetadata()
