from .parser import MarkdownDocument
import os
from chevette.utils.constants import OUTPUT_DIR
from chevette.utils.helpers import folder_exists


class Article(MarkdownDocument):

    def __init__(self, path):
        self.path = path

    def _save_to_html(self):
        public_articles_dir = os.path.join(OUTPUT_DIR, 'articles')
        output_path = os.path.join(
            public_articles_dir, self.html_filename
        )
        if not folder_exists(public_articles_dir):
            os.mkdir(public_articles_dir)

        with open(output_path, 'w') as f:
            f.write(self.html)
