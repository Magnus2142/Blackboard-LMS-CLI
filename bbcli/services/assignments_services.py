from datetime import timezone
import json
import click
import requests
import dateutil.parser
from bbcli.services.contents_services import upload_file
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
    return results




def get_column_attempts(session: requests.Session, course_id, column_id):
    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().create()

    response = session.get(url)
    response.raise_for_status()
    response = json.loads(response.text)
    results = response['results']
    return results

def get_column_attempt(session: requests.Session, course_id, column_id, attempt_id):
    url = url_builder.base_v2().add_courses().add_id(course_id).add_gradebook(
    ).add_columns().add_id(column_id).add_attempts().add_id(attempt_id).create()

    response = session.get(url)
    attempt = json.loads(response.text)
    attempt = json.dumps(attempt, indent=2)
    return attempt


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
    response.raise_for_status()
    response_json = json.loads(response.text)

    if dst is not None and response.status_code == 201:
        attempt_id = response_json['id']
        attach_file(session, course_id, attempt_id, dst)
        if draft:
            return
        update_column_attempt(session, course_id, column_id,
                              attempt_id, status='NeedsGrading')
    
    print(response_json)
    return json.dumps(response_json, indent=2)


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

    if dst is not None:
        attach_file(session, course_id, attempt_id, dst)

    return json.dumps(response, indent=2)

def attach_file(session: requests.Session, course_id, attempt_id, dst: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_gradebook().add_attempts().add_id(attempt_id).add_files().create()

    uploaded_file = upload_file(session, dst)

    data = {'uploadId': uploaded_file['id']}
    data = json.dumps(data)
    response = session.post(url, data)

    response_json = json.loads(response.text)
    click.echo(response_json)
