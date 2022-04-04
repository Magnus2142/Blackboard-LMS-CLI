import requests
import click

# ERROR HANDLER SHOULD BE USED IN VIEW??


def HTTP_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            click.echo(err)
            click.Abort()
    return inner_function
