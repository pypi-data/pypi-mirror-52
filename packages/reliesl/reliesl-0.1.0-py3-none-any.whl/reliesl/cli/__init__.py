import click

from reliesl.cli.bump import bump
from reliesl.cli.release import release


@click.group()
def reliesl():
    pass


reliesl.add_command(bump)
reliesl.add_command(release)


def main():
    """Entry point to be used when building reliesl as a library."""
    reliesl()
