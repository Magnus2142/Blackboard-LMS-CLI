from datetime import timezone
import json
import click
import requests
import dateutil.parser

from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()


def get_assignments(session: requests.Session, course_id):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_gradebook().add_columns().create()
    response = session.get(url)
    response = json.loads(response.text)
    results = response['results']
    print_assignments(results)


def print_assignments(assignments):
    for i in range(len(assignments)):
        name = assignments[i]['name']
        due = 'N/A'
        if ('grading' in assignments[i]):
            if ('due' in assignments[i]['grading']):
                due = assignments[i]['grading']['due']
                due_datetime = utc_to_local(dateutil.parser.parse(due))
                date = str(due_datetime.date())
                time = str(due_datetime.time())
                due = f'{date} {time}'

        click.echo('{:<40s} due {:<10s}'.format(name, due))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
