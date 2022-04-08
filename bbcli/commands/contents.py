from bbcli.utils.utils import format_date
from bbcli.utils.error_handler import exception_handler
import click
from bbcli.entities.content_builder_entitites import FileOptions, GradingOptions, StandardOptions, WeblinkOptions
from bbcli.services import contents_service
import time
import click
import threading
import concurrent.futures

from bbcli.entities.Node import Node
from bbcli.utils.URL_builder import URL_builder
from bbcli.utils import content_utils
from bbcli.utils.content_handler import content_handler
from bbcli.views import contents_view

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
@click.argument('course_id')
@click.option('-f', '--folders', required=False, is_flag=True, help='Specify this if you want to only list folders.')
@click.option('-t', '--threads', required=False, is_flag=True, help='Specify this if you want to run with threads')
@click.option('--content-type', required=False, type=click.Choice(content_handler.keys(), case_sensitive=False))
@click.pass_context
@exception_handler
def list_contents(ctx, course_id: str, content_type, folders: bool = False, threads: bool = True):
    '''
    Get the contents\n
    Folders are blue and have an id \n
    Files are white
    '''
    click.echo('Loading...')
    start = time.time()

    response = contents_service.list_contents(ctx.obj['SESSION'], course_id)
    data = response.json()['results']
    folder_ids = dict()
    node_ids = dict()

    if threads == False:
        for node in data:
            root = Node(node)
            worklist = [root]
            folder_ids[node['title']] = node['id']
            root_node = content_utils.list_contents_thread(ctx, course_id, worklist, folder_ids, node_ids, root, folders, content_type)
            if root_node is not None:
                contents_view.list_tree(root_node, folder_ids, node_ids, only_folders=folders)
            else:
                return
    else:
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for node in data:
                root = Node(node)
                worklist = [root]
                folder_ids[node['title']] = node['id']
                args = [ctx, course_id, worklist, folder_ids, node_ids, root, folders, content_type]
                t = executor.submit(content_utils.list_contents_thread, *args)
                threads.append(t)
                
        for t in threads:
            root_node = t.result()
            if root_node is not None:
                contents_view.list_tree(root_node, folder_ids, node_ids, only_folders=folders)
            else: return 

        # [t.join() for t in threads]

    end = time.time()

    print(f'\ndownload time: {end - start} seconds')


@click.command(name='get')
@click.argument('course_id', required=True, type=str)
@click.argument('node_id', required=True, type=str)
@click.pass_context
def get_content(ctx, course_id: str, node_id: str):
    content_utils.check_content_handler(ctx, course_id, node_id)
    

@click.command(name='attachment', help='Adds an attachment to a content. Only supports contents of type document and assignment')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@click.pass_context
@exception_handler
def upload_attachment(ctx, course_id: str, content_id: str, file_path: str):
    contents_service.upload_attachment(ctx.obj['SESSION'], course_id, content_id, file_path)


@click.command(name='document', help='Creates a document content, optionally with file attachments')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@standard_options
@click.pass_context
@exception_handler
def create_document(ctx, course_id: str, parent_id: str, title: str, hide_content: bool, reviewable: bool, start_date: str=None, end_date: str=None, attachments: tuple=None):
    standard_options = StandardOptions(hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)

    response = contents_service.create_document(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, attachments)
    click.echo(response)


@click.command(name='file', help='Creates a file content.')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('file_path', required=True, type=click.Path(exists=True))
@file_options
@standard_options
@click.pass_context
@exception_handler
def create_file(ctx, course_id: str, parent_id: str, title: str, file_path: str, 
                        launch_in_new_window:bool, hide_content: bool, reviewable: bool,
                        start_date: str=None, end_date: str=None):
    file_options = FileOptions(launch_in_new_window)
    standard_options = StandardOptions(
        hide_content=hide_content, reviewable=reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_file(
        ctx.obj['SESSION'], course_id, parent_id, title, file_path, file_options, standard_options)
    click.echo(response)


@click.command(name='web-link', help='Create a web link content.')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('url', required=True, type=str)
@standard_options
@web_link_options
@click.pass_context
@exception_handler
def create_web_link(ctx, course_id: str, parent_id: str, title: str, url: str, 
                        launch_in_new_window:bool, hide_content: bool, reviewable: bool,
                        start_date: str=None, end_date: str=None):
    web_link_options = WeblinkOptions(launch_in_new_window)
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_externallink(
        ctx.obj['SESSION'], course_id, parent_id, title, url, web_link_options, standard_options)
    click.echo(response)


@click.command(name='folder', help='Create a folder either in top level or inside another content.')
@click.argument('course_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.option('-p', '--parent_id', required=False, type=str, help='Id of parent folder')
@click.option('--is-bb-page', is_flag=True, help='Make folder a blackboard page')
@standard_options
@click.pass_context
@exception_handler
def create_folder(ctx, course_id: str, parent_id: str, title: str,
                        hide_content: bool, reviewable: bool, is_bb_page: bool = False,
                        start_date: str=None, end_date: str=None):
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_folder(
        ctx.obj['SESSION'], course_id, parent_id, title, is_bb_page, standard_options)
    click.echo(response)
    
@click.command(name='course-link', help='Create a course link content which redirects user to the target content.')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('target_id', required=True, type=str)
@standard_options
@click.pass_context
@exception_handler
def create_courselink(ctx, course_id: str, parent_id: str, title: str, target_id: str,
                        hide_content: bool, reviewable: bool, 
                        start_date: str=None, end_date: str=None):
    standard_options = StandardOptions(hide_content, reviewable)
    set_dates(standard_options, start_date, end_date)
    response = contents_service.create_courselink(
        ctx.obj['SESSION'], course_id, parent_id, title, target_id, standard_options)
    click.echo(response)
    
@click.command(name='assignment', help='Creates an assignment.')
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
                        due_date: str, max_attempts:int, unlimited_attempts: bool, score: int,
                        attachments: tuple):
    standard_options = StandardOptions(hide_content, reviewable)
    grading_options = GradingOptions(
        attempts_allowed=max_attempts, is_unlimited_attemps_allowed=unlimited_attempts, score_possible=score)

    set_dates(standard_options, start_date, end_date)
    grading_options.due = format_date(due_date)

    response = contents_service.create_assignment(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, grading_options, attachments)
    click.echo(response)


@click.command(name='delete', help='Deletes a content.')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.option('--delete-grades', is_flag=True, help='Deletes grades if a grade column is assosciated with the content.')
@click.pass_context
@exception_handler
def delete_content(ctx, course_id: str, content_id: str, delete_grades: bool):
    response = contents_service.delete_content(ctx.obj['SESSION'], course_id, content_id, delete_grades)
    click.echo(response)

@click.command(name='update', help='Updates a given content.\nEditable content types: document, files, assignments, externallinks, courselinks')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.pass_context
@exception_handler
def update_content(ctx, course_id: str, content_id: str):
    response = contents_service.update_content(ctx.obj['SESSION'], course_id, content_id)
    click.echo(response)


"""
HELPER FUNCTIONS
"""


def set_dates(standard_options: StandardOptions, start_date: str, end_date: str):
    if start_date:
        standard_options.date_interval.start_date = format_date(start_date)
    if end_date:
        standard_options.date_interval.end_date = format_date(end_date)
