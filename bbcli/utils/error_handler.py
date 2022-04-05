import requests
import click

# ERROR HANDLER SHOULD BE USED IN VIEW??


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            click.echo(err.response.text)
            raise click.Abort()
        except KeyError as err:
            click.echo(f'KeyError: key {err} does not exist.')
            raise click.Abort()
    return inner_function
