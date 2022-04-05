from concurrent.futures import ThreadPoolExecutor
import time
from venv import create
import requests
import bbcli.cli as cli
import click
import os
from colorama import Fore, Style

from anytree import Node as Nd, RenderTree


from bbcli import check_response
from bbcli.entities.Node import Node
from bbcli.entities.Node import Node2
from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()

base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@click.command(name='get-user')
@click.argument('user_name', default='')
def get_user(user_name: str):
    '''
    Get the user
    Specify the user_name as an option, or else it will use the default user_name
    '''
    if user_name == '':
        user_name = click.prompt("What is your user name?")
    url = f'{base_url}users?userName={user_name}'
    response = requests.get(
        url,
        cookies=cli.cookies
    )
    if check_response(response) == False:
        return
    else:
        data = response.json()['results'][0]
        fn = data['name']['given']
        sn = data['name']['family']
        id = data['studentId']

        click.echo(f'Student name: {fn} {sn}')
        click.echo(f'Student ID: {id}')


@click.command(name='get-course')
@click.argument('course_id', default='IDATT2900')
def get_course(course_id: str):
    '''
    Get the course
    '''
    if course_id == '':
        course_id = click.prompt("What is the course id?")
    url = f'{base_url}courses?courseId={course_id}'
    response = requests.get(
        url,
        cookies=cli.cookies)
    if check_response(response) == False:
        return
    else:
        data = response.json()['results'][0]
        name = data['name']
        course_url = data['externalAccessUrl']
        click.echo(name)
        click.echo(f'URL for the course: {course_url}')


@click.command(name='get-course-contents')
@click.argument('course_id', default='_27251_1')
def get_course_contents(course_id: str):
    '''
    Get the course contents
    '''
    url = f'{base_url}courses/{course_id}/contents'
    click.echo(url)
    response = requests.get(url, cookies=cli.cookies)
    if check_response(response) == False:
        return
    else:
        data = response.json()['results']
        click.echo('Mapper:')
        map = dict()
        for i in range(len(data)):
            title = data[i]['title']
            map[i+1] = data[i]['id']
            click.echo(f'{i+1} {title}')
        click.echo(map)


content_types = dict()
content_types['assignments'] = 'resource/x-bb-assignment'
content_types['blankpage'] = 'resource/x-bb-blankpage'
content_types['folder'] = 'resource/x-bb-folder'


def get_children(session, worklist, url, acc, count: int = 0):
    count = count + 1
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc
    else:
        node = worklist.pop()
        id = node.data['id']
        tmp = url[:url.index('contents') + len('contents')]
        old = f'{tmp}/{id}/children'
        response = session.get(old, cookies=cli.cookies)
        if check_response(response) == False:
            return acc
        else:
            children = response.json()['results']
            for i in range(len(children)):
                # TODO: Add list of children instead of bool
                if key in children[i] and children[i][key] == True:
                    # if children[i]['contentHandler'] == content_types['folder']:
                    child = Node(children[i], True, node)
                    worklist.append(child)
                    acc.append(child)
                else:
                    child = Node(children[i], False, node)
                    acc.append(child)
            return get_children(session, worklist, url, acc)


def get_children2(session, worklist, url, acc, count: int = 0):
    count = count + 1
    key = 'hasChildren'
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop()
        id = node.data['id']
        tmp = url[:url.index('contents') + len('contents')]
        old = f'{tmp}/{id}/children'
        response = session.get(old, cookies=cli.cookies)
        if check_response(response) == False:
            return acc
        else:
            children = response.json()['results']
            parent = Node2(node)
            for i in range(len(children)):
                # TODO: Add list of children instead of bool
                if key in children[i] and children[i][key] == True:
                    # if children[i]['contentHandler'] == content_types['folder']:
                    # child = Node(children[i], True, parent)
                    child = Node2(children[i])
                    parent.children.append(child)
                    worklist.append(child)
                    # acc.append(child)
                else:
                    child = Node2(children[i])
                    parent.children.append(child)
                    # child = Node(children[i], False, parent)
                    # acc.append(child)
            return get_children(session, worklist, url, acc)


def create_tree(root, nodes):
    parents = []
    root_node = Nd(root.data['title'])
    parent = root_node
    parents.append(parent)
    folders = dict()
    folders[root.data['title']] = root.data['id']

    for i in range(len(nodes)):
        id = nodes[i].data['id']
        title = nodes[i].data['title']
        if (nodes[i].has_children):
            for parent in parents:
                if (parent.name == nodes[i].parent.data['title']):
                    node = Nd(title, parent)
                    folders[title] = id
                    parents.append(node)
                    continue

            node = Nd(title, root_node)
            folders[title] = id
            parents.append(node)

        else:
            for parent in parents:
                if (parent.name == nodes[i].parent.data['title']):
                    node = Nd(title, parent)
                    folders[title] = ''

    for pre, fill, node in RenderTree(root_node):
        folder_id = folders[node.name]
        if folder_id == '':
            print("%s%s" % (pre, node.name))
        else:
            print(f'{pre}{Fore.BLUE}{folder_id} {node.name} {Style.RESET_ALL}')


@click.command(name='get-contents')
@click.argument('course_id', default='_27251_1')
@click.option('--folder-id')
def get_contents(course_id: str, folder_id=None):
    '''
    Get the contents\n
    Folders are blue and have an id \n
    Files are white
    '''
    session = requests.Session()
    if folder_id is not None:
        url = f'{base_url}courses/{course_id}/contents/{folder_id}'
    else:
        url = f'{base_url}courses/{course_id}/contents'
    start = time.time()
    response = session.get(url, cookies=cli.cookies)
    if check_response(response) == False:
        return
    else:
        if folder_id is not None:
            data = response.json()
            root = Node(data, True)
            worklist = [root]
            res = get_children(session, worklist, url, [])
            create_tree(root, res)
        else:
            folders = response.json()['results']
            root = None
            for folder in folders:
                # root = Node(folder, True)
                root = Node2(folder)
                worklist = [root]
                get_children2(session, worklist, url, [])
                print(root.data['title'])
                # create_tree(root, res)
            for child in root.children:
                print(child.data['title'])

    end = time.time()

    print(f'\ndownload time: {end - start} seconds')


def list_tree(root, contents):
    for content in contents:
        parent = Nd(content.parent.data['title'])
        this = Nd(content.data['title'], parent)

    for pre, fill, node in RenderTree(root_node):
        print("%s%s" % (pre, node.name))
