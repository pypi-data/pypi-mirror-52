import os
from chevette.server.server import ChevetteServer
from chevette.exceptions import NoConfigError
from chevette.utils.constants import (
    ARTICLES_DIR,
    OUTPUT_DIR,
    TEMPLATES_DIR,
    SITE_CONFIG
)
from chevette.markdown import Page, Article
from shutil import copy2, copytree
from chevette.utils.helpers import (
    is_file,
    is_markdown,
    is_extention_allowed,
    folder_exists,
    clear_directory,
    print_error_and_exit,
)


class Chevette(object):

    @classmethod
    def serve(cls):

        try:
            cls._check_config_file()
        except NoConfigError as e:
            print_error_and_exit(e.error_msg)

        try:
            config = cls._load_config()
            port = config['site'].get('port', 8080)
            print(f'Starting server on localhost using port {port}...')
            httpd = ChevetteServer(config, '127.0.0.1', port)
            print('Running server ...')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down server ...')
            httpd.socket.close()

    @classmethod
    def build(cls):

        try:
            cls._check_config_file()
        except NoConfigError as e:
            print_error_and_exit(e.error_msg)
        else:
            cls._create_output_dir()

            other_files = cls._get_pages_and_other_files()

            for file in other_files:
                if is_markdown(file):
                    page = Page(file)
                    page.render_html()
                else:
                    copy2(file, OUTPUT_DIR)

            articles = cls._get_all_articles()

            for article in articles:
                article.render_html()

    @classmethod
    def new(cls, path, force):
        """
        create the basic folder structure necessary
        to the creation of a blog.
        /*
            articles -> where the blog posts will be stored (in markdown)
            public -> where the final site will be generated (in html)
        */
        """

        if folder_exists(path) and path != '.':

            err_msg = f"""
            [Error]: Could not create directory.
            Path ({os.path.abspath(path)}) Already Exists.
            Please make sure the directory is empty or use --force
            to overwrite the files.
            """

            if force:
                print(f'Overwriting content inside {path}')
                clear_directory(path)
                print('Done !')
                return cls._generate_boilerplate(path)

            print_error_and_exit(err_msg)

        else:
            cls._generate_boilerplate(path)

    def _get_all_articles(path=ARTICLES_DIR):
        return (
            Article(os.path.abspath(os.path.join(ARTICLES_DIR, article)))
            for article in os.listdir(ARTICLES_DIR)
            if is_file(os.path.join(ARTICLES_DIR, article))
            and is_markdown(article) # noqa W503
        )

    def _generate_boilerplate(path):
        print('Generating default folder structure ...')

        if path != '.':
            os.mkdir(path)

        for fd in os.listdir(TEMPLATES_DIR):
            src = os.path.join(TEMPLATES_DIR, fd)
            if is_file(src):
                copy2(src, path)

            if folder_exists(src):
                dest = os.path.join(path, fd)
                copytree(src, dest)

        print('Done !')

    def _get_pages_and_other_files():
        cur_dir = os.getcwd()
        return (
           os.path.join(cur_dir, f) for f in os.listdir(cur_dir) # noqa E121
           if is_file(os.path.join(cur_dir, f))
           and is_extention_allowed(f) # noqa W503
        )

    def _create_output_dir():
        if not folder_exists(OUTPUT_DIR):
            os.mkdir(os.path.join(os.getcwd(), OUTPUT_DIR))
        else:
            clear_directory(OUTPUT_DIR)

    def _check_config_file():
        if not is_file(SITE_CONFIG):
            raise NoConfigError

    def _load_config():
        from importlib.machinery import SourceFileLoader
        import inspect

        config_module = SourceFileLoader('config', SITE_CONFIG).load_module()
        site_config = {'site': {}}
        config_settings = [
            (k.lower(), v) for k, v in inspect.getmembers(config_module)
            if k.isupper()
        ]
        site_config['site'].update(config_settings)
        return site_config
