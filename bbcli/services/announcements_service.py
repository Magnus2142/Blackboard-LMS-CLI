from datetime import datetime
import json
from subprocess import call
from typing import Dict, Any
import requests
from bbcli.entities.content_builder_entitites import DateInterval
from bbcli.services.courses_service import list_courses
from bbcli.utils.utils import input_body, set_cookies
import click

from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()


def list_announcements(session: requests.Session, user_name: str):
    courses = list_courses(session, user_name=user_name)
    announcements = []

    for course in courses:
        url = url_builder.base_v1().add_courses().add_id(
            course['id']).add_announcements().create()
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
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().create()
    course_announcements = session.get(url)
    course_announcements.raise_for_status()
    course_announcements = json.loads(course_announcements.text)['results']
    return course_announcements


def list_announcement(session: requests.Session, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    announcement = session.get(url)
    announcement = json.loads(announcement.text)
    return announcement

# TODO: Test if the duration actually makes it unavailable/available when it should


def create_announcement(session: requests.Session, course_id: str, title: str, date_interval: DateInterval):
    body = input_body()

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

    return response.text


def delete_announcement(session: requests.Session, course_id: str, announcement_id: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    response = session.delete(url)
    response.raise_for_status()
    return response.text


def update_announcement(session: requests.Session, course_id: str, announcement_id: str):

    announcement = list_announcement(
        session=session, course_id=course_id, announcement_id=announcement_id)
    MARKER = '# Everything below is ignored.\n'
    editable_data = {
        'title': announcement['title'],
        'body': announcement['body'],
        'created': announcement['created'],
        'availability': announcement['availability'],
        'draft': announcement['draft']
    }
    announcement = json.dumps(editable_data, indent=2)
    new_data = click.edit(announcement + '\n\n' + MARKER)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_announcements().add_id(announcement_id).create()
    response = session.patch(url, data=new_data)
    response.raise_for_status()

    return response.text
