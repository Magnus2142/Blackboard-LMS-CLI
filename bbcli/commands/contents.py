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




import time
import requests
import bbcli.cli as cli
import click

from anytree import Node as Nd, RenderTree
from colorama import Fore, Style

from bbcli import check_response
from bbcli.entities.Node import Node
from bbcli.entities.Node2 import Node2
from bbcli.utils.URL_builder import URLBuilder

url_builder = URLBuilder()

base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'

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
                root = Node(folder, True)
                worklist = [root]
                get_children(session, worklist, url, [])
                print(root.data['title'])

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
