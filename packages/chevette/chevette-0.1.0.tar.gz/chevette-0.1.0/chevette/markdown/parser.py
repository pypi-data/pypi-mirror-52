import os
import inspect
import misaka as m
import frontmatter as fm
from importlib.machinery import SourceFileLoader
from chevette.utils.constants import THEME_JINJA_ENV, SITE_CONFIG
from chevette.utils.helpers import print_error_and_exit
from jinja2.exceptions import TemplateNotFound


class MarkdownDocument(object):

    path = None
    is_page = False
    metadata = None
    content = None
    html_filename = None

    def _parse(self):
        _article = fm.load(self.path)
        self.metadata = _article.metadata
        self.content = _article.content

    def _render(self):
        layout = self.metadata.get('layout', 'post')
        site_config = self._load_config_from_module()
        config = {**site_config, **self.metadata}

        try:
            template = THEME_JINJA_ENV.get_template(f'{layout}.html.jinja2')
        except TemplateNotFound as e:
            err_msg = f"""
            [Error]
            Unable to compile {self.path}.
            Could not find the following layout template: {e.name}.
            Make sure the spelling is correct or that a file named {e.name}
            sits under the theme directory.
            """
            print_error_and_exit(err_msg)
        else:
            self.html = template.render(
                content=m.html(self.content), **config
            )

    def render_html(self):
        self._parse()
        self._render()
        self._save_to_html()

    @property
    def html_filename(self):
        filename, _ = os.path.splitext(os.path.basename(self.path))
        return f'{filename}.html'

    def _load_config_from_module(self):
        config_module = SourceFileLoader('config', SITE_CONFIG).load_module()
        site_config = {'site': {}}
        config_settings = [
            (k.lower(), v) for k, v in inspect.getmembers(config_module)
            if k.isupper()
        ]
        site_config['site'].update(config_settings)
        return site_config
