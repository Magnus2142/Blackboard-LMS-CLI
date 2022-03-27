import json
from subprocess import call
from typing import Dict, Any
import requests
from bbcli.services.course_service import list_courses
import click

from bbcli.utils.URL_builder import URLBuilder

url_builder = URLBuilder()

def list_announcements(cookies: Dict, user_name: str):
    courses = list_courses(cookies=cookies, user_name=user_name)

    session = requests.Session()
    announcements = []

    for course in courses:
        url = url_builder.base_v1().add_courses().add_id(course['id']).add_announcements().create()
        course_announcements = session.get(url, cookies=cookies)
        course_announcements = json.loads(course_announcements.text)
        
        # Adds the course name to each course announcement list to make it easier to display which course the announcement comes from
        if 'results' in course_announcements:
            announcements.append({
                    'course_name': course['name'],
                    'course_announcements': course_announcements['results']
                })
    
    return announcements

def list_course_announcements(cookies: Dict, course_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().create()
    course_announcements = requests.get(url, cookies=cookies)
    course_announcements = json.loads(course_announcements.text)['results']
    return course_announcements

def list_announcement(cookies: Dict, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    announcement = requests.get(url, cookies=cookies)
    announcement = json.loads(announcement.text)
    return announcement

# TODO: Add compatibility for flags and options to make a more detailed announcement
def create_announcement(cookies: Dict, headers: Dict, course_id: str, title: str):
    
    MARKER = '# Everything below is ignored\n'
    body = click.edit('\n\n' + MARKER)
    if body is not None:
        body = body.split(MARKER, 1)[0].rstrip('\n')
    
    data = {
        'title': title,
        'body': body
    }

    data = json.dumps(data)
    headers['Content-Type'] = 'application/json'
    
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().create()
    response = requests.post(url, cookies=cookies, headers=headers, data=data)

    return response.text

def delete_announcement(cookies: Dict, headers: Dict, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    response = requests.delete(url, cookies=cookies, headers=headers)
    if response.text == '':
        return 'Sucessfully deleted announcement!'
    else:
        return response.text

def update_announcement(cookies: Dict, headers: Dict, course_id: str, announcement_id: str):

    announcement = list_announcement(cookies=cookies, course_id=course_id, announcement_id=announcement_id)
    MARKER = '# Everything below is ignored\n'
    editable_data = {
        'title': announcement['title'],
        'body': announcement['body'],
        'created': announcement['created'],
        'availability': announcement['availability'],
        'draft': announcement['draft']
    }
    announcement = json.dumps(editable_data, indent=2)
    new_data = click.edit(announcement + '\n\n' + MARKER)

    headers['Content-Type'] = 'application/json'
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    response = requests.patch(url, cookies=cookies, headers=headers, data=new_data)
    response.raise_for_status()

    return response.text