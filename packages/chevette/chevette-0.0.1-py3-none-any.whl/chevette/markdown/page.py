import os
from chevette.utils.constants import OUTPUT_DIR
from .parser import MarkdownDocument


class Page(MarkdownDocument):

    def __init__(self, path):
        self.path = path
        self.is_page = True

    def _save_to_html(self):
        output_path = os.path.join(OUTPUT_DIR, self.html_filename)

        with open(output_path, 'w') as f:
            f.write(self.html)
