"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from typing import Optional

import typer

from bbcli import __app_name__, __version__, endpoints


app = typer.Typer()
app.add_typer(endpoints.app, name='endpoints', help='Call the endpoints')

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
    return
