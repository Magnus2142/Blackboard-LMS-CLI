import requests
import click
from http import HTTPStatus



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


def list_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            status_code = err.response.json()['status']
            if status_code == HTTPStatus.FORBIDDEN:
                click.echo('Current user do not have the right permissions to use this resource/resources.')
                raise click.Abort()
            if status_code == HTTPStatus.BAD_REQUEST or status_code == HTTPStatus.NOT_FOUND:
                params = kwargs.keys()
                key_list = []
                for param in params:
                    if kwargs[param] != None:
                        key_list.append(param)
                click.echo(f'Could not find resource/-s with the id/-s of type: {key_list}.')
                click.echo('HINT: Double-check if id/-s are correct and in the correct order.')
                raise click.Abort()
    return inner_function