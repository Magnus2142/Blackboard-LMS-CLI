from datetime import datetime
import json
from subprocess import call
from typing import Dict, Any, List
import requests
from bbcli.entities.content_builder_entitites import DateInterval
from bbcli.services.courses_services import list_all_courses
from bbcli.utils.utils import input_body
import click
import markdown
import markdownify

from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()


def list_announcements(session: requests.Session, user_name: str) -> List:
    courses = list_all_courses(session, user_name=user_name)
    announcements = []
    for course in courses:
        course_announcements = list_course_announcements(session, course['id'], True)

        # Adds the course name to each course announcement list to make it easier to display which course the announcement comes from
        if 'results' in course_announcements:
            announcements.append({
                'course_name': course['name'],
                'course_announcements': course_announcements
            })
    return announcements

def list_course_announcements(session: requests.Session, course_id: str, allow_bad_request: bool=False) -> Dict:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().create()
    course_announcements = session.get(url)
    if not allow_bad_request:
        course_announcements.raise_for_status()
    course_announcements = json.loads(course_announcements.text)
    return course_announcements

def list_announcement(session: requests.Session, course_id: str, announcement_id: str) -> Dict:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    announcement = session.get(url)
    announcement.raise_for_status()
    announcement = json.loads(announcement.text)
    return announcement

def create_announcement(session: requests.Session, course_id: str, title: str, date_interval: DateInterval, is_markdown: bool) -> Dict:
    if title == '':
        raise click.BadParameter('Argument TITLE cannot be empty!')
    
    body = input_body()
    if is_markdown:
        body = markdown.markdown(body)
    data = {
        'title': title,
        'body': body
    }
    if date_interval:
        start_date_str = datetime.strftime(
            date_interval.start_date, '%Y-%m-%dT%H:%m:%S.%fZ') if date_interval.start_date else None
        end_date_str = datetime.strftime(
            date_interval.end_date, '%Y-%m-%dT%H:%m:%S.%fZ') if date_interval.end_date else None

        data.update({
            'availability': {
                'duration': {
                    'start': start_date_str,
                    'end': end_date_str
                }
            }
        })

    data = json.dumps(data)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().create()
    response = session.post(url, data=data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response


def delete_announcement(session: requests.Session, course_id: str, announcement_id: str) -> str:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    response = session.delete(url)
    response.raise_for_status()
    return response.text


def update_announcement(session: requests.Session, course_id: str, announcement_id: str, is_markdown: bool) -> Dict:

    announcement = list_announcement(
        session=session, course_id=course_id, announcement_id=announcement_id)
    
    new_title = edit_title(announcement)
    new_data = edit_body(announcement, is_markdown)

    data = json.dumps({
        'title': new_title,
        'body': new_data
    })

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    response = session.patch(url, data=data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response

def update_announcement_advanced(session: requests.Session, course_id: str, announcement_id: str, is_markdown: bool) -> Dict:
    announcement = list_announcement(
        session=session, course_id=course_id, announcement_id=announcement_id)
    if is_markdown:
        announcement['body'] = markdownify.markdownify(announcement['body'])

    MARKER = '# Everything below is ignored.\n'

    announcement = json.dumps(announcement, indent=2)
    data = click.edit(announcement + '\n\n' + MARKER)
    new_data = data if data != None else announcement
    if new_data is not None:
        new_data = new_data.split(MARKER, 1)[0].rstrip('\n')

    if is_markdown:
        new_data = json.loads(new_data)
        new_data['body'] = markdown.markdown(new_data['body'])
        new_data = json.dumps(new_data, indent=2)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    response = session.patch(url, data=new_data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response

"""
HELPER FUNCTIONS
"""

def edit_title(data: Dict) -> str:
    MARKER_TITLE = '# Edit title. Everything below is ignored.\n'
    title = click.edit(data['title'] + '\n\n' + MARKER_TITLE)
    new_title = title if title != None else data['title']
    if new_title is not None:
        new_title = new_title.split(MARKER_TITLE, 1)[0].rstrip('\n')
    return new_title

def edit_body(data: Dict, is_markdown: bool) -> str:
    try:
        data['body']
    except KeyError:
        data['body'] = ''
    if is_markdown:
        data['body'] = markdownify.markdownify(data['body'])
    MARKER_BODY = '# Edit body. Everything below is ignored.\n'
    body = click.edit(data['body'] + '\n\n' + MARKER_BODY)
    new_body = body if body != None else data['body']
    if new_body is not None:
        new_body = new_body.split(MARKER_BODY, 1)[0].rstrip('\n')
    if is_markdown:
        new_body = markdown.markdown(new_body)
    return new_body