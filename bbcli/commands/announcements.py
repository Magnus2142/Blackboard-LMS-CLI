from datetime import datetime
import json
import click
from bbcli.entities.content_builder_entitites import DateInterval
from bbcli.services import announcements_service
from bbcli.utils.error_handler import create_exception_handler, delete_exception_handler, list_exception_handler, update_exception_handler
from bbcli.utils.utils import format_date
from bbcli.views import announcements_view
import os


@click.command(name='list', help='This command lists your announcements.\nEither all announcements, all announcements from a spesific course, or one announcement.')
@click.option('-c', '--course', 'course_id', required=False, type=str, help='COURSE ID, list announcements from a spesific course')
@click.option('-a', '--announcement', 'announcement_id', required=False, type=str, help='ANNONUCEMENT ID, list a spesific announcement from a course.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print data in json format')
@click.pass_context
@list_exception_handler
def list_announcements(ctx, course_id=None, announcement_id=None, print_json=False):
    response = None

    if announcement_id:
        response = announcements_service.list_announcement(
            ctx.obj['SESSION'], course_id, announcement_id)
        if not print_json:
            announcements_view.print_announcement(response)
    elif course_id:
        response = announcements_service.list_course_announcements(
            ctx.obj['SESSION'], course_id)
        if not print_json:
            announcements_view.print_course_announcements(response)
    else:
        user_name = os.getenv('BB_USERNAME')
        response = announcements_service.list_announcements(
            ctx.obj['SESSION'], user_name)
        if not print_json:
            announcements_view.print_announcements(response)
    
    if print_json:
        click.echo(json.dumps(response, indent=2))


@click.command(name='create', help='Creates an announcement. Add --help for all options available.')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID of the course you want to create an announcement in.')
@click.argument('title', required=True, type=str)
@click.option('--start-date', type=str, help='When to make announcement available. Format: DD/MM/YY HH:MM:SS')
@click.option('--end-date', type=str, help='When to make announcement unavailable. Format: DD/MM/YY HH:MM:SS')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print response data in json format')
@click.pass_context
@create_exception_handler
def create_announcement(ctx, course_id: str, title: str, start_date: str, end_date: str, print_json: bool):
    date_interval = DateInterval()
    if start_date or end_date:
        if start_date:
            date_interval.start_date = format_date(start_date)
        if end_date:
            date_interval.end_date = format_date(end_date)

    response = announcements_service.create_announcement(
        ctx.obj['SESSION'], course_id, title, date_interval)
    if print_json:
        data = json.loads(response)
        click.echo(json.dumps(data, indent=2))
    else:
        announcements_view.print_announcement_created(response)


@click.command(name='delete', help='Deletes an announcement. Add --help for all options available')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID of the course you want to create an announcement in.')
@click.option('-a', '--announcement', 'announcement_id', required=True, type=str, help='ANNOUNCEMENT ID, of the announcement you want to delete.')
@click.pass_context
@delete_exception_handler
def delete_announcement(ctx, course_id: str, announcement_id: str):
    announcements_service.delete_announcement(
        ctx.obj['SESSION'], course_id, announcement_id)
    announcements_view.print_announcement_deleted()


@click.command(name='update', help='Updates an announcement. Add --help for all options available.')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID of the course you want to create an announcement in.')
@click.option('-a', '--announcement', 'announcement_id', required=True, type=str, help='ANNOUNCEMENT ID, of the annonucement you want to update.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print response data in json format')
@click.pass_context
@update_exception_handler
def update_announcement(ctx, course_id: str, announcement_id: str, print_json: bool):
    response = announcements_service.update_announcement(
        ctx.obj['SESSION'], course_id, announcement_id)
    if print_json:
        data = json.loads(response)
        click.echo(json.dumps(data, indent=2))
    else:
        announcements_view.print_announcement_updated(response)
