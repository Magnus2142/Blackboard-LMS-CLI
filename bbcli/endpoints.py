import requests
#from requests.auth import HTTPBasicAuth
import json
import pprint
import typer
from string_builder import StringBuilder

app = typer.Typer()


cookies = {'BbRouter': 'expires:1645028532,id:FB0C2EC2C0F7E65CBF8DA06E10933C29,signature:e283fbd97b70959a733dd7a18e23db8a5420fe305678f468b53a29dc1c9fc01a,site:f4fe20be-98b0-4ecd-9039-d18ce2989292,timeout:10800,user:15bd75dd85af4f56b31283276eb8da7c,v:2,xsrf:6d7d4b40-4fb4-40b9-8d4c-800162d2137a'}
base_str = 'https://ntnu.blackboard.com/learn/api/public/v1/'


@app.command()
def getuser(user_name: str):
    '''
    url = StringBuilder()
    url.append(base_str)
    url.append('users?userName=')
    url.append(user_name)
    print(url)
    '''
    url = 'https://ntnu.blackboard.com/learn/api/public/v1/users?userName=%s' % user_name
    x = requests.get(
        url,
        cookies=cookies
    )

    data = x.json()
    # print(data)
    print(pprint.pprint(data))


@app.command()
def getcourse(course_id: str):
    url = 'https://ntnu.blackboard.com/learn/api/public/v1/courses?courseId=%s' % course_id
    x = requests.get(
        url,
        cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


@app.command()
def getcoursecontents():
    id: str = '_27251_1'
    url = 'https://ntnu.blackboard.com/learn/api/public/v1/courses/%s/contents' % id
    x = requests.get(url, cookies=cookies)
    data = x.json()
    print(pprint.pprint(data))


if __name__ == "__main__":
    '''
    sb = StringBuilder()
    sb.append("Hello")
    sb.append("World")
    print(sb)
    '''
    app()