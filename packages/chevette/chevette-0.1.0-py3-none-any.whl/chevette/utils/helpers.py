import sys
import os
from shutil import rmtree
from colorama import Fore, Style
from .constants import EXTENSIONS_NOT_ALLOWED


def is_markdown(file):
    return file.endswith('.md') or file.endswith('.markdown')


def is_extention_allowed(file):
    try:
        file_ext = file.split('.')[1]
    except IndexError:
        return False
    return file_ext not in EXTENSIONS_NOT_ALLOWED


def folder_exists(path):
    return os.path.isdir(path)


def print_error_and_exit(message):
    print(Fore.RED + message.strip())
    print(Style.RESET_ALL)
    sys.exit(1)


def clear_directory(_dir):
    for file in os.listdir(_dir):
        file_path = os.path.join(_dir, file)

        if is_file(file_path):
            os.unlink(file_path)
        elif folder_exists(file_path):
            rmtree(file_path)


def is_file(path):
    return os.path.isfile(path)
