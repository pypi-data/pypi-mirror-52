from subprocess import Popen, PIPE
from os import path
import click
from .settings import FILE_NOT_FOUND_TEMPLATE


def do_algomax(filename: str, config: str, params: str, mode: str):
    process = Popen('python {0} {1} {2}'.format(filename, config, params), stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    process.wait()

    if stdout:
        click.echo(' Output '.center(50, '-'))
        click.echo(stdout)
        click.echo('-'.center(50, '-'))

    if stderr:
        click.echo(' Error '.center(50, '-'))
        click.echo(stderr)
        click.echo('-'.center(50, '-'))


@click.command()
@click.argument('filename')
@click.argument('config')
@click.option('-p', help='your algorithm config filename')
@click.option('-m', help='schedule filename')
def algomax(filename: str, config: str, p: str, m: str):
    if not path.exists(filename):
        click.echo(FILE_NOT_FOUND_TEMPLATE.format(filename))
    elif not path.exists(config):
        click.echo(FILE_NOT_FOUND_TEMPLATE.format(config))
    elif p is not None and not path.exists(p):
        click.echo(FILE_NOT_FOUND_TEMPLATE.format(p))
    elif m is not None and not path.exists(m):
        click.echo(FILE_NOT_FOUND_TEMPLATE.format(m))
    else:
        do_algomax(filename, config, p, m)


if __name__ == '__main__':
    algomax()
