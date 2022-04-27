import json
import click
from tabulate import tabulate

def print_courses(courses, print_json):
    if print_json:
        click.echo(json.dumps(courses, indent=2))
    else:
        click.echo('\n')
        table = {'id': [], 'course_name': []}
        for course in courses:
            table['id'].append(course['id'])
            table['course_name'].append(course['name'])

        click.echo(tabulate(table, headers=['Id', 'Course Name']))
        click.echo('\n')

def print_course(course, print_json):
    if print_json:
        click.echo(json.dumps(course, indent=2))
    else:
        primary_id = course['id']
        course_id = course['courseId']
        name = course['name']

        click.echo('\n{:<12} {:<12}'.format('Id:', primary_id))
        click.echo('{:<12} {:<12}'.format('Course Id:', course_id))
        click.echo('{:<12} {:<12}\n'.format('Name:', name))