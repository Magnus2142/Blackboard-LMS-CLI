import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
#from string_builder import StringBuilder
import click

app = typer.Typer()


cookies = {'BbRouter': 'expires:1645188702,id:0E5CC03E415FE4459D9F34DDDFC4AEE7,signature:4e8d6fc59c11f744f6350399dc8cdf14f65a2c26d20e7d53c97141749e9056ac,site:f4fe20be-98b0-4ecd-9039-d18ce2989292,timeout:10800,user:15bd75dd85af4f56b31283276eb8da7c,v:2,xsrf:ac218e34-3110-415c-8718-bd0c8c8bcc8c'}
base_url = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@app.command()
def getuser(user_name: str = 'hanswf') -> None:
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
    url = base_url + 'courses/%s/contents' % course_id
    x = requests.get(url, cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


if __name__ == "__main__":
    app()