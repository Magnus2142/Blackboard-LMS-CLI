import json
import click
import csv
import time
from pathlib import Path

def print_courses(courses):
    click.echo('\n{:<12} {:<5}\n'.format('Id', 'Course Name'))
    for course in courses:
        course_id = course['id']
        name = course['name']
        click.echo('{:<12} {:<5}'.format(course_id, name))
    click.echo('\n\n')

def print_course(course):

    primary_id = course['id']
    course_id = course['courseId']
    name = course['name']

    click.echo('\n{:<12} {:<12}'.format('Id:', primary_id))
    click.echo('{:<12} {:<12}'.format('Course Id:', course_id))
    click.echo('{:<12} {:<12}\n'.format('Name:', name))

def print_course_users(users, print_json=False):
    if print_json:
        click.echo(f'\n{json.dumps(users, indent=2)}\n\n')
    else:
        click.echo('\n{:<12} {:<5}\n'.format('Id', 'Username'))
        for user in users:
            user_id = user['id']
            name = user['userName']
            click.echo('{:<12} {:<5}'.format(user_id, name))
        click.echo('\n\n')

def save_data_to_csv(users):
    keys = users[0].keys()

    downloads_path = str(Path.home() / 'Downloads')
    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
    path = f'{downloads_path}/course_users_{moment}.csv'
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(users)
    click.echo('\nSuccessfully exported users from the course to a csv in path: ' + path + '\n')