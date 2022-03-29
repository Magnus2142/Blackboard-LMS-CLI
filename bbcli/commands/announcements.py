import click
from bbcli.services import announcements_service
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
@click.pass_context
def create_announcement(ctx, course_id: str, title: str):
    """
    This command creates an announcement. Add --help
    for all options available
    """
    response = announcements_service.create_announcement(ctx.obj['SESSION'], course_id, title)
    click.echo(response)


@click.command(name='delete')
@click.argument('course_id', required=True, type=str)
@click.argument('announcement_id', required=True, type=str)
@click.pass_context
def delete_announcement(ctx, course_id: str, announcement_id: str):
    """
    This command deletes an announcement. Add --help
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
    This command updates an announcement. Add --help
    for all options available
    """
    response = announcements_service.update_announcement(ctx.obj['SESSION'], course_id, announcement_id)
    click.echo(response)
