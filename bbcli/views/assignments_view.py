import json
import click
from datetime import timezone
import dateutil.parser
from bbcli.utils.utils import print_keys_in_dict
from tabulate import tabulate


def print_created_assignment(response, print_json):
    if print_json:
        click.echo(json.dumps(response, indent=2))
    else:
        click.echo('\nAssignment successfully created: \n')
        print_keys_in_dict(response)


def print_assignments(assignments):
    click.echo('\n')
    table = {'id': [], 'title': [], 'due': []}
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
        table['id'].append(column_id)
        table['title'].append(name)
        table['due'].append(due)

    click.echo(tabulate(table, headers=['Id', 'Title', 'Due date']))
    click.echo('\n')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def print_submitted_attempts(attempts, print_json):
    if print_json:
        for attempt in attempts:
            if attempt['status'] == 'InProgress':
                attempts.remove(attempt)

        click.echo(json.dumps(attempts, indent=2))
    else:
        table = {'id': [], 'user_id': [], 'status': [], 'score': [], 'created': []}
        statuses = ['NeedsGrading', 'Completed']
        for attempt in attempts:
            for status in statuses:
                if (status == attempt['status']):
                    append_to_table(attempt, table)
                    continue

        click.echo(tabulate(table, headers=['Id', 'User Id', 'Status', 'Score', 'Created']))


def print_all_attempts(attempts, print_json):
    if print_json:
        click.echo(json.dumps(attempts, indent=2))
    else:
        table = {'id': [], 'user_id': [], 'status': [], 'score': [], 'created': []}
        for attempt in attempts:
            append_to_table(attempt, table)
        click.echo(tabulate(table, headers=['Id', 'User Id', 'Status', 'Score', 'Created']))


def append_to_table(attempt, table):
    table['id'].append(attempt['id'])
    table['user_id'].append(attempt['userId'])
    table['status'].append(attempt['status'])
    table['score'].append(
        attempt['score']) if 'score' in attempt else table['score'].append('N/A')
    created = utc_to_local(dateutil.parser.parse(attempt['created']))
    table['created'].append(created)

def print_get_attempt(attempt):
    print_keys_in_dict(attempt)

def print_submitted_attempt(attempt):
    click.echo('\nAssignment successfully submitted: \n')
    print_keys_in_dict(attempt)

def print_submitted_draft(attempt):
    click.echo('\nAssignment draft successfully submitted: \n')
    print_keys_in_dict(attempt)

def print_updated_attempt(attempt):
    click.echo('\nAttempt successfully updated: \n')
    print_keys_in_dict(attempt)

def print_graded_attempt(attempt):
    click.echo('\nAttempt successfully graded: \n')
    print_keys_in_dict(attempt)