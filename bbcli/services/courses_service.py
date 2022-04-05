import json
from typing import Dict, Any, List
import requests
from datetime import date

from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()


def list_courses(session: requests.Session, user_name: str) -> Any:

    terms = get_terms(session)
    sort_terms(terms)

    term_1 = terms[len(terms) - 1]
    term_2 = terms[len(terms) - 2]

    course_memberships = get_course_memberships(session, user_name)

    course_list = []

    # Get courses from the correct terms
    for course in course_memberships:
        url = url_builder.base_v3().add_courses().add_id(
            course['courseId']).create()
        response = session.get(url, params={'fields': 'id, name, termId'})
        response.raise_for_status()
        response = json.loads(response.text)
        if response['termId'] == term_1['id'] or response['termId'] == term_2['id']:
            course_list.append({
                'id': response['id'],
                'name': response['name']
            })
        else:
            break

    return course_list


def list_all_courses(session: requests.Session, user_name: str) -> Any:
    course_memberships = get_course_memberships(session, user_name)

    course_list = []

    for course in course_memberships:
        url = url_builder.base_v3().add_courses().add_id(
            course['courseId']).create()
        response = session.get(url, params={'fields': 'id, name'})
        response.raise_for_status()
        response = json.loads(response.text)
        course_list.append(response)

    return course_list


def list_course(session: requests.Session, course_id: str) -> Any:
    url = url_builder.base_v3().add_courses().add_id(course_id).create()
    response = session.get(url)
    response.raise_for_status()

    return json.loads(response.text)


"""

HELPER FUNCTIONS

"""


def take_start_date(elem):
    return date.fromisoformat(elem['availability']['duration']['start'].split('T')[0])


def get_terms(session: requests.Session):
    url = url_builder.base_v1().add_terms().create()
    terms = session.get(url)
    terms.raise_for_status()
    terms = json.loads(terms.text)['results']
    return terms


def sort_terms(terms):
    # Sort terms by start date to get the two most recent semesters to determine which courses to show
    for term in terms:
        if term['availability']['duration']['type'] != 'DateRange':
            terms.remove(term)
    terms.sort(key=take_start_date)


def get_course_memberships(session: requests.Session, user_name: str):
    url = url_builder.base_v1().add_users().add_id(
        id=user_name, id_type='userName').add_courses().create()
    course_memberships = session.get(url)
    course_memberships.raise_for_status()
    course_memberships = json.loads(course_memberships.text)['results']
    return course_memberships
