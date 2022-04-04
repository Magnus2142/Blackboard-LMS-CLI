from datetime import datetime
import click
from bbcli.entities.content_builder_entitites import DateInterval
from bbcli.services import announcements_service
from bbcli.utils.utils import format_date
from bbcli.views import announcement_view
import os

@click.command(name='list')
@click.argument('course_id', required=False)
@click.argument('announcement_id', required=False)
@click.pass_context
def list_announcements(ctx,course_id=None, announcement_id=None):

    """
    This command lists your announcements.
    Either all announcements, all announcements from a spesific course, or one announcement.
    """
    response = None
    
    if announcement_id:
        response = announcements_service.list_announcement(ctx.obj['SESSION'], course_id, announcement_id)
        announcement_view.print_course_announcements([response])
    elif course_id:
        response = announcements_service.list_course_announcements(ctx.obj['SESSION'], course_id)
        announcement_view.print_course_announcements(response)
    else:
        user_name = os.getenv('BB_USERNAME')
        response = announcements_service.list_announcements(ctx.obj['SESSION'], user_name)
        announcement_view.print_announcements(response)


@click.command(name='create')
@click.argument('course_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.option('--start-date', type=str, help='When to make announcement available. Format: DD/MM/YY HH:MM:SS')
@click.option('--end-date', type=str, help='When to make announcement unavailable. Format: DD/MM/YY HH:MM:SS')
@click.pass_context
def create_announcement(ctx, course_id: str, title: str, start_date: str, end_date: str):
    """
    Creates an announcement. Add --help
    for all options available
    """
    if start_date or end_date:
        date_interval = DateInterval()
        if start_date:
            date_interval.start_date = format_date(start_date)
        if end_date:
            date_interval.end_date = format_date(end_date)

    response = announcements_service.create_announcement(ctx.obj['SESSION'], course_id, title, date_interval)
    click.echo(response)


@click.command(name='delete')
@click.argument('course_id', required=True, type=str)
@click.argument('announcement_id', required=True, type=str)
@click.pass_context
def delete_announcement(ctx, course_id: str, announcement_id: str):
    """
    Deletes an announcement. Add --help
    for all options available
    """
    response = announcements_service.delete_announcement(ctx.obj['SESSION'], course_id, announcement_id)
    click.echo(response)


@click.command(name='update')
@click.argument('course_id', required=True, type=str)
@click.argument('announcement_id', required=True, type=str)
@click.pass_context
def update_announcement(ctx, course_id: str, announcement_id: str):
    """
    Updates an announcement. Add --help
    for all options available
    """
    response = announcements_service.update_announcement(ctx.obj['SESSION'], course_id, announcement_id)
    click.echo(response)
