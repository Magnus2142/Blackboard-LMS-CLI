import json
from subprocess import call
from typing import Dict, Any
import requests
from bbcli.services.course_service import list_courses
import click


# User gets a tree structure view of the courses content
# where each content is listed something like this: _030303_1 Lectures Folder
def list_course_content(cookies: Dict, course_id: str):
    print('Getting course content!')


# If it is a folder, list it like a tree structure view like mentioned above.
# If it is a document, download and open the document maybe?
# Find all types of content and have an appropriate response for them. This
# should maybe be handled in the view...
def get_content(cookies: Dict, course_id: str, content_id: str):
    print('Getting content by its ID.')


# List all contents of type assignment, should be executed if a flag for example like --content-type assignment or smth is used
def list_assignments(cookies: Dict, course_id: str):
    print('Getting all assignments')

# TODO: add methods for all content types like the one above


# Create content. This should have a flag which says what kind of content type it is


# Create assignment. Creates an assignment

# Delete spesific content

# Update spesific content