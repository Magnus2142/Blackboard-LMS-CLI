import requests
#from requests.auth import HTTPBasicAuth
# import json
# import pprint
import bbcli.cli as cli
#from string_builder import StringBuilder
import click
# from typing import Optional
# from dotenv import load_dotenv
# from anytree import Node, RenderTree
import os



from bbcli import check_response

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

        click.echo(f'Name of the student: {fn} {sn}')
        click.echo(f'The student id: {id}')


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

def get_children(worklist, url, acc, count: int = 0):
    count = count + 1
    click.echo(f'kommer hit: {count}')
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc
    else:
        data = worklist.pop()
        id = data['id']
        old = f'{url}/{id}/children'
        response = requests.get(old, cookies = cli.cookies)
        if check_response(response) == False:
            return acc
        else:
            child = response.json()['results']
            for i in range(len(child)):
                if key in child[i] and child[i][key] == True:
                    worklist.append(child[i])
                else:
                    acc.append(child[i])
            return get_children(worklist, url, acc, count)



@click.command(name='get-assignments')
@click.argument('course_id', default='_27251_1')
def get_assignments(course_id: str):
    '''
    Get the assignments
    '''
    url = f'{base_url}courses/{course_id}/contents'
    response = requests.get(url, cookies=cli.cookies)
    if check_response(response) == False:
        return
    else:
        data = response.json()['results']
        root = data[8]
        # root = Node(data[8])
        worklist = [root]
        res = get_children(worklist, url, [])

        for i in res:
            print(i['title'])



    
