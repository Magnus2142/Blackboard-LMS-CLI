import os
from datetime import datetime
import mmap
from typing import Dict, List
from requests import Session
import html2text
import click

from bbcli.services.authorization_service import login

def check_valid_key(obj, key) -> bool:
    # print("the keys are", obj.keys())
    if key not in obj.keys():
        click.echo(f'The key: \"{key}\" is not in the object')
        return False
    else:
        return True


def check_response(response) -> bool:
    invalid_statuscodes = [401, 403, 404]
    if response.status_code in invalid_statuscodes:
        click.echo('Status: ' + str(response.json()['status']))
        click.echo('Message: ' + response.json()['message'])
        return False
    else:
        return True


def check_valid_date(cookie) -> bool:
    tmp = cookie
    start = int(tmp.find('expires')) + len('expires') + 1
    end = int(tmp.find(','))
    timestmp = int(tmp[start: end])
    expires = datetime.fromtimestamp(timestmp)
    now = datetime.now()
    if expires >= now:
        return True
    else:
        return False


def set_cookies(session: Session, cookies: List):
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])


def set_headers(session: Session, headers: List):
    for header in headers:
        session.headers.update(header)


def html_to_text(html_data: str):
    to_text = html2text.HTML2Text()
    return to_text.handle(html_data)


def input_body():
    MARKER = '# Everything below is ignored. Leave blank if you want empty body.\n'
    body = click.edit('\n\n' + MARKER)
    if body is not None:
        body = body.split(MARKER, 1)[0].rstrip('\n')
    return body


def format_date(date: str):
    if date:
        try:
            return datetime.strptime(date, '%d/%m/%y %H:%M:%S')
        except ValueError:
            click.echo('Value format is not valid, please see --help for more info.')
            raise click.Abort()

def get_download_path(file_name, path: str):
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        downloads_path = f'{location}\{file_name}'
        if path == None:
            return donwloads_path
        else:
            return downloads_path.replace('Downloads', path)
    else:
        if path == None:
            return os.path.join(os.path.expanduser('~'), f'Downloads/{file_name}')
        else:
            return os.path.join(os.path.expanduser('~'), f'{path}/{file_name}')


def authorization_handler(func):
	def inner_function(*args, **kwargs):
		is_authorized = True if os.getenv("BB_ROUTER") != None else False
		if is_authorized:
			func(*args, **kwargs)
		else:
			click.echo('You are not logged in, running login script:')
			login()
			click.echo('You can now communicate with Blackboard LMS')
	return inner_function

def handle_fish_shell_completion():
    append_text = '_BB_COMPLETE=fish_source bb > ~/.config/fish/completions/bb.fish'
    path = os.path.join(os.path.expanduser('~'), f'/.config/fish/completions/bb.fish')
    if os.path.exists(path):
        with open(path, 'rb') as f, \
            mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(bytearray(append_text)) != -1:
                is_activated = True
                click.echo('Shell completion already activated!')
    
    if is_activated == False:
        with open(path, 'a') as f:
            f.write(f'\n{append_text}\n')
            click.echo('Shell completion activated! Restart shell to load the changes.')

def print_keys_in_dict(dictionary: Dict):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            print_keys_in_dict(dictionary[key])
        elif dictionary[key] != None:
            click.echo('{:<20} {:20}'.format(f'{key}:', str(dictionary[key])))

