from datetime import datetime
import click
from bbcli.entities.content_builder_entitites import FileOptions, StandardOptions, WeblinkOptions
from bbcli.services import contents_service
from bbcli.views import content_view
import os

def standard_options(function):
    function = click.option('-h', '--hide-content', is_flag=True, help='Hide contents for students')(function)
    function = click.option('-r', '--reviewable', is_flag=True, help='Make content reviewable')(function)
    function = click.option('--start-date', type=str, help='When to make content available. Format: DD/MM/YY HH:MM:SS')(function)
    function = click.option('--end-date', type=str, help='When to make content unavailable. Format: DD/MM/YY HH:MM:SS')(function)
    return function

def file_options(function):
    function = click.option('-n', '--new-window', 'launch_in_new_window', is_flag=True)(function)
    return function

def web_link_options(function):
    function = click.option('-n', '--new-window', 'launch_in_new_window', is_flag=True)(function)
    return function


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

@click.command(name='upload')
@click.pass_context
def upload_file(ctx):
    contents_service.test_upload_file(ctx.obj['SESSION'], '/home/magnus/Downloads/3_meeting_notes.pdf')


@click.command(name='document')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@standard_options
@click.pass_context
def create_document(ctx, course_id: str, parent_id: str, title: str, hide_content: bool, reviewable: bool, start_date: str=None, end_date: str=None):
    """
    Creates a document content
    """

    standard_options = StandardOptions(hide_content=hide_content, reviewable=reviewable)
    validate_dates(standard_options, start_date, end_date)

    response = contents_service.create_document(ctx.obj['SESSION'], course_id, parent_id, title, standard_options)
    print(response)


@click.command(name='file')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@file_options
@standard_options
@click.pass_context
def create_file(ctx, course_id: str, parent_id: str, title: str, file_path: str, 
                        launch_in_new_window:bool, hide_content: bool, reviewable: bool,
                        start_date: str=None, end_date: str=None):
    """
    Creates a file content
    """

    file_options = FileOptions(launch_in_new_window)
    standard_options = StandardOptions(hide_content=hide_content, reviewable=reviewable)
    validate_dates(standard_options, start_date, end_date)
    response = contents_service.create_file(ctx.obj['SESSION'], course_id, parent_id, title, file_path, file_options, standard_options)
    print(response)


def validate_dates(standard_options: StandardOptions, start_date: str, end_date: str):
    if start_date:
        try:
            standard_options.date_interval.start_date = datetime.strptime(start_date, '%d/%m/%y %H:%M:%S')
        except ValueError:
            click.echo('Value format is not valid, please see --help for more info')
            raise click.Abort()
            
    if end_date:
        try:
            standard_options.date_interval.end_date = datetime.strptime(end_date, '%d/%m/%y %H:%M:%S')
        except ValueError:
            click.echo('Value format is not valid, please see --help for more info')
            raise click.Abort()



@click.command(name='web-link')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('url', required=True, type=str)
@standard_options
@web_link_options
@click.pass_context
def create_web_link(ctx, course_id: str, parent_id: str, title: str, url: str, 
                        launch_in_new_window:bool, hide_content: bool, reviewable: bool,
                        start_date: str=None, end_date: str=None):
    """
    Create a web link content
    """
    web_link_options = WeblinkOptions(launch_in_new_window)
    standard_options = StandardOptions(hide_content, reviewable)
    validate_dates(standard_options, start_date, end_date)
    response = contents_service.create_externallink(ctx.obj['SESSION'], course_id, parent_id, title, url, web_link_options, standard_options)
    print(response)


@click.command(name='folder')
@click.argument('course_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.option('-p', '--parent_id', required=False, type=str, help='Id of parent folder')
@click.option('--is-bb-page', is_flag=True, help='Make folder a blackboard page')
@standard_options
@click.pass_context
def create_folder(ctx, course_id: str, parent_id: str, title: str,
                        hide_content: bool, reviewable: bool, is_bb_page: bool = False,
                        start_date: str=None, end_date: str=None):
    """
    Create a folder either in top level or inside another content
    """
    standard_options = StandardOptions(hide_content, reviewable)
    validate_dates(standard_options, start_date, end_date)
    response = contents_service.create_folder(ctx.obj['SESSION'], course_id, parent_id, title, is_bb_page, standard_options)
    print(response)

@click.command(name='course-link')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('target_id', required=True, type=str)
@standard_options
@click.pass_context
def create_courselink(ctx, course_id: str, parent_id: str, title: str, target_id: str,
                        hide_content: bool, reviewable: bool, 
                        start_date: str=None, end_date: str=None):
    """
    Create a course link content which redirects user to the target content
    """
    standard_options = StandardOptions(hide_content, reviewable)
    validate_dates(standard_options, start_date, end_date)
    response = contents_service.create_courselink(ctx.obj['SESSION'], course_id, parent_id, title, target_id, standard_options)
    print(response)


