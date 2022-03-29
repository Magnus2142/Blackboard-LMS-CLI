import click
from bbcli.services import contents_service
from bbcli.views import content_view
import os


#, help='List a spesific course with the corresponding id'
@click.command(name='list')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=False, type=str)
# @click.option('-a', '--all/--no-all', 'show_all', default=False, help='Lists all courses you have ever been signed up for')
@click.pass_context
def list_contents(ctx, course_id: str=None, content_id: str=None):

    """
    This command lists contents of a course.
    """
    response = None

    if content_id:
        print('GEtting spesific content from a course')
    else:
        print('Printing content tree from a course, course', course_id)


@click.command(name='create')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.pass_context
def create_content(ctx, course_id: str, content_id: str):
    contents_service.test_create_assignment(ctx.obj['SESSION'], course_id, content_id)
