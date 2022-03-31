import base64
from datetime import date
import json
import os
from subprocess import call
from tarfile import ENCODING
from typing import Dict, Any, List
import requests
import magic
from bbcli.services.courses_service import list_courses
from bbcli.utils.URL_builder import URLBuilder
from bbcli.services.utils.content_builder import ContentBuilder
from bbcli.entities.content_builder_entitites import DateInterval, FileContent, StandardOptions, FileOptions, WeblinkOptions
from bbcli.utils.utils import input_body

url_builder = URLBuilder()
content_builder = ContentBuilder()

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

# NB: Alle options sende som values i enkle fields i bodyen

# Alle disse blir sendt til post content endpoint. title, body er samme. Options varirerer. Største ulikheten
# er i content-handler. None kan også ha attachments.

# Tror svaret er en ContentBuilder

# Hvis dato er inkludert for visning av content etter en spesifikk tid osv. oppdater ny regel ellr hva det nå er
# Kilde: https://docs.blackboard.com/rest-apis/learn/getting-started/adaptive-release. KANSKJE IKKE NØDVENDIG

# Title, body, eventuelt attachements?, Standard Options: permit users to view, track number of views, date (start, end)
def create_document(session:requests.Session, course_id: str, parent_id: str, title: str, standard_options: StandardOptions=None, attachments: List[str]=None):
    
    data_body = input_body()
    data = content_builder\
        .add_parent_id(parent_id)\
        .add_title(title)\
        .add_body(data_body)\
        .add_standard_options(standard_options)\
        .add_content_handler_document()\
        .create()
    
    data = json.dumps(data)
    url = generate_create_content_url(course_id, parent_id)
    response = session.post(url, data=data)
    return response.text


# Title, file itself, FIle Options: open in new window, add alignment to content, Standard Options: as above

def create_file(session: requests.Session, course_id: str, parent_id: str, title: str, file_dst: str, file_options: FileOptions, standard_options: StandardOptions):

    uploaded_file = upload_file(session, file_dst)
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_dst)

    with open(file_dst, 'rb') as f:
        file_name = os.path.basename(f.name)

    file_content = FileContent(uploaded_file['id'], file_name, mime_type)

    data = content_builder\
        .add_parent_id(parent_id)\
        .add_title(title)\
        .add_standard_options(standard_options)\
        .add_file_options(file_options)\
        .add_content_handler_file(file_content)\
        .create()
    
    data = json.dumps(data)
    url = generate_create_content_url(course_id, parent_id)
    response = session.post(url, data=data)
    return response.text

# Title, URL, body, eventuelt attachments?, Weblink options: open in new window?, Standard options: as above


def create_externallink():
    pass

# Title, body, Standard options: as above


def create_folder():
    pass

# Title, body, location(?), targetId content, Standard Options: as above


def create_courselink():
    pass

# Se egen metode i BBL REST API


def create_assignment():
    pass

# Vet ikke enda


def create_forumlink():
    pass

# Vet ikke enda


def create_blti_link():
    pass


# TODO: Check how to publish audio and image, it doesn't have a content handler
# SOLUTION: See the upload files section. There it says something about uploading images and audio and videoetc,
# SOLUTION 2: THIS IS EMBEDDED IN THE BODY I BELIEVE

# TODO: Module page has it own 'resource/x-bb-module-page' content typ, but is not mentioned in the documentation
# Do reserach on this later

# TODO: Same as the one above, just with blank page 'resource/x-bb-blankpage', Both are under new page option in the
# bb web interface


# TODO: 'x-bb-lesson'


# TODO: CReat an own method for attachments posting for either being
# called straight after a content of type file, document, or assignment is created.
# OR afterwards



"""

HELPER FUNCTIONS

"""

def upload_file(session: requests.Session, dst: str):
    
    del session.headers['Content-Type']
    with open(dst, 'rb') as f:
        file_name = os.path.basename(f.name)
        files = {file_name: f.read()}

    url = url_builder.base_v1().add_uploads().create()
    response = session.post(url, files=files)
    session.headers.update({
        'Content-Type': 'application/json'
    })
    file = json.loads(response.text)
    return file

def generate_create_content_url(course_id: str, content_id: str):
    return url_builder\
        .base_v1()\
        .add_courses()\
        .add_id(course_id)\
        .add_contents()\
        .add_id(content_id)\
        .add_children()\
        .create()