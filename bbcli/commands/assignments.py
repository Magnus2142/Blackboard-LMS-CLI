import click
from bbcli.commands.contents import grading_options, set_dates, standard_options
from bbcli.entities.content_builder_entitites import GradingOptions, StandardOptions
from bbcli.services import assignment_service, contents_service
from bbcli.utils.error_handler import exception_handler
from bbcli.utils.utils import format_date


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
@click.command(name='create')
@click.argument('course_id', required=True, type=str)
@click.argument('parent_id', required=True, type=str)
@click.argument('title', required=True, type=str)
@click.argument('attachments', required=False, nargs=-1, type=click.Path())
@standard_options
@grading_options
@click.pass_context
@exception_handler
def create_assignment(ctx, course_id: str, parent_id: str, title: str,
                      hide_content: bool, reviewable: bool,
                      start_date: str, end_date: str,
                      due_date: str, max_attempts: int, unlimited_attempts: bool, score: int,
                      attachments: tuple):
    """
    Create an assignment.
    """
    standard_options = StandardOptions(hide_content, reviewable)
    grading_options = GradingOptions(
        attempts_allowed=max_attempts, is_unlimited_attemps_allowed=unlimited_attempts, score_possible=score)

    set_dates(standard_options, start_date, end_date)
    grading_options.due = format_date(due_date)

    response = contents_service.create_assignment(
        ctx.obj['SESSION'], course_id, parent_id, title, standard_options, grading_options, attachments)
    click.echo(response)


@click.command(name='list')
@click.argument('course-id', required=True)
@click.pass_context
def get_assignments(ctx, course_id):
    """
    List assignments for a course.
    """
    assignment_service.get_assignments(ctx.obj['SESSION'], course_id)


@click.command(name='list')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.option('--submitted', is_flag=True, help='List only submitted attempts.')
@click.pass_context
def get_attempts(ctx, course_id, column_id, submitted):
    """
    List attempts for an assignment.
    """
    assignment_service.get_column_attempts(
        ctx.obj['SESSION'], course_id, column_id, print_submitted=submitted)


# TODO: Retrieve the submission w/ attachments.
@click.command(name='get')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.argument('attempt_id', required=True)
@click.pass_context
def get_attempt(ctx, course_id, column_id, attempt_id):
    """
    Get a specific attempt for an assignment.
    """
    assignment_service.get_column_attempt(
        ctx.obj['SESSION'], course_id, column_id, attempt_id)


@click.command(name='submit')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.option('--studentComments', help='The student comments associated with this attempt.')
@click.option('--studentSubmission', help='The student submission text associated with this attempt.')
@click.option('--file', help='Attach a file to an attempt for a Student Submission. Relative path of file.')
@click.option('--draft', is_flag=True)
@click.pass_context
def submit_attempt(ctx, course_id, column_id, studentComments, studentSubmission, file, draft):
    """
    Submit assignment attempt.
    """
    assignment_service.create_column_attempt(
        ctx.obj['SESSION'], course_id, column_id, studentComments=studentComments, studentSubmission=studentSubmission, dst=file, status='needsGrading', draft=draft)


@click.command(name='submit-draft')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.argument('attempt_id', required=True)
@click.pass_context
def submit_draft(ctx, course_id, column_id, attempt_id):
    """
    Submit assignment draft.
    """
    assignment_service.update_column_attempt(
        ctx.obj['SESSION'], course_id=course_id, column_id=column_id, attempt_id=attempt_id, status='needsGrading')


@click.command(name='update')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.argument('attempt_id', required=True)
@attempt_options
@click.option('--studentComments', help='The student comments associated with this attempt.')
@click.option('--studentSubmission', help='The student submission text associated with this attempt.')
@click.pass_context
def update_attempt(ctx, course_id, column_id, attempt_id, status, comments, submission, file):
    """
    Update assignment.
    """
    assignment_service.update_column_attempt(
        session=ctx.obj['SESSION'], course_id=course_id, column_id=column_id, attempt_id=attempt_id, status=status, studentComments=comments, studentSubmission=submission, dst=file)


@click.command(name='grade')
@click.argument('course_id', required=True)
@click.argument('column_id', required=True)
@click.argument('attempt_id', required=True)
@attempt_options
@click.pass_context
def grade_assignment(ctx, course_id, column_id, attempt_id, status, score, text, notes, feedback, exempt):
    """
    Grade assignment.
    """
    if status is None:
        status = 'Completed'

    assignment_service.update_column_attempt(session=ctx.obj['SESSION'], status=status, course_id=course_id, column_id=column_id,
                                             attempt_id=attempt_id, score=score, text=text, notes=notes, feedback=feedback, exempt=exempt)
