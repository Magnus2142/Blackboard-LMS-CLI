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



app = typer.Typer()


load_dotenv()
cookies = {'BbRouter' : os.getenv("BB_ROUTER")}
headers = {'X-Blackboard-XSRF': os.getenv('XSRF')}
base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@app.command(name='get-user')
def get_user(user_name: str = typer.Argument('', help='Name of the user'))-> None:
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

def get_children(worklist, url, acc, count: int = 0):
    count = count + 1
    typer.echo(f'kommer hit: {count}')
    # print("The acc is: ", acc)
    key = 'hasChildren'
    if len(worklist) == 0:
        return acc
    else:
        data = worklist.pop()
        id = data['id']
        old = f'{url}/{id}/children'
        # typer.echo(url)
        response = requests.get(old, cookies = cookies)
        if response.status_code == 403 or response.status_code == 404:
            typer.echo(response.json()['status'])
            typer.echo(response.json()['message'])
            return acc
        else:
            child = response.json()['results']
            for i in range(len(child)):
                if key in child[i] and child[i][key] == True:
                    worklist.append(child[i])
                else:
                    acc.append(child[i])
            # parent = worklist.pop()
            return get_children(worklist, url, acc, count)



@app.command(name='get-assignments')
def get_assignments(course_id: str = typer.Argument('_27251_1', help='The course id')):
    '''
    Get the assignments
    '''
    url = f'{base_url}courses/{course_id}/contents'
    x = requests.get(url, cookies=cookies)
    data = x.json()['results']
    root = data[8]
    # root = Node(data[8])
    worklist = [root]
    res = get_children(worklist, url, [])

    for i in res:
        print(i['title'])



    
