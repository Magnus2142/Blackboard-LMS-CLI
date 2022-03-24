import json
from typing import Dict, Any
import requests


# TODO: use /term endpoint to determine whether the course is an active term
def list_courses(cookies: Dict, user_name: str) -> Any:
    response = requests.get('https://ntnu.blackboard.com/learn/api/public/v1/users/userName:{}/courses'.format(user_name), cookies=cookies)
    courses = json.loads(response.text)['results']
    detailed_course_list = []
    for course in courses:
        detailed_course = list_course(cookies=cookies, course_id=course['courseId'])
        detailed_course_list.append(detailed_course)

    return detailed_course_list

def list_course(cookies: Dict, course_id:str) -> Any:
    response = requests.get('https://ntnu.blackboard.com/learn/api/public/v3/courses/{}'.format(course_id), cookies=cookies)
    return json.loads(response.text)

def list_favorite_courses(cookies: Dict, user_name: str) -> Any:
    return "Blackboard rest api do not have an option for this yet"
    # response = requests.get('https://ntnu.blackboard.com/learn/api/public/v1/users/userName:{}/courses'.format(user_name), cookies=cookies)
