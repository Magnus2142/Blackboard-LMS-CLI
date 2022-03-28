import click
from typing import List
from bbcli.utils.utils import html_to_text


def print_announcements(announcements: List):
    for course in announcements:
        print_course_announcements(course['course_announcements'], course['course_name'])

def print_course_announcements(course_announcements: List, course_name: str = None):
    
    for announcement in course_announcements:
        if 'body' in announcement:
            announcement_id = announcement['id']
            title = announcement['title']
            body = html_to_text(announcement['body'])
            created = announcement['created'].split('T')[0]

            click.echo('----------------------------------------------------------------------\n')
            if course_name:
                click.echo(f'{course_name}\n')
            click.echo('{:<15} {:<15}'.format('Id: ', announcement_id))
            click.echo('{:<15} {:<15}'.format('Title: ', title))
            click.echo('{:<15} {:<15}'.format('Date: ', created))
            click.echo('\n{:<15}\n'.format(body))
