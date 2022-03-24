
from typing import Optional
from pkg_resources import EntryPoint
# import typer
from bbcli import __app_name__, __version__ 
from bbcli.endpoints import get_user, get_course_contents, get_assignments
import os
from dotenv import load_dotenv
from bbcli import check_valid_date, check_response
import click

from bbcli.services import authorization_service
from bbcli.services import announcement_service

@click.group()
def entry_point():
    authorize_user()
    pass

@click.command(name='announcements')
def get_announcements():
    response = announcement_service.update_announcement(cookies, headers, '_33050_1', '_385022_1')
    click.echo(response)


entry_point.add_command(get_announcements)
entry_point.add_command(get_user)
entry_point.add_command(get_course_contents)
entry_point.add_command(get_assignments)

load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}

#----- AUTHORIZATION MODULE -----#
# @app.command(name='login', help='Authorize the user.')
def authorize_user():
    if check_valid_date(cookies) == False:
        authorization_service.login()
