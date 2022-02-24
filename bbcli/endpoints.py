import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint 
import typer
#from string_builder import StringBuilder
import click
from typing import Optional

app = typer.Typer()

cookies = {'BbRouter' : 'expires:1645724548,id:CBD8467556E3976D9F7047190DC6F82D,signature:4a5b5bbf51712187e3c59b9374c42d4d0f62409b32504b200f5d49bc1636f7f1,site:f4fe20be-98b0-4ecd-9039-d18ce2989292,timeout:10800,user:15bd75dd85af4f56b31283276eb8da7c,v:2,xsrf:fd102c30-042c-4135-a515-a293ed638ba5'}
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

def get_children(d, url,acc, count: int = 0):
    #count = count + 1
    #typer.echo(f'kommer hit: {count}')
    key = 'hasChildren'
    if key not in d or d[key] == False:
        typer.echo('nei')
        return acc
    else:
        typer.echo('ja')
        id = d['id']
        url = f'{url}/{id}/children'
        typer.echo(url)
        response = requests.get(url, cookies = cookies)
        child = response.json()['results']
        get_children(child, url, acc+child, count)
        # return child

def get_children(d, url):
    key = 'hasChildren'
    while key in d and d[key] == True:
        id = d['id']
        url = f'{url}/{id}/children'
        typer.echo()
        typer.echo(url)
        typer.echo()
        response = requests.get(url, cookies=cookies)
        child = response.json()['results']
        return child



@app.command(name='get-assignments')
def get_assignments(course_id: str = typer.Argument('_27251_1', help='The course id')):
    '''
    Get the assignments
    '''
    url = f'{base_url}courses/{course_id}/contents'
    x = requests.get(url, cookies=cookies)
    data = x.json()['results']
    #res = get_children(data[2], url, [])
    res = get_children(data[2], url)
    #typer.echo(ptyper.echo.ptyper.echo(res))
    for o in res:
        typer.echo(o['title'])
    #typer.echo(ptyper.echo.ptyper.echo(data))
    #for d in data:
        #typer.echo()
        #typer.echo(get_children(d, url))
