
import requests
from bbcli.utils.utils import handle_fish_shell_completion, set_cookies, set_headers
from bbcli import __app_name__, __version__
import os
import shutil
from dotenv import load_dotenv
from bbcli import check_valid_date
import click

from bbcli.commands.courses import list_courses
from bbcli.commands.announcements import list_announcements, create_announcement, delete_announcement, update_announcement
from bbcli.commands.contents import create_assignment_from_contents, create_courselink, create_folder, delete_content, list_contents, create_document, create_file, create_web_link, update_content, upload_attachment, get_content
from bbcli.commands.assignments import get_assignments, submit_attempt, grade_assignment, get_attempts, get_attempt, submit_draft, update_attempt, submit_draft, create_assignment
from bbcli.services.authorization_service import login
import mmap


def initiate_session():
    bb_cookie = {
        'name': 'BbRouter',
        'value': os.getenv("BB_ROUTER")
    }
    xsrf = {'X-Blackboard-XSRF': os.getenv('XSRF')}

    session = requests.Session()
    set_cookies(session, [bb_cookie])
    set_headers(session, [xsrf])
    session.headers.update({'Content-Type': 'application/json'})
    return session

def authenticate_user():
    load_dotenv()
    bb_cookie = os.getenv('BB_ROUTER')
    is_authorized = True if bb_cookie != None and check_valid_date(bb_cookie) else False
    if not is_authorized:
        click.echo('You are not logged in. Executing authorization script...')
        login()
    

@click.group()
@click.pass_context
@click.version_option(__version__)
def entry_point(ctx):
    ctx.ensure_object(dict)

"""
LOGIN AND LOGOUT COMMANDS
"""
@click.command(name='login')
def authorize_user():
    """
    Authorize user with username and password.
    """
    login()

@click.command(name='logout')
def logout():
    """
    Logout user.
    """
    open(f'{os.path.dirname(os.path.abspath(__file__))}/.env', 'w').close()
    click.echo('Sucessfully logged out.')

entry_point.add_command(authorize_user)
entry_point.add_command(logout)

"""
SHELL COMPLETION COMMANDS
"""
@click.command(name='activate-shell-completion', help='Activate shell completion for your shell')
@click.argument('shell', required=True, type=str)
def activate_shell_completion(shell: str):
    if shell == 'fish':
        handle_fish_shell_completion()
    else:
        if shell == 'bash' or shell == 'zsh':
            is_activated = False
            path = os.path.join(os.path.expanduser('~'), f'.{shell}rc')
            append_text = f'. ~/.bb-complete.{shell}'
            with open(path, 'rb') as f, \
                mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(bytearray(append_text.encode())) != -1:
                    is_activated = True

            if not is_activated:
                shutil.copy(f'{os.path.dirname(os.path.abspath(__file__))}/shell-completion/.bb-complete.bash', os.path.expanduser('~'))
                with open(os.path.join(os.path.expanduser('~'), f'.{shell}rc'), 'a') as f:
                    f.write('\n. ~/.bb-complete.bash\n')
                    click.echo('Shell completion activated! Restart shell to load the changes.')
            else:
                click.echo('Shell completion already activated.')
        else: 
            click.echo('Did not recognize the Shell or CLI shell completion is not compatible with your Shell.')


entry_point.add_command(activate_shell_completion)

"""
COURSE COMMANDS ENTRY POINT
"""

@entry_point.group()
@click.pass_context
def courses(ctx):
    """
    Commands for listing courses
    """
    authenticate_user()
    load_dotenv()
    session = initiate_session()
    ctx.obj['SESSION'] = session


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
    authenticate_user()
    load_dotenv()
    session = initiate_session()
    ctx.obj['SESSION'] = session

announcements.add_command(list_announcements)
announcements.add_command(create_announcement)
announcements.add_command(delete_announcement)
announcements.add_command(update_announcement)


@entry_point.group()
@click.pass_context
def assignments(ctx):
    """
    Commands for creating, listing and submitting assignments.
    """
    authenticate_user()
    load_dotenv()
    session = initiate_session()
    ctx.obj['SESSION'] = session

assignments.add_command(get_assignments)
assignments.add_command(create_assignment)
assignments.add_command(grade_assignment)


@assignments.group()
@click.pass_context
def attempts(ctx):
    """
    Commands for creating, submitting and listing attempts for an assignment.
    """
    pass


attempts.add_command(get_attempts)
attempts.add_command(get_attempt)
attempts.add_command(submit_attempt)
attempts.add_command(submit_draft)
attempts.add_command(update_attempt)

"""
CONTENT COMMANDS ENTRY POINT
"""


@entry_point.group()
@click.pass_context
def contents(ctx):
    """
    Commands for listing, creating, deleting, updating and downloading content
    """
    authenticate_user()
    load_dotenv()
    session = initiate_session()
    ctx.obj['SESSION'] = session


contents.add_command(list_contents)
contents.add_command(get_content)
contents.add_command(delete_content)
contents.add_command(update_content)

"""
CONTENTS CREATE COMMANDS ENTRY POINT
"""


@contents.group()
@click.pass_context
def create(ctx):
    """
    Commands for creating different types of content types in blackboard
    """
    authenticate_user()
    load_dotenv()
    session = initiate_session()
    ctx.obj['SESSION'] = session


create.add_command(create_document)
create.add_command(create_file)
create.add_command(create_web_link)
create.add_command(create_folder)
# create.add_command(create_courselink)
create.add_command(upload_attachment)
create.add_command(create_assignment_from_contents)
