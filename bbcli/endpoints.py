from venv import create
import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
#from string_builder import StringBuilder
import click
from typing import Optional
from dotenv import load_dotenv
from bbcli.Node import Node
import os

from anytree import Node as Nd, RenderTree


app = typer.Typer()


load_dotenv()
cookies = {'BbRouter': os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}
base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@app.command(name='get-user')
def get_user(user_name: str = typer.Argument('', help='Name of the user')) -> None:
    '''
    Get the user
    Specify the user_name as an option, or else it will use the default user_name
    '''
    if user_name == '':
        user_name = typer.prompt("What is your user name?")
    url = f'{base_url}users?userName={user_name}'
    x = requests.get(
        url,
        cookies=cookies
    )

    data = x.json()['results'][0]
    # typer.echo(data)
    fn = data['name']['given']
    sn = data['name']['family']
    id = data['studentId']

    typer.echo(f'Name of the student: {fn} {sn}')
    typer.echo(f'The student id: {id}')


@app.command(name='get-course')
def get_course(course_id: str = typer.Argument('', help='Id of the course')):
    '''
    Get the course
    '''
    if course_id == '':
        course_id = typer.prompt("What is the course id?")
    url = f'{base_url}courses?courseId={course_id}'
    x = requests.get(
        url,
        cookies=cookies)
    data = x.json()['results'][0]
    name = data['name']
    course_url = data['externalAccessUrl']
    typer.echo(name)
    typer.echo(f'URL for the course: {course_url}')

# def open_folder(data, map):
#     key = 'hasChildren'
#     acc = []
#     if key in data and data[key] == True:
#         acc.append


@app.command(name='get-course-contents')
def get_course_contents(course_id: str = '_27251_1'):
    '''
    Get the course contents
    '''
    url = f'{base_url}courses/{course_id}/contents'
    typer.echo(url)
    x = requests.get(url, cookies=cookies)
    data = x.json()['results']
    typer.echo('Mapper:')
    map = dict()
    for i in range(len(data)):
        title = data[i]['title']
        map[i+1] = data[i]['id']
        typer.echo(f'{i+1} {title}')
    # idx = typer.prompt("Open a folder by pressing a number: ")
    typer.echo(map)
    # for d in data:
    # typer.echo(d['title'])


def get_children(worklist, url, acc):
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc
    else:
        node = worklist.pop()
        id = node.data['id']
        old = f'{url}/{id}/children'
        response = requests.get(old, cookies=cookies)
        if response.status_code == 403 or response.status_code == 404:
            typer.echo(response.json()['status'])
            typer.echo(response.json()['message'])
            return acc
        else:
            children = response.json()['results']
            for i in range(len(children)):
                # TODO: Add list of children instead of bool
                if key in children[i] and children[i][key] == True:
                    child = Node(children[i], True, node)
                    worklist.append(child)
                    acc.append(child)
                else:
                    child = Node(children[i], False, node)
                    acc.append(child)
            return get_children(worklist, url, acc)


def create_tree(root, nodes):
    parents = []
    root_node = Nd(root.data['title'])
    parent = root_node
    parents.append(parent)

    for i in range(len(nodes)):
        if (nodes[i].children and nodes[i] not in parents):
            for parent in parents:
                if (parent == nodes[i].parent.data['title']):
                    node = Nd(nodes[i].data['title'], parent)
                    parents.append(node)
                    continue

            node = Nd(nodes[i].data['title'], root_node)
            parents.append(node)

        elif (nodes[i].children):
            for parent in parents:
                if (nodes[i].parent.data['title'] == parent):
                    node = Nd(node.data['title'], parent)
        if (nodes[i].children is False):
            for parent in parents:
                if (parent.name == nodes[i].parent.data['title']):
                    node = Nd(nodes[i].data['title'], parent)

    for pre, fill, node in RenderTree(root_node):
        print("%s%s" % (pre, node.name))


@app.command(name='get-assignments')
def get_assignments(course_id: str = typer.Argument('_32909_1', help='The course id')):
    '''
    Get the assignments
    '''
    url = f'{base_url}courses/{course_id}/contents'
    x = requests.get(url, cookies=cookies)
    data = x.json()['results']

    

    for root in data:
        root = Node(root, True)
        worklist = [root]
        res = get_children(worklist, url, [])
        create_tree(root, res)
