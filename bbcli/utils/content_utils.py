import click
import webbrowser

from bbcli.services import contents_service
from bbcli.utils.utils import check_response, html_to_text
from bbcli.entities.Node import Node
from bbcli.utils.content_handler import content_handler
from bbcli.views import contents_view

def is_folder(node):
    key = 'contentHandler'
    return key in node and node[key]['id'] == content_handler['folder']

def get_children(ctx, course_id, worklist, folder_ids, node_ids):
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop(0)
        node_id = node.data['id']
        response = contents_service.get_children(
            ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            pass
        else:
            children = response.json()['results']
            for child in children:
                child_node = Node(child)
                node.add_child(child_node)
                if is_folder(child):
                    worklist.append(child_node)
                    folder_ids[child['title']] = child['id']
                else:
                    node_ids[child['title']] = child['id']

            return get_children(ctx, course_id, worklist, folder_ids, node_ids)


def get_folders(ctx, course_id, worklist, folder_ids, node_ids):
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop(0)
        node_id = node.data['id']
        response = contents_service.get_children(
            ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            pass
        else:
            children = response.json()['results']
            for child in children:
                if is_folder(child):
                    child_node = Node(child)
                    node.add_child(child_node)
                    worklist.append(child_node)
                    folder_ids[child['title']] = child['id']

            return get_folders(ctx, course_id, worklist, folder_ids, node_ids)


def get_content_type(ctx, course_id, worklist, folder_ids, node_ids, content_type):
    if len(worklist) == 0:
        return
    else:
        node = worklist.pop(0)
        node_id = node.data['id']
        response = contents_service.get_children(
            ctx.obj['SESSION'], course_id, node_id)
        if check_response(response) == False:
            pass
        else:
            children = response.json()['results']
            for child in children:
                if is_folder(child):
                    child_node = Node(child)
                    node.add_child(child_node)
                    worklist.append(child_node)
                    folder_ids[child['title']] = child['id']
                elif 'contentHandler' in child and content_handler[content_type] == child['contentHandler']['id']:
                    child_node = Node(child)
                    node.add_child(child_node)
                    node_ids[child['title']] = child['id']

            return get_content_type(
                ctx, course_id, worklist, folder_ids, node_ids, content_type)


def list_contents_thread(
        ctx,
        course_id,
        worklist,
        folder_ids,
        node_ids,
        root,
        folders: bool,
        content_type: str):
    if folders and content_type is not None:
        click.ClickException(
            'Cannot list contents and a specific folder type. Try either one.')
    elif folders and content_type is None:
        get_folders(ctx, course_id, worklist, folder_ids, node_ids)
    elif folders == False and content_type is not None:
        get_content_type(ctx, course_id, worklist, folder_ids, node_ids,  content_type)
    else:
        get_children(ctx, course_id, worklist, folder_ids, node_ids)

    root_node = root.preorder()
    return root_node


def check_content_handler(ctx, course_id: str, node_id: str):
    session = ctx.obj['SESSION']
    response = contents_service.get_content(
        ctx.obj['SESSION'], course_id, node_id)
    data = response.json()
    ch = data['contentHandler']['id']
    if ch == content_handler['document']:
        click.confirm(
            "This is a document with an attachment(s), do you want to download it?",
            abort=True)
        contents_service.download_attachments(session, course_id, node_id)
        # contents_view.open_vim(data)
    elif ch == content_handler['externallink']:
        link = data['contentHandler']['url']
        webbrowser.open(link)
    elif ch == content_handler['folder']:
        folder_ids = dict()
        folder_ids[data['title']] = data['id']
        root = Node(data)
        worklist = [root]
        get_children(ctx, course_id, worklist, folder_ids)
        root_node = root.preorder(root)
        contents_view.list_tree(folder_ids, root_node, only_folders=False)
    elif ch == content_handler['courselink']:
        print("tester ut courselink")
        key = 'targetId'
        if key in data['contentHandler']:
            target_id = data['contentHandler'][key]
            check_content_handler(ctx, course_id, target_id)
    elif ch == content_handler['file']:
        response = contents_service.get_attachments(
            session, course_id, node_id)
        attachments = response.json()['results']
        if len(attachments) > 0:
            click.confirm(
                "This is a file, do you want to download and open it?",
                abort=True)
        paths = contents_service.download_attachments(
            session, course_id, node_id, attachments)
        [contents_service.open_file(path) for path in paths]
    elif ch == content_handler['assignment']:
        str = data['title'] + '\n' + html_to_text(data['body'])
        contents_view.open_less_page(str)
        response = contents_service.get_attachments(
            session, course_id, node_id)
        attachments = response.json()['results']
        if len(attachments) > 0:
            click.confirm(
                "The assignment contains attachment(s), do you want to download?",
                abort=True)
            paths = contents_service.download_attachments(
                session, course_id, node_id, attachments)
            [contents_service.open_file(path) for path in paths]


image_files = ['jpeg', 'jpg', 'gif', 'svg', 'png', 'tiff', 'tif']
document_files = ['pdf', 'doc', 'docx', 'html', 'htm', 'xls', 'xlsx', 'txt']
video_files = ['mp4', 'avi', 'mov', 'flv', 'avchd']
presentation_files = ['ppt', 'pptx', 'odp', 'key']
audio_files = ['m4a', 'mp3', 'wav']


def get_file_type(fn):
    ft = ''
    ft = ['image_file' for imf in image_files if imf in fn]
    if len(ft) > 0:
        return ft[0]
    ft = ['document_file' for df in document_files if df in fn]
    if len(ft) > 0:
        return ft[0]
    ft = ['video_files' for vf in video_files if vf in fn]
    if len(ft) > 0:
        return ft[0]
    ft = ['presentation_files' for pf in presentation_files if pf in fn]
    if len(ft) > 0:
        return ft[0]
    ft = ['audio_files' for af in audio_files if af in fn]
    if len(ft) > 0:
        return ft[0]
    else:
        print("Could not find any of the files")
        # TODO: maybe throw something
        return
