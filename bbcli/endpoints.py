import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
#from string_builder import StringBuilder
import click
from typing import Optional

app = typer.Typer()

base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'
cookies = {'BbRouter': 'expires:1645636281,id:B2D974616358A83C4663CE3CEC57040F,signature:c77518e494765a09f4cc1b8d390964f05da9d35a1fcdf88350dd105b7151cce6,site:f4fe20be-98b0-4ecd-9039-d18ce2989292,timeout:10800,user:7fa494bb9cd54a7395923f41a1771ccc,v:2,xsrf:2692c68d-69f7-4ec8-b67b-f2a56b2cb85a'}
headers = {'X-Blackboard-XSRF': '2692c68d-69f7-4ec8-b67b-f2a56b2cb85a',
           'Content-Type': 'application/json'}


@app.command()
def postannouncement(title: str = typer.Option(..., '--title', '-t', prompt=True), body: str = typer.Option(..., '--body', '-b', prompt=True), config: typer.FileText = typer.Option(...)):

    data = {
        "title": title,
        "body": body,
        "availability": {
            "duration": {
                "type": "Permanent",
                "start": "2022-02-21T18:03:42.241Z",
                "end": "2022-02-21T18:03:42.241Z"
            }
        },
    }

    data = json.dumps(data)

    url = f'{base_url}courses/_33050_1/announcements'
    x = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        data=data)

    typer.echo(x.text)


@app.command()
def getuser(user_name: str = typer.Argument('hanswf', help='Name of the user')) -> None:
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
