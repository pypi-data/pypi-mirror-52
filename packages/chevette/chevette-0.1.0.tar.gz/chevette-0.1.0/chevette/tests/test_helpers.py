import pytest
from chevette.utils.helpers import (
    is_markdown,
    is_extention_allowed,
    print_error_and_exit,
    folder_exists,
    clear_directory,
    is_file,
)
from chevette.utils.constants import EXTENSIONS_NOT_ALLOWED


def escape_ansi(line):
    import re
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def test_is_markdown():
    assert is_markdown('hello.md') == True
    assert is_markdown('hello.markdown') == True
    assert is_markdown('pipfile') == False


def test_is_extension_allowed():
    assert is_extention_allowed('some_file_without_extension') == False
    assert is_extention_allowed('index.html') == True
    for ext in EXTENSIONS_NOT_ALLOWED:
        filename = 'test.' + ext
        assert is_extention_allowed(filename) == False


def test_print_error_and_exit(capsys):
    error_message = 'Some error message'
    with pytest.raises(SystemExit):
        print_error_and_exit(error_message)
    captured = capsys.readouterr()
    escaped_output = escape_ansi(captured.out)
    assert escaped_output.rstrip() == error_message


def test_folder_exists(temp_dir):
    assert folder_exists(temp_dir.path) == True
    assert folder_exists(temp_dir.file1) == False


def test_clear_directory(temp_dir):
    import os
    full_dir_content_count = len(os.listdir(temp_dir.path))
    assert full_dir_content_count != 0
    clear_directory(temp_dir.path)
    empty_dir_content_count = len(os.listdir(temp_dir.path))
    assert empty_dir_content_count == 0


def test_is_file(temp_dir):
    assert is_file(temp_dir.file1) == True
    assert is_file(temp_dir.path) == False
