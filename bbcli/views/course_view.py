import click

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