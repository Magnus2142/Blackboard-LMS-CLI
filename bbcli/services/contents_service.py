import json
import os
import requests
import magic
from bbcli.utils.URL_builder import URL_builder
from bbcli.services.utils.content_builder import ContentBuilder
from bbcli.entities.content_builder_entitites import FileContent, GradingOptions, StandardOptions, FileOptions, WeblinkOptions
from bbcli.utils.utils import input_body
import click
import urllib.request

from bbcli.utils.utils import check_response, get_download_path

url_builder = URL_builder()
content_builder = ContentBuilder()

# User gets a tree structure view of the courses content
# where each content is listed something like this: _030303_1 Lectures Folder
def list_contents(session: requests.Session, course_id):
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().create()
    response = session.get(url)
    if check_response(response) is False:
        return
    else:
        return response

# get the children of a specific folder


def get_children(session: requests.Session, course_id: str, node_id: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).add_children().create()
    return session.get(url)

# If it is a folder, list it like a tree structure view like mentioned above.
# If it is a document, download and open the document maybe?
# Find all types of content and have an appropriate response for them. This
# should maybe be handled in the view...


def get_content(session: requests.Session, course_id: str, node_id: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).create()
    print(url)
    return session.get(url)


def download_file(session: requests.Session, course_id: str, node_id: str):
    # https://ntnu.blackboard.com/learn/api/public/v1/courses/_27251_1/contents/_1685326_1
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).add_attachments()
    current = url.create()
    response = session.get(current)
    data = response.json()
    if check_response(response) == False:
        return
    else:
        id = data['results'][0]['id']
        file_name = data['results'][0]['fileName']
        url = url_builder.base_v1().add_courses().add_id(course_id).add_contents(
        ).add_id(node_id).add_attachments().add_id(id).add_download().create()
        response = session.get(url, allow_redirects=True)
        downloads_path = get_download_path(file_name)
        f = open(downloads_path, 'wb')
        f.write(response.content)
        f.close()
        click.echo("The file was downloaded to your downloads folder.")


def upload_attachment(session: requests.Session, course_id: str, content_id: str, file_dst: str):
    uploaded_file = upload_file(session, file_dst)
    data = json.dumps(uploaded_file)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).add_attachments().create()
    response = session.post(url, data=data)
    response.raise_for_status()


def create_document(session: requests.Session, course_id: str, parent_id: str, title: str, standard_options: StandardOptions = None, attachments: tuple = None):

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
    response.raise_for_status()

    created_content_id = json.loads(response.text)['id']
    handle_attachments(session, course_id, created_content_id, attachments)

    return response.text

# TODO: Bug that if a file is created with an attachment, the attachment takes the place of the actual file for the content. In addition,
#       if two attachments is added, only the last one is added/overwrite the first one


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
    response.raise_for_status()

    return response.text


def create_externallink(session: requests.Session, course_id: str, parent_id: str, title: str, url: str, web_link_options: WeblinkOptions, standard_options: StandardOptions):

    data = content_builder\
        .add_parent_id(parent_id)\
        .add_title(title)\
        .add_standard_options(standard_options)\
        .add_weblink_options(web_link_options)\
        .add_content_handler_externallink(url)\
        .create()

    data = json.dumps(data)
    url = generate_create_content_url(course_id, parent_id)
    response = session.post(url, data=data)
    response.raise_for_status()
    return response.text


def create_folder(session: requests.Session, course_id: str, parent_id: str, title: str, is_bb_page: bool, standard_options: StandardOptions):

    data_body = input_body()

    data = content_builder\
        .add_title(title)\
        .add_body(data_body)\
        .add_standard_options(standard_options)\
        .add_content_handler_folder(is_bb_page=is_bb_page)

    if parent_id:
        url = generate_create_content_url(course_id, parent_id)
        data.add_parent_id(parent_id)
    else:
        url = url_builder.base_v1().add_courses().add_id(
            course_id).add_contents().create()
    data = data.create()

    data = json.dumps(data)
    response = session.post(url, data=data)
    response.raise_for_status()
    return response.text


# TODO:FUNKER IKKE PGA targetType
def create_courselink(session: requests.Session, course_id: str, parent_id: str, title: str, target_id: str, standard_options: StandardOptions):

    data_body = input_body()

    data = content_builder\
        .add_title(title)\
        .add_body(data_body)\
        .add_standard_options(standard_options)\
        .add_content_handler_courselink(target_id=target_id)\
        .create()

    data = json.dumps(data)
    url = generate_create_content_url(course_id, parent_id)

    response = session.post(url, data=data)
    response.raise_for_status()
    return response.text

# TODO: Figure out how a lecturer can get/edit submission-, grading-, and display of grades options.


def create_assignment(session: requests.Session, course_id: str, parent_id: str, title: str, standard_options: StandardOptions, grading_options: GradingOptions, attachments: tuple = None):

    instructions = input_body()

    data = content_builder\
        .add_parent_id(parent_id)\
        .add_title(title)\
        .add_standard_options(standard_options)\
        .add_grading_options(grading_options)\
        .create()

    data.update({'instructions': instructions})

    if attachments:
        files = []
        for attachment in attachments:
            files.append(upload_file(session, attachment)['id'])
        data.update({'fileUploadIds': files})

    data = json.dumps(data)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_create_assignment().create()
    response = session.post(url, data=data)
    response.raise_for_status()
    return response.text


def delete_content(session: requests.Session, course_id: str, content_id: str, delete_grades: bool):

    parameters = {
        'deleteGrades': delete_grades
    }
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).create()
    response = session.delete(url, params=parameters)
    response.raise_for_status()
    return response.text


def update_content(session: requests.Session, course_id: str, content_id: str):
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).create()
    content = session.get(url)
    content = json.loads(content.text)
    if not is_editable_content_type(content['contentHandler']['id']):
        click.echo('This content type is not editable')
        raise click.Abort()
    if 'contentHandler' in content:
        del content['contentHandler']
    if 'links' in content:
        del content['links']
    MARKER = '# Everything below is ignored.\n'
    editable_data = json.dumps(content, indent=2)
    new_data = click.edit(editable_data + '\n\n' + MARKER)

    response = session.patch(url, data=new_data)
    response.raise_for_status()
    return response.text


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
    response.raise_for_status()
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


def handle_attachments(session: requests.Session, course_id: str, content_id: str, attachments: tuple or None):
    if attachments:
        for attachment in attachments:
            upload_attachment(session, course_id, content_id, attachment)


def is_editable_content_type(content_type: str):
    valid_content_types = ['resource/x-bb-assignment', 'resource/x-bb-externallink',
                           'resource/x-bb-courselink', 'resource/x-bb-file', 'resource/x-bb-document']
    for type in valid_content_types:
        if content_type == type:
            return True
    return False
