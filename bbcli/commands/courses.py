import click
from bbcli.services import courses_services
from bbcli.utils.error_handler import list_exception_handler
from bbcli.views import courses_views
import os
import requests



# TODO: Hear with Donn whether it is okay to always list all courses?
@click.command(name='list', help='List courses')
@click.option('-c', '--course', 'course_id', required=False, type=str, help='[COURSE ID] Get information about a specific course')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@list_exception_handler
def list_courses(ctx: click.core.Context, course_id: str, print_json: bool) -> None:
    if course_id:
        response = courses_services.list_course(ctx.obj['SESSION'], course_id)
        courses_views.print_course(response, print_json)
    else:
        user_name = os.getenv('BB_USERNAME')
        response = courses_services.list_all_courses(ctx.obj['SESSION'], user_name)
        courses_views.print_courses(response, print_json)
