import json
import click
from typing import Dict, List
from bbcli.utils.utils import html_to_text, print_keys_in_dict

def print_announcement(announcement: Dict) -> None:
    announcement_id = announcement['id']
    title = announcement['title']
    body = html_to_text(announcement['body'])
    created = announcement['created'].split('T')[0]

    click.echo('\n\n{:<15} {:<15}'.format('Id: ', announcement_id))
    click.echo('{:<15} {:<15}'.format('Title: ', title))
    click.echo('{:<15} {:<15}'.format('Date: ', created))
    click.echo('\n{:<15}\n'.format(body))

def print_announcements(announcements: List) -> None:
    announcements.reverse()
    for course in announcements:
        print_course_announcements(course['course_announcements'], course['course_name'])

def print_course_announcements(course_announcements: List, course_name: str = None) -> None:
    course_announcements = course_announcements['results']
    course_announcements.reverse()
    
    click.echo('\n')
    table = {'id': [], 'title': [], 'body': [], 'date': []}
    for announcement in course_announcements:
        if 'body' in announcement:

            announcement_id = announcement['id']
            title = announcement['title']
            body = html_to_text(announcement['body'])
            created = announcement['created'].split('T')[0]

            table['id'].append(announcement_id)
            table['title'].append(title)
            table['body'].append(body)
            table['date'].append(created)
            
            click.echo('----------------------------------------------------------------------\n')
            if course_name:
                click.echo(f'{course_name}\n')
            click.echo('{:<15} {:<15}'.format('Id: ', announcement_id))
            click.echo('{:<15} {:<15}'.format('Title: ', title))
            click.echo('{:<15} {:<15}'.format('Date: ', created))
            click.echo('\n{:<15}\n'.format(body))

def print_announcement_created(announcement: Dict) -> None:
    click.echo('\nAnnouncement sucessfully created:\n')
    print_keys_in_dict(announcement)

def print_announcement_deleted() -> None:
    click.echo('\nAnnouncement sucessfully deleted.\n')

def print_announcement_updated(announcement: Dict) -> None:
    click.echo('\nAnnouncement sucessfully updated:\n')
    print_keys_in_dict(announcement)