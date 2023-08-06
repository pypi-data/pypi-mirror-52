import pytest
import tempfile
from shutil import rmtree
from collections import namedtuple

TempDir = namedtuple('TempDir', ['path', 'file1', 'file2'])


@pytest.fixture(scope='function')
def temp_dir():
    _dir = tempfile.mkdtemp()
    f_one = tempfile.mkstemp(dir=_dir, suffix='.md')
    f_two = tempfile.mkstemp(dir=_dir, suffix='.txt')
    yield TempDir(_dir, f_one[1], f_two[1])
    rmtree(_dir)
