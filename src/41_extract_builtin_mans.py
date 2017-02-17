#!/usr/bin/env python3.6
import json
import re
from pathlib import Path

from utils import man_to_txt, generate_description


class ExtractBuiltins:
    def __init__(self):
        self.html_root = Path('data/html').resolve()
        text = man_to_txt(Path('data/man/man1/bash.1'))
        m = re.search('\n\nSHELL BUILTIN COMMANDS\n(.*?)\n\nRESTRICTED SHELL\n', text, flags=re.S)
        text = m.groups()[0]
        m = re.search('\n(\s{7}: \[arguments\].*)', text, flags=re.S)
        text = m.groups()[0]
        # Path('bash-builtins.txt').write_text(text)
        regex = re.compile('^\s{7,8}((\S+).*?)(?=^\s{7,8}\S)', re.M | re.S)
        current = ''
        self.metadata = []
        for m in regex.finditer(text):
            item_content, item_name = m.groups()
            current += item_content
            if item_content.count('\n') == 1:
                continue
            self.save(item_name, current)
            current = ''
        with Path('data/builtin_metadata.json').open('w') as f:
            json.dump(self.metadata, f, indent=2, sort_keys=True)

    def save(self, name, content):
        lines = content.split('\n')
        short_description = ''
        synopsis = []
        description = []
        for line in lines:
            if not line:
                continue
            if not line.startswith(' '):
                synopsis.append('<p>{}</p>'.format(line))
                continue
            if not short_description:
                short_description = generate_description(line)
            prefix = '<p>'
            if line.startswith(' ' * 20):
                prefix = '<p class="indented">'
            line = re.sub('^(\S{,20})(\s{2,})', r'<b>\g<1></b>\2', line.strip(' '))
            line = re.sub('^(\S{,20})$', r'<b>\g<1></b>', line)
            line = re.sub(' {2,}', lambda m: '&nbsp;' * len(m.group()), line)
            description.append('{}{}</p>'.format(prefix, line))
        html = """\
<h2>NAME</h2>
{name} - {short_description}
<h2>SYNOPSIS</h2>
{synopsis}
<h2>DESCRIPTION</h2>
{description}
<h2>SEE ALSO</h2>
<p>This is extracted from the main <a href="/man1/bash">bash</a> man page, see there for more details.</p>
""".format(
            name=name,
            short_description=short_description,
            synopsis='\n'.join(synopsis),
            description='\n'.join(description)
        )
        out_file = self.html_root / 'builtins' / (name + '.html')
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html)
        info = {
            'name': name,
            'description': short_description,
            'uri': '/builtin/' + name,
            'raw_path': str(out_file.relative_to(self.html_root)),
        }
        self.metadata.append(info)

if __name__ == '__main__':
    ExtractBuiltins()
