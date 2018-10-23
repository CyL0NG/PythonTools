import os
from html.parser import HTMLParser

indent = "  "


class TemplateError(Exception):
    pass


class HTMLTag:
    def __init__(self, idx, tag="", attrs="", data=""):
        self.tag = tag
        self.clses = []
        self.ids = []
        self.attrs = []
        for attr, value in attrs:
            if attr == 'class':
                self.clses += value.split(' ')
            elif attr == 'id':
                self.ids.append(value)
            elif attr == 'style':
                styles = value.split(';')
                style_value = {}
                for style in styles:
                    if not style:
                        continue
                    name, val = style.split(':')
                    style_value[name.strip()] = val.strip()
                self.attrs.append(f'style={str(style_value)}')
            else:
                if value:
                    self.attrs.append(f'{attr}="{value}"')
                else:
                    self.attrs.append(attr)
        self.idx = idx
        self.data = data
        self.type = "tag" if tag else 'data'

    def pug(self):
        if self.type == "data":
            return self.data

        text = f"{indent * self.idx}{self.tag}"
        new_line = False
        if len(self.attrs) > 2:
            new_line = True
        if len(self.attrs) != 0:
            if not new_line:
                text += '(' + ' '.join(self.attrs) + ')'
            else:
                text += '(\n'
                for attr in self.attrs:
                    text += f'{indent * (self.idx + 1)}{attr}\n'
                text += f'{indent * self.idx})'

        if self.clses:
            for cls in self.clses:
                text += f'.{cls}'
        if self.ids:
            for _id in self.ids:
                text += f'#{_id}'
        return text


class VueParser(HTMLParser):
    def error(self, message):
        print(message)

    def __init__(self):
        super().__init__()
        self.tags = []
        self.current_idx = 1

    def handle_starttag(self, tag, attrs):
        self.tags.append(HTMLTag(self.current_idx, tag, attrs))
        self.current_idx += 1

    def handle_endtag(self, tag):
        self.current_idx -= 1

    def handle_startendtag(self, tag, attrs):
        self.tags.append(HTMLTag(self.current_idx, tag, attrs))

    def handle_data(self, data):
        if data.strip():
            self.tags.append(HTMLTag(self.current_idx, data=data.strip()))


def trans2pug(content):
    parser = VueParser()
    parser.feed(content)

    previous = ""
    html = '<template lang="pug">'
    for tag in parser.tags:
        if previous == 'tag':
            if tag.type == 'tag':
                html += '\n' + tag.pug()
            else:
                html += ' ' + tag.pug()
        else:
            if tag.type == 'data':
                html += tag.pug()
            else:
                html += '\n' + tag.pug()
        previous = tag.type
    html += '\n</template>'
    lines = html.split('\n')
    return [f'{line}\n' for line in lines]


def separate_file(file):
    with open(file) as fp:
        lines = fp.readlines()
    if len(lines) == 0:
        raise TemplateError(f'empty file: {file}')
    if lines[0].strip() != '<template>':
        raise TemplateError(f'{file} template format error')
    end = -1
    for index, line in enumerate(lines):
        if line.rstrip() == '</template>':
            end = index
    if end == -1:
        raise TemplateError('no template end')
    return lines[1:end], lines[end+1:]


def trans_file(file):
    print(f'translating {file}')
    try:
        template, other = separate_file(file)
    except TemplateError:
        return
    pug = trans2pug(''.join(template))
    with open(file, 'w') as fp:
        fp.writelines(pug + other)


def trans_dir(directory):
    omits = ['App.vue']
    ext = '.vue'
    files = os.listdir(directory)
    for file in files:
        if os.path.isdir(f'{directory}/{file}'):
            trans_dir(f'{directory}/{file}')
        else:
            if file[-4:] == ext and file not in omits:
                trans_file(f'{directory}/{file}')


def main():
    path = "/home/cylong/workspace/ibsp_front/src"
    trans_dir(path)


if __name__ == "__main__":
    main()
