import click
from bbcli.services import contents_service
# from bbcli.views.contents_view import list_tree, create_tree, get_content
from bbcli.views import contents_view
import time
import click

from anytree import Node as Nd, RenderTree

from bbcli import check_response
from bbcli.entities.Node import Node
from bbcli.entities.Node2 import Node2
from bbcli.utils.URL_builder import URLBuilder
from bbcli.utils.content_handler import content_handler

url_builder = URLBuilder()

base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'

@click.command(name='list')
@click.argument('course_id', default='_27251_1')
# @click.option('--folder-id')
@click.pass_context
def list_contents(ctx, course_id: str, folder_id=None):
    '''
    Get the contents\n
    Folders are blue and have an id \n
    Files are white
    '''
    start = time.time()

    response = contents_service.list_contents(ctx.obj['SESSION'], course_id, folder_id)
    folders = response.json()['results']
    roots = []
    for folder in folders:
        # root = Node(folder, True)
        root = Node2(folder)
        worklist = [root]
        get_children2(ctx, course_id, worklist)
        roots.append(root)
    
    for r in roots:
        # print(r)
        # root = Nd(r.data['title'])
        root = r.level_order(r)
        # for pre, fill, node in RenderTree(root):
        #     click.echo("%s%s" % (pre, node.name))

    end = time.time()

    print(f'\ndownload time: {end - start} seconds')

@click.command(name='get')
@click.argument('course_id', required=True, type=str)
@click.argument('node_id', required=True, type=str)
@click.pass_context
def get_content(ctx, course_id: str, node_id: str):
    response = contents_service.get_content(ctx.obj['SESSION'], course_id, node_id)
    data = response.json()
    if data['contentHandler']['id'] == content_handler['document']:
        contents_view.open_vim()
    elif data['contentHandler']['id'] == content_handler['file'] or data['contentHandler']['id'] == content_handler['document'] or data['contentHandler']['id'] == content_handler['assignment']:
        click.confirm("This is a .docx file, do you want to download it?", abort=True)
        response = contents_service.get_file(ctx.obj['SESSION'], course_id, node_id)
    elif data['contentHandler']['id'] == content_handler['folder']:
        root = Node(data, True)
        worklist = [root]
        res = get_children(ctx, course_id, worklist, [])
        contents_view.create_tree(root, res)
   

@click.command(name='create')
@click.argument('course_id', required=True, type=str)
@click.argument('content_id', required=True, type=str)
@click.pass_context
def create_content(ctx, course_id: str, content_id: str):
    contents_service.test_create_assignment(ctx.obj['SESSION'], course_id, content_id)

def get_children(ctx, course_id, worklist, acc, count: int = 0):
    count = count + 1
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc 
    else:
        node = worklist.pop()
        node_id = node.data['id']
        response = contents_service.get_children(ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            return acc
        else:
            children = response.json()['results']
            for i in range(len(children)):
                if key in children[i] and children[i][key] == True:
                    child = Node(children[i], True, node)
                    worklist.append(child)
                    acc.append(child)
                else:
                    child = Node(children[i], False, node)
                    acc.append(child)
            return get_children(ctx, course_id, worklist, acc)


def get_children2(ctx, course_id, worklist):
    key = 'hasChildren'
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop(0)
        node_id = node.data['id']
        response = contents_service.get_children(ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            # return get_children(ctx, course_id, worklist, acc)
            pass
        else:
            children = response.json()['results']
            for child in children:
                if key in child and child[key] == True:
                    child_node = Node2(child)
                    node.add_child(child_node)
                    worklist.append(child_node)
                else:
                    child_node = Node2(child)
                    node.add_child(child_node)
            
            return get_children2(ctx, course_id, worklist)
