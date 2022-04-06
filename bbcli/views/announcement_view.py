import click
from typing import List
from bbcli.utils.utils import html_to_text


def print_announcements(announcements: List):
    announcements.reverse()
    for course in announcements:
        print_course_announcements(course['course_announcements'], course['course_name'])

def print_course_announcements(course_announcements: List, course_name: str = None):
    course_announcements.reverse()
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

def print_announcement_created(announcement):
    click.echo('\nAnnouncement sucessfully created:\n\n' + announcement)


def print_announcement_deleted():
    click.echo('\nAnnouncement sucessfully deleted.\n')

def print_announcement_updated(announcement):
    click.echo('\nAnnouncement sucessfully updated:\n\n' + announcement)
