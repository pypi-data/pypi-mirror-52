import setuptools
from chevette.utils.constants import VERSION

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='chevette',
    version=VERSION,
    description='Chevette is a MarkDown powered static blog engine.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(
        exclude=['docs', 'tests']
    ),
    url="https://github.com/Zabanaa/chevette",
    author="Karim C",
    author_email="karim.cheurfi@gmail.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary'
    ],
    keywords="static site generator",
    python_requires='>=3.7',
    install_requires=[
        'jinja2',
        'misaka',
        'python-frontmatter',
        'click',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'chevette=chevette.cli:chevette'
        ]
    }
)
