import json
import os
from typing import Dict, List
import requests
import magic
from bbcli.utils.URL_builder import Builder, URL_builder
from bbcli.services.utils.content_builder import ContentBuilder
from bbcli.entities.content_builder_entitites import FileContent, GradingOptions, StandardOptions, FileOptions, WeblinkOptions
from bbcli.utils.utils import input_body
import click
import webbrowser
import markdown
import markdownify

from bbcli.utils.utils import get_download_path

url_builder = URL_builder()
content_builder = ContentBuilder()

# User gets a tree structure view of the courses content
# where each content is listed something like this: _030303_1 Lectures Folder
def list_contents(session: requests.Session, course_id: str) -> requests.models.Response:
    url = url_builder.base_v1().add_courses().add_id(course_id).add_contents().create()
    response = session.get(url)
    response.raise_for_status()
    return response

# get the children of a specific folder
def get_children(session: requests.Session, course_id: str, node_id: str) -> requests.models.Response:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).add_children().create()
    response = session.get(url)
    response.raise_for_status()
    return response

def get_content(session: requests.Session, course_id: str, node_id: str) -> requests.models.Response:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).create()
    response = session.get(url)
    response.raise_for_status()
    return response

def get_content_targe_tid(session: requests.Session, course_id: str, target_id: str) -> requests.models.Response:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(target_id).create()
    return session.get(url)

def get_attachments(session: requests.Session, course_id: str, node_id: str) -> requests.models.Response:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).add_attachments().create()
    response = session.get(url)
    response.raise_for_status()
    return response

def download_attachment(session: requests.Session, course_id: str, node_id: str, attachment, path) -> str:
    attachment_id = attachment['id']
    fn = attachment['fileName']
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(node_id).add_attachments(
        ).add_id(attachment_id).add_download().create()
    response = session.get(url, allow_redirects=True)
    response.raise_for_status()
    downloads_path = get_download_path(fn, path)
    try:
        f = open(downloads_path, 'wb')
        f.write(response.content)
        f.close()
    except FileNotFoundError:
        click.echo(f'\"{fn}\" could not be downloaded, please specify a valid path.')
        return 
    path = path if path != None else 'Downloads'
    click.echo(f'\"{fn}\" was downloaded to \"{path}\".')
    return downloads_path 

def download_attachments(session: requests.Session, course_id: str, node_id: str, attachments: List, path: str) -> List:
    paths = []
    for attachment in attachments:
        downloads_path = download_attachment(session, course_id, node_id, attachment, path)
        if downloads_path != None:
            paths.append(downloads_path)
    return paths

def open_file(path: str) -> None:
    webbrowser.open(r'file:'+path)

def upload_attachment(session: requests.Session, course_id: str, content_id: str, file_dst: str) -> Dict:
    uploaded_file = upload_file(session, file_dst)
    data = json.dumps(uploaded_file)

    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).add_attachments().create()
    response = session.post(url, data=data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response

def create_document(session: requests.Session, course_id: str, parent_id: str, title: str, 
                    standard_options: StandardOptions, attachments: tuple, is_markdown: bool) -> Dict:

    data_body = input_body()
    if is_markdown:
        data_body = markdown.markdown(data_body)

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
    response = json.loads(response.text)

    created_content_id = response['id']
    handle_attachments(session, course_id, created_content_id, attachments)

    return response

def create_file(session: requests.Session, course_id: str, parent_id: str, title: str, 
                file_dst: str, file_options: FileOptions, standard_options: StandardOptions) -> Dict:

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
    response = json.loads(response.text)
    return response


def create_externallink(session: requests.Session, course_id: str, parent_id: str, title: str, 
                        url: str, web_link_options: WeblinkOptions, standard_options: StandardOptions) -> Dict:

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
    response = json.loads(response.text)
    return response


def create_folder(session: requests.Session, course_id: str, parent_id: str,title: str, 
                is_bb_page: bool, standard_options: StandardOptions, is_markdown: bool) -> Dict:

    data_body = input_body()
    if is_markdown:
        data_body = markdown.markdown(data_body)

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
    response = json.loads(response.text)
    return response


def create_courselink(session: requests.Session, course_id: str, parent_id: str, title: str, 
                    target_id: str, standard_options: StandardOptions, is_markdown: bool) -> Dict:

    data_body = input_body()
    if is_markdown:
        data_body = markdown.markdown(data_body)

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
    response = json.loads(response.text)
    return response

def create_assignment(session: requests.Session, course_id: str, parent_id: str, title: str, 
                    standard_options: StandardOptions, grading_options: GradingOptions, 
                    attachments: tuple, is_markdown: bool) -> Dict:
    instructions = input_body()
    if is_markdown:
        instructions = markdown.markdown(instructions)

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
    response = json.loads(response.text)
    return response

def delete_content(session: requests.Session, course_id: str, content_id: str, delete_grades: bool) -> requests.models.Response:
    parameters = {
        'deleteGrades': delete_grades
    }
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).create()
    response = session.delete(url, params=parameters)
    response.raise_for_status()
    return response

def update_content(session: requests.Session, course_id: str, content_id: str, is_markdown: bool) -> Dict:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).create()
    content = session.get(url)
    content = json.loads(content.text)
    content_type = content['contentHandler']['id']

    validate_content_type(content_type)

    new_title = edit_title(content)

    data = update_content_data(content, is_markdown)
    data['title'] = new_title
    data = json.dumps(data)

    response = session.patch(url, data=data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response

def update_content_advanced(session: requests.Session, course_id: str, content_id: str, is_markdown: bool) -> Dict:
    url = url_builder.base_v1().add_courses().add_id(
        course_id).add_contents().add_id(content_id).create()
    content = session.get(url)
    content = json.loads(content.text)
    if 'body' in content and is_markdown:
        content['body'] = markdownify.markdownify(content['body'])

    if not is_editable_content_type(content['contentHandler']['id']):
        click.echo('This content type is not editable')
        raise click.Abort()
    if 'links' in content:
        del content['links']
    MARKER = '# Everything below is ignored.\n'
    editable_data = json.dumps(content, indent=2)
    data = click.edit(editable_data + '\n\n' + MARKER)
    new_data = data if data != None else editable_data
    if new_data is not None:
        new_data = new_data.split(MARKER, 1)[0].rstrip('\n')

    if 'body' in content and is_markdown:
        new_data = json.loads(new_data)
        new_data['body'] = markdown.markdown(new_data['body'])
        new_data = json.dumps(new_data, indent=2)

    response = session.patch(url, data=new_data)
    response.raise_for_status()
    response = json.loads(response.text)
    return response


"""

HELPER FUNCTIONS

"""


def upload_file(session: requests.Session, dst: str) -> Dict:

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


def generate_create_content_url(course_id: str, content_id: str) -> str:
    return url_builder\
        .base_v1()\
        .add_courses()\
        .add_id(course_id)\
        .add_contents()\
        .add_id(content_id)\
        .add_children()\
        .create()


def handle_attachments(session: requests.Session, course_id: str, content_id: str, attachments: tuple or None) -> None:
    if attachments:
        for attachment in attachments:
            upload_attachment(session, course_id, content_id, attachment)


def is_editable_content_type(content_type: str) -> bool:
    valid_content_types = ['resource/x-bb-assignment', 'resource/x-bb-externallink',
                           'resource/x-bb-courselink', 'resource/x-bb-file', 'resource/x-bb-document']
    for type in valid_content_types:
        if content_type == type:
            return True
    return False

def validate_content_type(content_type: str) -> None:
    if not is_editable_content_type(content_type):
        click.echo('This content type is not editable')
        raise click.Abort()

def update_default_content(content: Dict, is_markdown: bool=False) -> Dict:
    try:
        content['body']
    except KeyError:
        content['body'] = ''
    if is_markdown:
        content['body'] = markdownify.markdownify(content['body'])
    MARKER_BODY = '# Edit body. Everything below is ignored.\n'
    data = click.edit(content['body'] + '\n\n' + MARKER_BODY)
    new_data = data if data != None else content['body']
    if new_data is not None:
        new_data = new_data.split(MARKER_BODY, 1)[0].rstrip('\n')
    if is_markdown:
        new_data = markdown.markdown(new_data)
    return {'body': new_data}

def update_external_link_content(content: Dict) -> Dict:
    MARKER_URL = '# Edit URL. Everything below is ignored.\n'
    data = click.edit(content['contentHandler']['url'] + '\n\n' + MARKER_URL)
    new_data = data if data != None else content['contentHandler']['url']
    if new_data is not None:
        new_data = new_data.split(MARKER_URL, 1)[0].rstrip('\n')
    return {
        'contentHandler': {
            'id': 'resource/x-bb-externallink',
            'url': new_data
        }
    }

def edit_title(data: Dict) -> str:
    MARKER_TITLE = '# Edit title. Everything below is ignored.\n'
    title = click.edit(data['title'] + '\n\n' + MARKER_TITLE)
    new_title = title if title != None else data['title']
    if new_title is not None:
        new_title = new_title.split(MARKER_TITLE, 1)[0].rstrip('\n')
    return new_title

def update_file_content() -> None:
    return {}

def update_content_data(content: Dict, is_markdown: bool) -> Dict:
    content_type = content['contentHandler']['id']

    if content_type == 'resource/x-bb-assignment' or content_type == 'resource/x-bb-courselink' or content_type == 'resource/x-bb-document':
        data = update_default_content(content, is_markdown)
    elif content_type == 'resource/x-bb-externallink':
        data = update_external_link_content(content)
    elif content_type == 'resource/x-bb-file':
        data = update_file_content()
    return data