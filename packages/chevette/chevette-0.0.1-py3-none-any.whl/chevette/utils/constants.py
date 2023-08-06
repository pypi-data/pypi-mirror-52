from jinja2 import Environment, FileSystemLoader
from os import getcwd
from os.path import dirname, abspath, join


CUR_DIR = getcwd()
VERSION = '0.0.1'
TEMPLATES_DIR = join(
    dirname(dirname(abspath(__file__))), 'templates'
)
SITE_CONFIG = join(CUR_DIR, 'settings.py')
ARTICLES_DIR = 'articles'
OUTPUT_DIR = join(CUR_DIR, 'public')
LAYOUTS_DIR = join(TEMPLATES_DIR, 'layouts')
THEME_DIR = join(CUR_DIR, 'theme')
THEME_JINJA_ENV = Environment(
    loader=FileSystemLoader(THEME_DIR),
    trim_blocks=True
)

EXTENSIONS_NOT_ALLOWED = (
    'py',
    'yml',
    'yaml'
    'toml'
    'ini',
    'php',
    'c',
    'cpp',
    'go',
    'lock',
    'json'
)
