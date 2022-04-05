from email.policy import default
import click

from bbcli.services import assignment_service


@click.command(name='get')
@click.argument('course_id', required=True)
@click.pass_context
def get_assignments(ctx, course_id):
    """
    Get assignments
    """
    assignment_service.get_assignments(ctx.obj['SESSION'], course_id)
