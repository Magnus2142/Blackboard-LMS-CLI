from concurrent.futures import ThreadPoolExecutor
import time
from venv import create
import requests
import bbcli.cli as cli
import click
import os

from anytree import Node as Nd, RenderTree


from bbcli import check_response
from bbcli.Node import Node

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


def get_children(session, worklist, url, acc, count: int = 0):
    count = count + 1
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc
    else:
        node = worklist.pop()
        id = node.data['id']
        old = f'{url}/{id}/children'
        response = session.get(old, cookies=cli.cookies)
        if check_response(response) == False:
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
            return get_children(session, worklist, url, acc)


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


@click.command(name='get-assignments')
@click.argument('course_id', default='_27251_1')
def get_assignments(course_id: str):
    '''
    Get the assignments
    '''
    session = requests.Session()
    url = f'{base_url}courses/{course_id}/contents'
    start = time.time()
    response = session.get(url, cookies=cli.cookies)
    if check_response(response) == False:
        return
    else:
        data = response.json()['results']
        for root in data:
            root = Node(root, True)
            worklist = [root]
            res = get_children(session, worklist, url, [])
            create_tree(root, res)
    end = time.time()

    print(f'\ndownload time: {end - start} seconds')
