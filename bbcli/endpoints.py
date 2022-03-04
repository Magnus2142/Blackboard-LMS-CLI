import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
#from string_builder import StringBuilder
import click
from typing import Optional
from dotenv import load_dotenv
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

    data = x.json()
    # print(data)
    print(pprint.pprint(data))


@app.command(name='get-course')
def get_course(course_id: str = 'IDATT2900'):
    '''
    Get the course
    '''
    url = base_url + 'courses?courseId=%s' % course_id
    x = requests.get(
        url,
        cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


@app.command(name='get-course-contents')
def get_course_contents(course_id: str = '_27251_1'):
    '''
    Get the course contents
    '''
    url = f'{base_url}courses/{course_id}/contents'
    x = requests.get(url, cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))

def get_children(d, url,acc, count: int = 0):
    #count = count + 1
    #print(f'kommer hit: {count}')
    key = 'hasChildren'
    if key not in d or d[key] == False:
        print('nei')
        return acc
    else:
        print('ja')
        id = d['id']
        url = f'{url}/{id}/children'
        print(url)
        response = requests.get(url, cookies = cookies)
        child = response.json()['results']
        #get_children(child, url, acc+child, count)
        return child

def get_children(d, url):
    key = 'hasChildren'
    while key in d and d[key] == True:
        id = d['id']
        url = f'{url}/{id}/children'
        print()
        print(url)
        print()
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
    print(pprint.pprint(res))
    #print(pprint.pprint(data))
    #for d in data:
        #print()
        #print(get_children(d, url))
