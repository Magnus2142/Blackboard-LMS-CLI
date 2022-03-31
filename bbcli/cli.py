
from typing import Optional
from pkg_resources import EntryPoint
import requests
from bbcli.utils.utils import set_cookies, set_headers
# import typer
from bbcli import __app_name__, __version__ 
# from bbcli.endpoints import get_user, get_course_contents, get_assignments
import os
from dotenv import load_dotenv
from bbcli import check_valid_date, check_response
import click

from bbcli.commands.courses import list_courses
from bbcli.commands.announcements import list_announcements, create_announcement, delete_announcement, update_announcement
from bbcli.commands.contents import list_contents, create_content, create_document, create_file
from bbcli.services.authorization_service import login

load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}

#----- AUTHORIZATION MODULE -----#
# @app.command(name='login', help='Authorize the user.')
def authorize_user():
    if cookies['BbRouter'] == None or check_valid_date(cookies) == False:
        login()

def initiate_session():
    bb_cookie = {
            'name':'BbRouter',
            'value': os.getenv("BB_ROUTER")
        }
    xsrf = {'X-Blackboard-XSRF': os.getenv('XSRF')}

    session = requests.Session()
    set_cookies(session, [bb_cookie])
    set_headers(session, [xsrf])
    session.headers.update({'Content-Type': 'application/json'})
    return session
    

@click.group()
@click.pass_context
def entry_point(ctx):
    ctx.ensure_object(dict)
    authorize_user()

    session = initiate_session()
    ctx.obj['SESSION'] = session

    pass

"""
COURSE COMMANDS ENTRY POINT
"""
@entry_point.group()
@click.pass_context
def courses(ctx):
    """
    Commands for listing courses
    """
    pass

courses.add_command(list_courses)


"""
ANNOUNCEMENT COMMANDS ENTRY POINT
"""
@entry_point.group()
@click.pass_context
def announcements(ctx):
    """
    Commands for listing, creating, deleting and updating announcements
    """
    pass

announcements.add_command(list_announcements)
announcements.add_command(create_announcement)
announcements.add_command(delete_announcement)
announcements.add_command(update_announcement)

"""
CONTENT COMMANDS ENTRY POINT
"""

@entry_point.group()
@click.pass_context
def contents(ctx):
    """
    Commands for listing, creating, deleting, updating and downloading content
    """
    pass

contents.add_command(list_contents)
# contents.add_command(upload_file)

"""
CONTENTS CREATE COMMANDS ENTRY POINT
"""

@contents.group()
@click.pass_context
def create(ctx):
    """
    Commands for creating different types of content types in blackboard
    """
    pass

# create.add_command(create_content)
create.add_command(create_document)
create.add_command(create_file)