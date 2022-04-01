import base64
import json
import os
from subprocess import call
from tarfile import ENCODING
from typing import Dict, Any
import requests
from bbcli.services.courses_service import list_courses
from bbcli.utils.URL_builder import URLBuilder

from bbcli.utils.utils import check_response

url_builder = URLBuilder()

# User gets a tree structure view of the courses content
# where each content is listed something like this: _030303_1 Lectures Folder
def list_contents(session: requests.Session, course_id, folder_id):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().create()
    response = session.get(url)
    if check_response(response) is False:
        return
    else:
        return response

# get the children of a specific folder
def get_children(session: requests.Session, course_id: str, node_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().add_id(node_id).add_children().create()
    return session.get(url)

# If it is a folder, list it like a tree structure view like mentioned above.
# If it is a document, download and open the document maybe?
# Find all types of content and have an appropriate response for them. This
# should maybe be handled in the view...
def get_content(session: requests.Session, course_id: str, node_id: str):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().add_id(node_id).create()
    print(url)
    return session.get(url)

def get_file(session: requests.Session, course_id: str, node_id: str):
    # https://ntnu.blackboard.com/learn/api/public/v1/courses/_27251_1/contents/_1685326_1
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().add_id(node_id).add_attachments()
    current = url.create()
    response = session.get(current)
    data = response.json()
    if check_response(response) == False:
        return
    else:
        print("kommer her")
        id = data['results'][0]['id']
        # url = url.add_id(id).add_download().create()
        url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().add_id(node_id).add_attachments().add_id(id).add_download().create()
        print(url)
        response = session.get(url)
        print(response.headers)

    return response


# List all contents of type assignment, should be executed if a flag for example like --content-type assignment or smth is used
def list_assignments(cookies: Dict, course_id: str):
    print('Getting all assignments')

# TODO: add methods for all content types like the one above


# Create content. This should have a flag which says what kind of content type it is


# Create assignment. Creates an assignment

# Delete spesific content

# Update spesific content


def test_create_assignment(session: requests.Session, course_id: str, content_id: str):
    
    with open('/home/magnus/Downloads/3_meeting_notes.pdf', 'rb') as f:
        byte_content = f.read()

    base64_bytes = base64.b64encode(byte_content)
    base64_string = base64_bytes.decode(ENCODING)

    data = {
        "parentId": content_id,
        "title": "Test file",
        'body': 'jaja',
        "description": "string",
        "position": 0,
        "launchInNewWindow": True,
        "availability": {
            "available": "Yes",
            "allowGuests": True,
            "allowObservers": True,
            "adaptiveRelease": {
            "start": "2022-03-29T09:32:35.571Z",
            }
        },
        "contentHandler": {
            'id':'resource/x-bb-file',
            'file': base64_string
        },
    }
    data = json.dumps(data)
    session.headers.update({'Content-Type': 'application/json'})
    # files = {
    #     'pdf_document': open('/home/magnus/Downloads/3_meeting_notes.pdf', 'rb')
    # }

    

    # Returns the string: domain +  /learn/api/public/v1/courses/{courseId}/contents/{contentId}/children
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().add_id(content_id).add_children().create()

    response = session.post(url, data=data)
    print(response.text)

    