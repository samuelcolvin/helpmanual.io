import json
import re
from pathlib import Path

from utils import man_to_txt, txt_to_html


class ExtractBuiltins:
    def __init__(self):
        self.html_root = Path('html_raw').resolve()

        text = man_to_txt(Path('./raw/man/man1/bash.1'))
        m = re.search('\n\nSHELL BUILTIN COMMANDS\n(.*?)\n\nRESTRICTED SHELL\n', text, flags=re.S)
        text = m.groups()[0]
        m = re.search('\n(\s{7}: \[arguments\].*)', text, flags=re.S)
        text = m.groups()[0]
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
        with Path('builtin_metadata.json').open('w') as f:
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
                first_line = line.strip(' ')
                full = True
                try:
                    s_end = first_line.index('.')
                except ValueError:
                    s_end = len(first_line)
                if s_end > 140:
                    full = False
                    s_end = 137
                    while first_line[s_end] != ' ':
                        s_end -= 1
                short_description = first_line[:s_end]
                if not full:
                    short_description += '...'
            if line.startswith(' ' * 20):
                description.append('<p class="indented">{}</p>'.format(line.strip(' ')))
            else:
                description.append('<p>{}</p>'.format(line.strip(' ')))
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

