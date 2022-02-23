import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
#from string_builder import StringBuilder
import click
from typing import Optional

app = typer.Typer()

cookies = {'BbRouter': 'expires:1645202601,id:2480855EED2012DA032F19DEE1610883,signature:81a13d5bdf4946a82a632a9035c0f35811f217671da872677b1d1c32e7a3c339,site:f4fe20be-98b0-4ecd-9039-d18ce2989292,timeout:10800,user:15bd75dd85af4f56b31283276eb8da7c,v:2,xsrf:1bea7fee-fa91-4197-991f-1d266fd1ceee'}
base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@app.command()
def getuser(user_name: str = typer.Argument('hanswf', help='Name of the user'))-> None:
    '''
    Get the user. 
    Specify the user_name as an option, or else it will use the default user_name
    '''
    url = base_url + 'users?userName=%s' % user_name
    x = requests.get(
        url,
        cookies=cookies
    )

    data = x.json()
    # print(data)
    print(pprint.pprint(data))


@app.command()
def getcourse(course_id: str = 'IDATT2900'):
    url = base_url + 'courses?courseId=%s' % course_id
    x = requests.get(
        url,
        cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


@app.command()
def getcoursecontents(course_id: str = '_27251_1'):
    url = f'{base_url}courses/{course_id}/contents'
    x = requests.get(url, cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


if __name__ == "__main__":
    app()