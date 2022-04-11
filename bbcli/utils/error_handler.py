from http.client import INTERNAL_SERVER_ERROR
from typing import Dict, List
import requests
import click
from http import HTTPStatus

id_parameter_names = ['course_id', 'announcement_id','content_id', 'node_id', 'parent_id', 'target_id', 'column_id']

def get_used_parameters(kwargs: Dict, only_id_parameters: bool=False, no_id_parameters:bool= False):
    params = kwargs.keys()
    key_list = []
    for param in params:
        if only_id_parameters:
            id_used(kwargs, param, key_list)
        elif no_id_parameters:
            param_used(kwargs, param, key_list)
        else:
            param_and_id_used(kwargs, param, key_list)
    return key_list

def id_used(kwargs: Dict, param: str, key_list: List):
    if kwargs[param] != None and param in id_parameter_names:
        key_list.append(param)

def param_used(kwargs: Dict, param: str, key_list: List):
    if kwargs[param] != None and param not in id_parameter_names:
        key_list.append(param)

def param_and_id_used(kwargs: Dict, param: str, key_list: List):
    if kwargs[param] != None:
        key_list.append(param)

# Handles exceptions where a resource is not found or user don't have the right permission
def list_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            click.echo(err.response.text + '\n\n')
            status_code = err.response.json()['status']
            forbidden_handler(status_code)
            not_found_handler(status_code, kwargs)
            bad_request_or_not_found_handler(status_code, kwargs)
            internal_server_error_handler(status_code)
    return inner_function

def create_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            status_code = err.response.json()['status']
            click.echo(err.response.text + '\n\n')
            forbidden_handler(status_code)
            not_found_handler(status_code, kwargs)
            bad_request_or_not_found_handler(status_code, kwargs)
            insufficient_storage_handler(status_code)
            conflict_handler(status_code)
            internal_server_error_handler(status_code)
            unprocessable_entity(status_code)
    return inner_function

def delete_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            status_code = err.response.json()['status']
            click.echo(err.response.text + '\n\n')
            forbidden_handler(status_code)
            bad_request_or_not_found_handler(status_code, kwargs)
            internal_server_error_handler(status_code)
    return inner_function

def update_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            status_code = err.response.json()['status']
            click.echo(err.response.text + '\n\n')
            forbidden_handler(status_code)
            not_found_handler(status_code, kwargs)
            bad_request_or_not_found_handler(status_code, kwargs)
            internal_server_error_handler(status_code)
            insufficient_storage_handler(status_code)
    return inner_function


def forbidden_handler(status_code):
    if status_code == HTTPStatus.FORBIDDEN:
        click.echo('Current user do not have the right permissions to use/edit this resource/resources.')
        raise click.Abort()

def bad_request_or_not_found_handler(status_code, kwargs):
    if status_code == HTTPStatus.BAD_REQUEST or status_code == HTTPStatus.NOT_FOUND:
        click.echo(f'Bad parameters! Please check if the id/-s of type: {get_used_parameters(kwargs, only_id_parameters=True)} is correct')
        params_only_list = get_used_parameters(kwargs, no_id_parameters=True)
        if len(params_only_list) != 0:
            click.echo(f'and if all all of the parameters of type: {get_used_parameters(kwargs, no_id_parameters=True)} have correct format.')
        click.echo('HINT: use --help for more info')
        raise click.Abort()

def not_found_handler(status_code, kwargs):
    if status_code == HTTPStatus.NOT_FOUND:
        click.echo(f'Could not find resource/-s with the id/-s of type: {get_used_parameters(kwargs, only_id_parameters=True)}.')
        raise click.Abort()
    
def insufficient_storage_handler(status_code):
    if status_code == HTTPStatus.INSUFFICIENT_STORAGE:
        click.echo(f'This folder cannot hold any more children. Folder quota exceeded.')
        raise click.Abort()

def conflict_handler(status_code):
    if status_code == HTTPStatus.CONFLICT:
        click.echo('A conflict have appeared!')
        raise click.Abort()

def internal_server_error_handler(status_code):
    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        click.echo('An internal server error has appered! HINT: Check --help for correct formatting of parameters.')
        click.echo('Remember id have the format _x_1, where you replace the x with a number.')
        raise click.Abort()

def unprocessable_entity(status_code):
    if status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        click.echo('This file is potentially unsafe as determined from an XSS scan.')
        raise click.Abort()