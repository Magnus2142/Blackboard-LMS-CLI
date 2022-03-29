from email.policy import default
import click
from bbcli.services import course_service
from bbcli.views import course_view
import os
import requests
from bbcli.utils.utils import set_cookies, set_headers


#, help='List a spesific course with the corresponding id'
@click.command(name='courses')
@click.argument('course_id', required=False)
@click.option('-a', '--all/--no-all', 'show_all', default=False, help='Lists all courses you have ever been signed up for')
def list_courses(course_id=None, show_all=False):

    """
    This command lists your courses, by default only the courses from
    two last semesters
    """

    bb_cookie = {
        'name':'BbRouter',
        'value': os.getenv("BB_ROUTER")
    }
    user_name = os.getenv('BB_USERNAME')

    session = requests.Session()
    set_cookies(session, [bb_cookie])

    response = None
    
    if course_id:
        response = course_service.list_course(session=session, course_id=course_id)
        course_view.print_course(response)
    else:
        if show_all:
            response = course_service.list_all_courses(session=session, user_name=user_name)
        else:
            response = course_service.list_courses(session=session, user_name=user_name)
        course_view.print_courses(response)

