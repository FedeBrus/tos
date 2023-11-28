class Htmlw:
    def __init__(self, htmlpath):
        self.path = htmlpath

    def open_tags(self, *tags):
        h = open(self.path, 'a')

        for tag in tags:
            h.write(f'<{tag}>')

        h.close()

    def close_tags(self, *tags):
        h = open(self.path, 'a')

        for tag in tags:
            h.write(f'</{tag}>')

        h.close()

    def tag_content(self, tag, content):
        h = open(self.path, 'a')
        h.write(f'<{tag}>{content}</{tag}>')
        h.close()

    def write(self, string):
        h = open(self.path, 'a')
        h.write(string)
        h.close()

    def clear(self):
        h = open(self.path, 'w')
        h.write('')
        h.close()

    def write_file_as_is(self, filepath):
        h = open(self.path, 'a')
        f = open(filepath, 'r')
        h.write('<div><pre>')
        lines = f.readlines()

        for line in lines:
            for char in line:
                if char == '\n':
                    h.write('<br>')
                elif char == '\t':
                    h.write('&emsp')
                else:
                    h.write(char)

        h.write('</pre></div>')
        h.close()
        f.close()