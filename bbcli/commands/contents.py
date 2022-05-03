import json
from bbcli.utils.URL_builder import URL_builder
from bbcli.utils.utils import format_date
from bbcli.utils.error_handler import create_exception_handler, delete_exception_handler, list_exception_handler, update_exception_handler
import click
from bbcli.entities.content_builder_entitites import FileOptions, GradingOptions, StandardOptions, WeblinkOptions
from bbcli.services import contents_services
import concurrent.futures

from bbcli.entities.Node import Node
from bbcli.utils import content_utils
from bbcli.utils.content_handler import content_handler
from bbcli.views import contents_views

url_builder = URL_builder()

"""
GROUPS OF REUSEABLE OPTIONS
"""

def standard_options(function):
    function = click.option('-h', '--hide-content', is_flag=True,
                            help='Hide content for students')(function)
    function = click.option(
        '-r', '--reviewable', is_flag=True, help='Make content reviewable')(function)
    function = click.option('--start-date', type=str,
                            help='When to make content available. Format: DD/MM/YY HH:MM:SS')(function)
    function = click.option(
        '--end-date', type=str, help='When to make content unavailable. Format: DD/MM/YY HH:MM:SS')(function)
    return function

def grading_options(function):
    function = click.option('-d', '--due-date', type=str,
                            help='Set a sumbission deadline for assignment. Format: DD/MM/YY HH:MM:SS')(function)
    function = click.option('-a', '--max-attempts', type=int,
                            help='Set maximum amount of attempts')(function)
    function = click.option('-u', '--unlimited-attempts',
                            is_flag=True, help='Enable unlimited attempts')(function)
    function = click.option('-s', '--score', required=True,
                            type=int, help='Set assignment score reward')(function)
    return function

def file_options(function):
    function = click.option('-n', '--new-window',
                            'launch_in_new_window', is_flag=True)(function)
    return function

def web_link_options(function):
    function = click.option('-n', '--new-window',
                            'launch_in_new_window', is_flag=True)(function)
    return function

@click.command(name='list', help='List contents\n\nFolders are blue and files are white')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'folder_id', required=False, type=str, help='FOLDER ID')
@click.option('-fo', '--folders-only', required=False, is_flag=True, help='List only folders')
@click.option('-ct', '--content-type', required=False, type=click.Choice(content_handler.keys(), case_sensitive=False))
@click.pass_context
@list_exception_handler
def list_contents(ctx: click.core.Context, course_id: str, folder_id: str, content_type: str, folders_only: bool) -> None:
    if folder_id:
        content_utils.check_content_handler(ctx, course_id, folder_id)
    else:
        ct = 'content' if content_type is None else content_type
        click.echo(f'Listing the {ct}s...')

        response = contents_services.list_contents(
            ctx.obj['SESSION'], course_id)
        data = response.json()['results']
        folder_ids = []
        node_ids = []

        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for node in data:
                root = Node(node)
                worklist = [root]
                folder_ids.append(node['id'])
                args = [ctx, course_id, worklist, folder_ids,
                        node_ids, root, folders_only, content_type]
                t = executor.submit(content_utils.list_contents_thread, *args)
                threads.append(t)

        for t in threads:
            root_node = t.result()
            if root_node is not None:
                contents_views.list_tree(root_node, folder_ids, node_ids)
            else:
                click.ClickException(
                    'Cannot list folders only and a specific content type. Try either one.'
                    ).show()
                return

@click.command(name='get', help='Get content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-co', '--content', 'node_id', required=True, type=str, help='CONTENT ID')
@click.option('-p', '--path', required=False, type=click.Path(exists=True), help='Path to be downloaded to')
@click.pass_context
@list_exception_handler
def get_content(ctx: click.core.Context, course_id: str, node_id: str, path: str) -> None:
    content_utils.check_content_handler(ctx, course_id, node_id, path)

@click.command(name='attachment', help='Add attachment to content\n\nOnly supports contents of type document and assignment')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID of the course where the content is located')
@click.option('-co', '--content', 'content_id', required=True, type=str, help='CONTENT ID of content to attach a file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@create_exception_handler
def upload_attachment(ctx: click.core.Context, course_id: str, content_id: str, file_path: str, print_json: bool) -> None:
    response = contents_services.upload_attachment(
        ctx.obj['SESSION'], course_id, content_id, file_path)
    contents_views.print_created_attachment_response(response, print_json)

@click.command(name='document', help='Create document content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID')
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@standard_options
@click.pass_context
@create_exception_handler
def create_document(ctx: click.core.Context, course_id: str, parent_id: str, title: str, 
                    hide_content: bool, reviewable: bool, start_date: str, end_date: str, 
                    attachments: tuple, print_json: bool, markdown: bool) -> None:
    standard_options = StandardOptions(
        hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)

    response = contents_services.create_document(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, attachments, markdown)
    contents_views.print_created_content_response(response, print_json)

@click.command(name='file', help='Create file content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID')
@click.argument('title', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@file_options
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@standard_options
@click.pass_context
@create_exception_handler
def create_file(ctx: click.core.Context, course_id: str, parent_id: str, title: str, file_path: str,
                launch_in_new_window: bool, hide_content: bool, reviewable: bool,
                start_date: str, end_date: str, print_json: bool) -> None:
    file_options = FileOptions(launch_in_new_window)
    standard_options = StandardOptions(
        hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_services.create_file(
        ctx.obj['SESSION'], course_id, parent_id, title, file_path, file_options, standard_options)
    contents_views.print_created_content_response(response, print_json)


@click.command(name='web-link', help='Create web link content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID')
@click.argument('title', required=True, type=str)
@click.argument('url', required=True, type=str)
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@standard_options
@web_link_options
@click.pass_context
@create_exception_handler
def create_web_link(ctx: click.core.Context, course_id: str, parent_id: str, title: str, url: str,
                    launch_in_new_window: bool, hide_content: bool, reviewable: bool,
                    start_date: str, end_date: str, print_json: bool) -> None:
    web_link_options = WeblinkOptions(launch_in_new_window)
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_services.create_externallink(
        ctx.obj['SESSION'], course_id, parent_id, title, url, web_link_options, standard_options)
    contents_views.print_created_content_response(response, print_json)


@click.command(name='folder', help='Create folder')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=False, type=str, help='FOLDER ID of the parent folder')
@click.argument('title', required=True, type=str)
@click.option('--is-bb-page', is_flag=True, help='Make folder a blackboard page')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@standard_options
@click.pass_context
@create_exception_handler
def create_folder(ctx: click.core.Context, course_id: str, parent_id: str, title: str,
                  hide_content: bool, reviewable: bool, is_bb_page: bool,
                  start_date: str, end_date: str, print_json: bool, markdown: bool) -> None:
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_services.create_folder(
        ctx.obj['SESSION'], course_id, parent_id, title, is_bb_page, standard_options, markdown)
    contents_views.print_created_content_response(response, print_json)


@click.command(name='course-link', help='Create course link content\n\nRedirects user to the target content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID')
@click.option('-t', '--target', 'target_id', required=True, type=str, help='TARGET ID')
@click.argument('title', required=True, type=str)
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@standard_options
@click.pass_context
@create_exception_handler
def create_courselink(ctx: click.core.Context, course_id: str, parent_id: str, title: str, target_id: str,
                      hide_content: bool, reviewable: bool,
                      start_date: str, end_date: str, print_json: bool, markdown: bool) -> None:
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_services.create_courselink(
        ctx.obj['SESSION'], course_id, parent_id, title, target_id, standard_options, markdown)
    contents_views.print_created_content_response(response, print_json)


@click.command(name='assignment', help='Create assignment')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID')
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@standard_options
@grading_options
@click.pass_context
@create_exception_handler
def create_assignment_from_contents(ctx: click.core.Context, course_id: str, parent_id: str, title: str,
                                    hide_content: bool, reviewable: bool,
                                    start_date: str, end_date: str,
                                    due_date: str, max_attempts: int, unlimited_attempts: bool, score: int,
                                    attachments: tuple, print_json: bool, markdown: bool) -> None:
    standard_options = StandardOptions(hide_content, reviewable)
    grading_options = GradingOptions(
        attempts_allowed=max_attempts, is_unlimited_attemps_allowed=unlimited_attempts, score_possible=score)

    set_dates(standard_options, start_date, end_date)
    grading_options.due = format_date(due_date)

    response = contents_services.create_assignment(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, grading_options, attachments, markdown)
    contents_views.print_created_content_response(response, print_json)

@click.command(name='delete', help='Delete content')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID')
@click.option('-co', '--content', 'content_id', required=True, type=str, help='CONTENT ID')
@click.option('--delete-grades', is_flag=True, help='Delete grades if a grade column is associated with the content')
@click.pass_context
@delete_exception_handler
def delete_content(ctx: click.core.Context, course_id: str, content_id: str, delete_grades: bool) -> None:
    contents_services.delete_content(
        ctx.obj['SESSION'], course_id, content_id, delete_grades)
    contents_views.print_deleted_content_response()

@click.command(name='update', help='Update content\n\nEditable content types: document, files, assignments, externallinks, courselinks')
@click.option('-c', '--course', 'course_id', required=True, type=str, help='COURSE ID.')
@click.option('-co', '--content', 'content_id', required=True, type=str, help='CONTENT ID')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@click.option('--advanced', required=False, is_flag=True, help='Use this flag if you also want to update the advanced settings of the content')
@click.pass_context
@update_exception_handler
def update_content(ctx: click.core.Context, course_id: str, content_id: str, print_json: bool, markdown: bool, advanced: bool) -> None:
    if advanced:
        response = contents_services.update_content_advanced(ctx.obj['SESSION'], course_id, content_id, markdown)
    else:
        response = contents_services.update_content(
            ctx.obj['SESSION'], course_id, content_id, markdown)
    contents_views.print_updated_content_response(response, print_json)


"""
HELPER FUNCTIONS
"""

def set_dates(standard_options: StandardOptions, start_date: str, end_date: str) -> None:
    if start_date:
        standard_options.date_interval.start_date = format_date(start_date)
    if end_date:
        standard_options.date_interval.end_date = format_date(end_date)
