import os
from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from colorama import Style, Fore
from pexpect import spawn

class Bash(Raw):
    has_content = True
    required_arguments = 0
    option_spec = {
        'norun': directives.flag
    }

    def run(self):
        import pdb; pdb.set_trace()
        command = '\n'.join(self.content)
        output = spawn(command).read()
        conv = Ansi2HTMLConverter(font_size='8pt', dark_bg=True)
        html = conv.convert(f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {command}{Fore.RESET}{Style.RESET_ALL}\n{output.decode("utf8").strip()}')
        self.content[0] = f'<div class="highlight", style="background-color:#000000;">{html}</div>'
        return super().run()

def setup(app):
    app.add_directive('bash', Bash)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
