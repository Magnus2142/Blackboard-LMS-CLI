"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from typing import Optional

import typer

from bbcli import __app_name__, __version__, endpoints
import os
from dotenv import load_dotenv
from datetime import datetime
from bbcli import login


app = typer.Typer()
app.add_typer(endpoints.app, name='endpoints', help='Call the endpoints')

load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}

def check_valid_date() -> bool:
    tmp = cookies['BbRouter']
    start = int(tmp.find('expires')) + len('expires') + 1
    end = int(tmp.find(','))
    timestmp = int(tmp[start : end])
    print(timestmp)
    expires = datetime.fromtimestamp(timestmp)
    now = datetime.now()
    if expires >= now:
        return True
    else: 
        return False

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    if check_valid_date() == False:
        login()
        # load_dotenv()
        # cookies['BbRouter'] = os.getenv("BB_ROUTER")
        # headers['X-Blackboard-XSRF'] = os.getenv("XSRF")
    return
