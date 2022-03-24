import json
from typing import Dict, Any
import requests
from datetime import date

def take_start_date(elem):
    return date.fromisoformat(elem['availability']['duration']['start'].split('T')[0])


def list_courses(cookies: Dict, user_name: str) -> Any:
    session = requests.Session()

    terms = session.get('https://ntnu.blackboard.com/learn/api/public/v1/terms', cookies=cookies)
    terms = json.loads(terms.text)['results']
    
    # Sort terms by start date to get the two most recent semesters to determine which courses to show
    for term in terms:
        if term['availability']['duration']['type'] != 'DateRange':
            terms.remove(term)
    terms.sort(key=take_start_date)

    term_1 = terms[len(terms) - 1]
    term_2 = terms[len(terms) - 2]

    course_memberships = session.get('https://ntnu.blackboard.com/learn/api/public/v1/users/userName:{}/courses'.format(user_name), cookies=cookies)
    course_memberships = json.loads(course_memberships.text)['results']

    course_list = []

    # Get courses from the correct terms
    for course in course_memberships:
        response = session.get('https://ntnu.blackboard.com/learn/api/public/v3/courses/{}'.format(course['courseId']), cookies=cookies, params={'fields': 'id, name, termId'})
        response = json.loads(response.text)
        if response['termId'] == term_1['id'] or response['termId'] == term_2['id']:
            course_list.append({
                'id': response['id'],
                'name': response['name']
            })
        else:
            break

    return course_list

def list_course(cookies: Dict, course_id:str) -> Any:
    response = requests.get('https://ntnu.blackboard.com/learn/api/public/v3/courses/{}'.format(course_id), cookies=cookies)
    return json.loads(response.text)

def list_favorite_courses(cookies: Dict, user_name: str) -> Any:
    return "Blackboard rest api do not have an option for this yet"
    # response = requests.get('https://ntnu.blackboard.com/learn/api/public/v1/users/userName:{}/courses'.format(user_name), cookies=cookies)
