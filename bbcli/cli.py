
from typing import Optional
import typer
from bbcli import __app_name__, __version__, endpoints
import os
from dotenv import load_dotenv
from bbcli import login, check_valid_date

from bbcli.Services import AuthorizationService

app = typer.Typer()
app.add_typer(endpoints.app, name='endpoints', help='Call the endpoints')

load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-v',
        help='Show the applications version and exit.',
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    if check_valid_date(cookies) == False:
        AuthorizationService.login()
        # load_dotenv()
        # cookies['BbRouter'] = os.getenv("BB_ROUTER")
        # headers['X-Blackboard-XSRF'] = os.getenv("XSRF")
    return

#----- AUTHORIZATION MODULE -----#
@app.command(name='login', help='Authorize the user.')
def authorize_user():
    AuthorizationService.login()


#----- COURSE MODULE -----#

@app.command(name='course')
def course(
    course_id: Optional[str] = typer.Argument(None, help='The id of the course you want.'),
    favorites: bool = typer.Option(False, help='List only your favorite courses.')):
    if course_id != None and favorites == False:
        # CODE FOR GETTING SPESIFIC COURSE


        print('getting spesific course...')
    elif course_id != None and favorites == True:
        # CODE FOR GETTING SPESIFIC FAVORITE COURSE

        print('getting spesific favorite course...')
    else:
        # CODE FOR GETTING ALL COURSES


        print('getting all courses...')