import json
from subprocess import call
from typing import Dict, Any
import requests
from bbcli.services.courses_service import list_courses
from bbcli.utils.utils import set_cookies
import click

from bbcli.utils.URL_builder import URLBuilder

url_builder = URLBuilder()

def list_announcements(session: requests.Session, user_name: str):
    courses = list_courses(session, user_name=user_name)
    announcements = []

    for course in courses:
        url = url_builder.base_v1().add_courses().add_id(course['id']).add_announcements().create()
        course_announcements = session.get(url)
        course_announcements = json.loads(course_announcements.text)
        
        # Adds the course name to each course announcement list to make it easier to display which course the announcement comes from
        if 'results' in course_announcements:
            announcements.append({
                    'course_name': course['name'],
                    'course_announcements': course_announcements['results']
                })
    
    return announcements

def list_course_announcements(session: requests.Session, course_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().create()
    course_announcements = session.get(url)
    course_announcements.raise_for_status()
    course_announcements = json.loads(course_announcements.text)['results']
    return course_announcements

def list_announcement(session: requests.Session, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    announcement = session.get(url)
    announcement = json.loads(announcement.text)
    return announcement

# TODO: Add compatibility for flags and options to make a more detailed announcement
def create_announcement(session: requests.Session, course_id: str, title: str):
    MARKER = '# Everything below is ignored\n'
    body = click.edit('\n\n' + MARKER)
    if body is not None:
        body = body.split(MARKER, 1)[0].rstrip('\n')
    
    data = {
        'title': title,
        'body': body
    }

    data = json.dumps(data)
    session.headers.update({'Content-Type': 'application/json'})

    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().create()
    response = session.post(url, data=data)

    return response.text

def delete_announcement(session: requests.Session, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    response = session.delete(url)
    if response.text == '':
        return 'Sucessfully deleted announcement!'
    else:
        return response.text

def update_announcement(session: requests.Session, course_id: str, announcement_id: str):

    announcement = list_announcement(session=session, course_id=course_id, announcement_id=announcement_id)
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

    session.headers.update({'Content-Type': 'application/json'})

    url = url_builder.base_v1().add_courses().add_id(course_id).add_announcements().add_id(announcement_id).create()
    response = session.patch(url, data=new_data)

    return response.text