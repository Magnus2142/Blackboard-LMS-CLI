from bbcli.utils.utils import format_date
from bbcli.utils.error_handler import exception_handler
from datetime import datetime
import click
from bbcli.entities.content_builder_entitites import FileOptions, GradingOptions, StandardOptions, WeblinkOptions
from bbcli.services import contents_service
from bbcli.views import contents_view
import time
import click

from bbcli import check_response
from bbcli.entities.Node import Node
from bbcli.utils.URL_builder import URL_builder
from bbcli.utils.content_handler import content_handler

url_builder = URL_builder()

base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


def standard_options(function):
    function = click.option('-h', '--hide-content', is_flag=True,
                            help='Hide contents for students')(function)
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
                            help='Set a maximum amount of attempts.')(function)
    function = click.option('-u', '--unlimited-attempts',
                            is_flag=True, help='Enable unlimited attempts.')(function)
    function = click.option('-s', '--score', required=True,
                            type=int, help='Set assignment score reward.')(function)
    return function


def file_options(function):
    function = click.option('-n', '--new-window',
                            'launch_in_new_window', is_flag=True)(function)
    return function


def web_link_options(function):
    function = click.option('-n', '--new-window',
                            'launch_in_new_window', is_flag=True)(function)
    return function


@click.command(name='list')
@click.argument('course_id', default='_27251_1')
# @click.option('--folder-id')
@click.pass_context
@exception_handler
def list_contents(ctx, course_id: str, folder_id=None):
    '''
    Get the contents\n
    Folders are blue and have an id \n
    Files are white
    '''
    start = time.time()

    response = contents_service.list_contents(
        ctx.obj['SESSION'], course_id, folder_id)
    folders = response.json()['results']
    for folder in folders:
        r = Node(folder)
        worklist = [r]
        get_children(ctx, course_id, worklist)
        colors, root = r.preorder(r)
        contents_view.list_tree(colors, root)

    end = time.time()

    print(f'\ndownload time: {end - start} seconds')


@click.command(name='get')
@click.argument('course_id', required=True, type=str)
@click.argument('node_id', required=True, type=str)
@click.pass_context
def get_content(ctx, course_id: str, node_id: str):
    response = contents_service.get_content(
        ctx.obj['SESSION'], course_id, node_id)
    data = response.json()
    if data['contentHandler']['id'] == content_handler['document']:
        contents_view.open_vim()
    elif data['contentHandler']['id'] == content_handler['file'] or data['contentHandler']['id'] == content_handler['document'] or data['contentHandler']['id'] == content_handler['assignment']:
        click.confirm(
            "This is a .docx file, do you want to download it?", abort=True)
        response = contents_service.get_file(
            ctx.obj['SESSION'], course_id, node_id)
    elif data['contentHandler']['id'] == content_handler['folder']:
        root = Node(data, True)
        worklist = [root]
        res = get_children(ctx, course_id, worklist, [])
        contents_view.create_tree(root, res)


@click.command(name='attachment')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@click.pass_context
@exception_handler
def upload_attachment(ctx, course_id: str, content_id: str, file_path: str):
    """
    Adds an attachment to a content. Only supports contents of type document and assignment
    """
    contents_service.upload_attachment(
        ctx.obj['SESSION'], course_id, content_id, file_path)


@click.command(name='document')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@standard_options
@click.pass_context
@exception_handler
def create_document(ctx, course_id: str, parent_id: str, title: str, hide_content: bool, reviewable: bool, start_date: str = None, end_date: str = None, attachments: tuple = None):
    """
    Creates a document content, optionally with file attachments
    """
    standard_options = StandardOptions(
        hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)

    response = contents_service.create_document(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, attachments)
    click.echo(response)


@click.command(name='file')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@file_options
@standard_options
@click.pass_context
@exception_handler
def create_file(ctx, course_id: str, parent_id: str, title: str, file_path: str,
                launch_in_new_window: bool, hide_content: bool, reviewable: bool,
                start_date: str = None, end_date: str = None):
    """
    Creates a file content
    """

    file_options = FileOptions(launch_in_new_window)
    standard_options = StandardOptions(
        hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_file(
        ctx.obj['SESSION'], course_id, parent_id, title, file_path, file_options, standard_options)
    click.echo(response)


@click.command(name='web-link')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('url', required=True, type=str)
@standard_options
@web_link_options
@click.pass_context
def create_content(ctx, course_id: str, content_id: str):
    contents_service.test_create_assignment(
        ctx.obj['SESSION'], course_id, content_id)


def get_children(ctx, course_id, worklist):
    key = 'hasChildren'
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop(0)
        node_id = node.data['id']
        response = contents_service.get_children(
            ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            # return get_children(ctx, course_id, worklist, acc)
            pass
        else:
            children = response.json()['results']
            for child in children:
                if key in child and child[key] == True:
                    child_node = Node(child)
                    node.add_child(child_node)
                    worklist.append(child_node)
                else:
                    child_node = Node(child)
                    node.add_child(child_node)

            return get_children(ctx, course_id, worklist)


@exception_handler
def create_web_link(ctx, course_id: str, parent_id: str, title: str, url: str,
                    launch_in_new_window: bool, hide_content: bool, reviewable: bool,
                    start_date: str = None, end_date: str = None):
    """
    Create a web link content
    """
    web_link_options = WeblinkOptions(launch_in_new_window)
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_externallink(
        ctx.obj['SESSION'], course_id, parent_id, title, url, web_link_options, standard_options)
    click.echo(response)


@click.command(name='folder')
@click.argument('course_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.option('-p', '--parent_id', required=False, type=str, help='Id of parent folder')
@click.option('--is-bb-page', is_flag=True, help='Make folder a blackboard page')
@standard_options
@click.pass_context
@exception_handler
def create_folder(ctx, course_id: str, parent_id: str, title: str,
                  hide_content: bool, reviewable: bool, is_bb_page: bool = False,
                  start_date: str = None, end_date: str = None):
    """
    Create a folder either in top level or inside another content
    """
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_folder(
        ctx.obj['SESSION'], course_id, parent_id, title, is_bb_page, standard_options)
    click.echo(response)


@click.command(name='course-link')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('target_id', required=True, type=str)
@standard_options
@click.pass_context
@exception_handler
def create_courselink(ctx, course_id: str, parent_id: str, title: str, target_id: str,
                      hide_content: bool, reviewable: bool,
                      start_date: str = None, end_date: str = None):
    """
    Create a course link content which redirects user to the target content
    """
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_courselink(
        ctx.obj['SESSION'], course_id, parent_id, title, target_id, standard_options)
    click.echo(response)


@click.command(name='assignment')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@standard_options
@grading_options
@click.pass_context
@exception_handler
def create_assignment(ctx, course_id: str, parent_id: str, title: str,
                      hide_content: bool, reviewable: bool,
                      start_date: str, end_date: str,
                      due_date: str, max_attempts: int, unlimited_attempts: bool, score: int,
                      attachments: tuple):
    """
    Creates an assignment.
    """
    standard_options = StandardOptions(hide_content, reviewable)
    grading_options = GradingOptions(
        attempts_allowed=max_attempts, is_unlimited_attemps_allowed=unlimited_attempts, score_possible=score)

    set_dates(standard_options, start_date, end_date)
    grading_options.due = format_date(due_date)

    response = contents_service.create_assignment(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, grading_options, attachments)
    click.echo(response)


@click.command(name='delete')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.option('--delete-grades', is_flag=True, help='Deletes grades if a grade column is assosciated with the content.')
@click.pass_context
@exception_handler
def delete_content(ctx, course_id: str, content_id: str, delete_grades: bool):
    """
    Deletes a content
    """
    response = contents_service.delete_content(
        ctx.obj['SESSION'], course_id, content_id, delete_grades)
    click.echo(response)


@click.command(name='update')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.pass_context
@exception_handler
def update_content(ctx, course_id: str, content_id: str):
    """
    Updates a given content
    Editable content types: document, files, assignments, externallinks, courselinks
    """
    response = contents_service.update_content(
        ctx.obj['SESSION'], course_id, content_id)
    click.echo(response)


"""
HELPER FUNCTIONS
"""


def set_dates(standard_options: StandardOptions, start_date: str, end_date: str):
    if start_date:
        standard_options.date_interval.start_date = format_date(start_date)
    if end_date:
        standard_options.date_interval.end_date = format_date(end_date)
