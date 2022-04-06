
import requests
from bbcli.utils.utils import set_cookies, set_headers
from bbcli import __app_name__, __version__
import os
from dotenv import load_dotenv
from bbcli import check_valid_date
import click

from bbcli.commands.courses import list_courses
from bbcli.commands.announcements import list_announcements, create_announcement, delete_announcement, update_announcement
from bbcli.commands.contents import create_assignment, create_courselink, create_folder, delete_content, list_contents, create_document, create_file, create_web_link, update_content, upload_attachment, get_content
from bbcli.commands.assignments import get_assignments
from bbcli.services.authorization_service import login
import mmap

load_dotenv()
cookies = {'BbRouter': os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}

#----- AUTHORIZATION MODULE -----#
# @app.command(name='login', help='Authorize the user.')


def authorize_user():
    if cookies['BbRouter'] == None or check_valid_date(cookies) == False:
        login()


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


@click.group()
@click.pass_context
def entry_point(ctx):
    ctx.ensure_object(dict)
    authorize_user()

    session = initiate_session()
    ctx.obj['SESSION'] = session



"""
ACTIVATE SHELL COMPLETION
"""
@click.command(name='activate-shell-completion')
def activate_shell_completion():
    is_activated = False
    shell = os.environ['SHELL']
    if shell == '/bin/bash':
        shell = 'bash'
    elif shell == '/bin/zsh':
        shell = 'zsh'
    elif shell == '/bin/fish':
        shell = 'fish'
    
    path = os.path.join(os.path.expanduser('~'), f'.config/fish/completions/bb.{shell}')\
        if shell == 'fish' else os.path.join(os.path.expanduser('~'), f'.{shell}rc')

    append_text = f'eval (env _BB_COMPLETE=source_fish bb)' if shell == 'fish' else f'eval "$(_BB_COMPLETE=source_{shell} bb)"'

    with open(path, 'rb') as f, \
        mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
    
        if s.find(bytearray(append_text.encode())) != -1:
            is_activated = True

    if not is_activated:
        with open(path, 'a') as f:
            f.write(f'\n{append_text}')
            click.echo('Shell completion activated!')
    else:    
        click.echo('Shell completion already activated.')


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


@entry_point.group()
@click.pass_context
def assignments(ctx):
    """
    Commands for creating, listing and submitting assignments.
    """
    pass


assignments.add_command(get_assignments)
assignments.add_command(create_assignment)

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
    pass


create.add_command(create_document)
create.add_command(create_file)
# create.add_command(create_web_link)
create.add_command(create_folder)
create.add_command(create_courselink)
create.add_command(upload_attachment)
create.add_command(create_assignment)
