from datetime import timezone
import json
import click
import requests
import dateutil.parser
from bbcli.services.contents_service import upload_file
from bbcli.services.utils.attempt_builder import AttemptBuilder
from tabulate import tabulate

from bbcli.utils.URL_builder import URL_builder

url_builder = URL_builder()


def get_assignments(session: requests.Session, course_id):
    url = url_builder.base_v2().add_courses().add_id(
        course_id).add_gradebook().add_columns().create()
    response = session.get(url)
    response.raise_for_status()
    response = json.loads(response.text)
    results = response['results']
    print_assignments(results)

# TODO: This should be in view
def print_assignments(assignments):
    for i in range(len(assignments)):
        column_id = assignments[i]['id']
        name = assignments[i]['name']
        due = 'N/A'
        if 'grading' in assignments[i]:
            if 'due' in assignments[i]['grading']:
                due = assignments[i]['grading']['due']
                due_datetime = utc_to_local(dateutil.parser.parse(due))
                date = str(due_datetime.date())
                time = str(due_datetime.time())
                due = f'{date} {time}'

        click.echo('{:<12s}{:<40s} due {:<10s}'.format(column_id, name, due))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_column_attempts(session: requests.Session, course_id, column_id, print_submitted):
    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().create()

    response = session.get(url)
    response.raise_for_status()
    response = json.loads(response.text)
    results = response['results']

    if print_submitted:
        print_submitted_attempts(results)
    else:
        print_all_attempts(results)


def print_submitted_attempts(attempts):
    table = {'id': [], 'user id': [], 'status': [], 'score': [], 'created': []}
    statuses = ['NeedsGrading', 'Completed']
    for attempt in attempts:
        for status in statuses:
            if (status == attempt['status']):
                append_to_table(attempt, table)
                continue

    click.echo(tabulate(table, headers='keys'))


def print_all_attempts(attempts):
    table = {'id': [], 'user id': [], 'status': [], 'score': [], 'created': []}
    for attempt in attempts:
        append_to_table(attempt, table)
    click.echo(tabulate(table, headers='keys'))


def append_to_table(attempt, table):
    table['id'].append(attempt['id'])
    table['user id'].append(attempt['userId'])
    table['status'].append(attempt['status'])
    table['score'].append(
        attempt['score']) if 'score' in attempt else table['score'].append('N/A')
    created = utc_to_local(dateutil.parser.parse(attempt['created']))
    table['created'].append(created)


def get_column_attempt(session: requests.Session, course_id, column_id, attempt_id):
    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().add_id(attempt_id).create()

    response = session.get(url)
    attempt = json.loads(response.text)
    attempt = json.dumps(attempt, indent=2)
    click.echo(attempt)


def create_column_attempt(session: requests.Session, course_id, column_id, studentComments=None, studentSubmission=None, dst: str = None, status=None, draft: bool = False):
    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().create()

    if draft or dst is not None:
        status = 'InProgress'

    attempt = AttemptBuilder(studentComments=studentComments,
                             studentSubmission=studentSubmission,
                             status=status)
    data = attempt.create_json()
    json_data = json.dumps(data, indent=2)
    response = session.post(url, data=json_data)
    response_json = json.loads(response.text)
    click.echo(response_json)

    if dst is not None and response.status_code == 201:
        attempt_id = response_json['id']
        attach_file(session, course_id, attempt_id, dst)
        if draft:
            return
        update_column_attempt(session, course_id, column_id,
                              attempt_id, status='NeedsGrading')


def update_column_attempt(session: requests.Session, course_id, column_id, attempt_id, status=None, score=None, text=None, notes=None, feedback=None, studentComments=None, studentSubmission=None, exempt=None, dst=None):

    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().add_id(attempt_id).create()

    attempt = AttemptBuilder(status=status, score=score, text=text,
                             notes=notes, feedback=feedback, studentComments=studentComments, studentSubmission=studentSubmission, exempt=exempt)
    data = attempt.create_json()
    json_data = json.dumps(data, indent=2)

    response = session.patch(url, data=json_data)
    response.raise_for_status()
    response = json.loads(response.text)
    click.echo(response)

    if dst is not None:
        attach_file(session, course_id, attempt_id, dst)


def attach_file(session: requests.Session, course_id, attempt_id, dst: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_gradebook().add_attempts().add_id(attempt_id).add_files().create()

    uploaded_file = upload_file(session, dst)

    data = {'uploadId': uploaded_file['id']}
    data = json.dumps(data)
    response = session.post(url, data)

    response_json = json.loads(response.text)
    click.echo(response_json)
