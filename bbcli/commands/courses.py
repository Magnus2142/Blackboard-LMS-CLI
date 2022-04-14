import click
from bbcli.services import courses_service
from bbcli.utils.error_handler import list_exception_handler
from bbcli.views import course_view
import os
import requests


# , help='List a spesific course with the corresponding id'
@click.command(name='list', help='List courses')
@click.option('-c', '--course', 'course_id', required=False, type=str, help='[COURSE ID] Get information about a specific course')
@click.option('-a', '--all/--no-all', 'show_all', default=False, help='List all registered courses on the current user')
@click.pass_context
@list_exception_handler
def list_courses(ctx, course_id=None, show_all=False):
    response = None

    if course_id:
        response = courses_service.list_course(
            session=ctx.obj['SESSION'], course_id=course_id)
        course_view.print_course(response)
    else:
        user_name = os.getenv('BB_USERNAME')
        if show_all:
            response = courses_service.list_all_courses(
                session=ctx.obj['SESSION'], user_name=user_name)
        else:
            response = courses_service.list_courses(
                session=ctx.obj['SESSION'], user_name=user_name)
        course_view.print_courses(response)
