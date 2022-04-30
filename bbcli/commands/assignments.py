import json
import click
from markdown import markdown
from bbcli.commands.contents import grading_options, set_dates, standard_options
from bbcli.entities.content_builder_entitites import GradingOptions, StandardOptions
from bbcli.services import assignments_services, contents_services
from bbcli.utils.error_handler import create_exception_handler, list_exception_handler, update_exception_handler
from bbcli.utils.utils import format_date
from bbcli.views import assignments_views


def attempt_options(function):
    function = click.option(
        '--status', default='Completed', help='The status of this attempt.', show_default=True)(function)
    function = click.option(
        '--text', help='The text grade associated with this attempt.')(function)
    function = click.option(
        '--score', type=int, help='The score associated with this attempt.')(function)
    function = click.option(
        '--notes', help='The instructor notes associated with this attempt.')(function)
    function = click.option(
        '--feedback', help='The instructor feedback associated with this attempt.')(function)
    function = click.option('--exempt', is_flag=True,
                            help='Whether the score associated with this attempt is ignored when computing the user\'s grade for the associated grade column.')(function)
    return function


# TODO: This function is a copy of the same function in contents.py. Fix this.
@click.command(name='create', help='Create an assignment.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course you want to create an assignment in.')
@click.option('-f', '--folder', 'parent_id', required=True, type=str, help='FOLDER ID, of the folder you want to place the assignment.')
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.option('-md', '--markdown', required=False, is_flag=True, help='Use this flag if you want to use markdown in body')
@standard_options
@grading_options
@click.pass_context
@create_exception_handler
def create_assignment(ctx, course_id: str, parent_id: str, title: str,
                      hide_content: bool, reviewable: bool,
                      start_date: str, end_date: str,
                      due_date: str, max_attempts: int, unlimited_attempts: bool, score: int,
                      attachments: tuple, print_json: bool, markdown: bool):
    standard_options = StandardOptions(hide_content, reviewable)
    grading_options = GradingOptions(
        attempts_allowed=max_attempts, is_unlimited_attemps_allowed=unlimited_attempts, score_possible=score)

    set_dates(standard_options, start_date, end_date)
    grading_options.due = format_date(due_date)

    response = contents_services.create_assignment(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, grading_options, attachments, markdown)
    assignments_views.print_created_assignment(json.loads(response), print_json)

@click.command(name='list', help='List all assignments from a course.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course you want assignments from.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@list_exception_handler
def get_assignments(ctx, course_id, print_json):
    response = assignments_services.get_assignments(ctx.obj['SESSION'], course_id)
    if print_json:
        click.echo(json.dumps(response, indent=2))
    else:
        assignments_views.print_assignments(response)

@click.command(name='list', help='List attempts for an assignment.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course you want the assignment attempts from')
@click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want attempts from')
@click.option('--submitted', is_flag=True, help='List only submitted attempts.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@list_exception_handler
def get_attempts(ctx, course_id, column_id, submitted, print_json):
    response = assignments_services.get_column_attempts(ctx.obj['SESSION'], course_id, column_id)
    if submitted:
        assignments_views.print_submitted_attempts(response, print_json)
    else:
        assignments_views.print_all_attempts(response, print_json)


# TODO: Retrieve the submission w/ attachments.
@click.command(name='get', help='Get a specific attempt for an assignment.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course of you want to get attempt from')
@click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want attempts from')
@click.option('-at', '--attempt', 'attempt_id', required=True, help='ATTEMPT ID, of the attempt you want to fetch.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@list_exception_handler
def get_attempt(ctx, course_id, column_id, attempt_id, print_json):
    response = assignments_services.get_column_attempt(ctx.obj['SESSION'], course_id, column_id, attempt_id)
    if print_json:
        click.echo(response)
    else:
        assignments_views.print_get_attempt(json.loads(response))

@click.command(name='submit', help='Submit assignment attempt.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course to submit an assignment to.')
@click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want to submit to.')
@click.option('--student-comments', help='The student comments associated with this attempt.')
@click.option('--student-submission', help='The student submission text associated with this attempt.')
@click.option('--file', type=click.Path(exists=True), help='Attach a file to an attempt for a Student Submission. Relative path of file.')
@click.option('--draft', is_flag=True)
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@create_exception_handler
def submit_attempt(ctx, course_id, column_id, student_comments, student_submission, file, draft, print_json):
    response = assignments_services.create_column_attempt(
        ctx.obj['SESSION'], course_id, column_id, studentComments=student_comments, studentSubmission=student_submission, dst=file, status='needsGrading', draft=draft)
    if print_json:
        click.echo(response)
    else:
        assignments_views.print_submitted_attempt(json.loads(response))

@click.command(name='submit-draft', help='Submit assignment draft.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course where the assignment is.')
@click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want to submit to.')
@click.option('-at', '--attempt', 'attempt_id', required=True, help='ATTEMPT ID, of the attempt you want to update.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@click.pass_context
@update_exception_handler
def submit_draft(ctx, course_id, column_id, attempt_id, print_json):
    response = assignments_services.update_column_attempt(
        ctx.obj['SESSION'], course_id=course_id, column_id=column_id, attempt_id=attempt_id, status='needsGrading')
    if print_json:
        click.echo(response)
    else:
        assignments_views.print_submitted_draft(json.loads(response))

# @click.command(name='update', help='Update assignment.')
# @click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course where the assignment is.')
# @click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want to submit to.')
# @click.option('-at', '--attempt', 'attempt_id', required=True, help='ATTEMPT ID, of the attempt you want to update.')
# @attempt_options
# @click.option('--student-comments', help='The student comments associated with this attempt.')
# @click.option('--student-submission', help='The student submission text associated with this attempt.')
# @click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
# @click.pass_context
# @update_exception_handler
# def update_attempt(ctx, course_id, column_id, attempt_id, status, student_comments, student_submission, file, print_json, exempt, feedback, notes, score, text, file):
#     response = assignment_service.update_column_attempt(
#         session=ctx.obj['SESSION'], course_id=course_id, column_id=column_id, attempt_id=attempt_id, status=status, studentComments=student_comments, studentSubmission=student_submission, dst=file)
#     if print_json:
#         click.echo(response)
#     else:
#         assignments_view.print_updated_attempt(json.loads(response))

@click.command(name='grade', help='Grade an assignment.')
@click.option('-c', '--course', 'course_id', required=True, help='COURSE ID, of the course where the assignment is.')
@click.option('-a', '--assignment', 'column_id', required=True, help='ASSIGNMENT ID, of the assignment you want.')
@click.option('-at', '--attempt', 'attempt_id', required=True, help='ATTEMPT ID, of the attempt you want to grade.')
@click.option('-j', '--json', 'print_json', required=False, is_flag=True, help='Print the data in json format')
@attempt_options
@click.pass_context
@update_exception_handler
def grade_assignment(ctx, course_id, column_id, attempt_id, status, score, text, notes, feedback, exempt, print_json):
    if status is None:
        status = 'Completed'

    response = assignments_services.update_column_attempt(session=ctx.obj['SESSION'], status=status, course_id=course_id, column_id=column_id,
                                             attempt_id=attempt_id, score=score, text=text, notes=notes, feedback=feedback, exempt=exempt)
    if print_json:
        click.echo(response)
    else:
        assignments_views.print_graded_attempt(json.loads(response))