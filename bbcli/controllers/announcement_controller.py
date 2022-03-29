from email.policy import default
import click
from bbcli.services import announcement_service
from bbcli.views import announcement_view
import os
import requests

from bbcli.utils.utils import set_cookies, set_headers

@click.command(name='announcements')
@click.argument('course_id', required=False)
@click.argument('announcement_id', required=False)
def list_announcements(course_id=None, announcement_id=None):

    """
    This command lists your announcements.
    Either all announcements, all announcements from a spesific course, or one announcement.
    """

    bb_cookie = {
        'name':'BbRouter',
        'value': os.getenv("BB_ROUTER")
    }
    xsrf = {'X-Blackboard-XSRF': os.getenv('XSRF')}
    user_name = os.getenv('BB_USERNAME')

    session = requests.Session()
    set_cookies(session, [bb_cookie])
    set_headers(session, [xsrf])

    response = None
    
    if announcement_id:
        response = announcement_service.list_announcement(session, course_id, announcement_id)
        announcement_view.print_course_announcements([response])
    elif course_id:
        response = announcement_service.list_course_announcements(session, course_id)
        announcement_view.print_course_announcements(response)
    else:
        response = announcement_service.list_announcements(session, user_name)
        announcement_view.print_announcements(response)
