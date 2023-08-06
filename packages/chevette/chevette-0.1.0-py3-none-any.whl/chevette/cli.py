import click
from chevette.chevette import Chevette


@click.group()
def chevette():
    """
    Chevette is a static blog platform written in Python.
    """
    pass


@click.command()
@click.option('-f', '--force', is_flag=True, help='Force creation even if PATH already exists.') # noqa E501
@click.argument('path', type=str)
def new(path, force):
    """
    Generates a new chevette boilerplate at the specified PATH
    """
    Chevette.new(path, force)


@click.command()
def build():
    """
    Build your blog.
    """
    Chevette.build()


@click.command()
def serve():
    """
    Start a server with your generated site
    """
    Chevette.serve()


chevette.add_command(new)
chevette.add_command(build)
chevette.add_command(serve)

if __name__ == "__main__":
    chevette()
