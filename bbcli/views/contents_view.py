import json
from anytree import Node as Nd, RenderTree
from colorama import Fore, Style
from bbcli.utils.utils import html_to_text, print_keys_in_dict
import click
import tempfile, os
from subprocess import call

def list_tree(root, folder_ids, node_ids):
    # color = Fore.RESET if only_folders else Fore.BLUE
    color = Fore.BLUE
    for pre, fill, node in RenderTree(root):
        node_id = node.name.split()[0]
        if node_id in folder_ids:
            click.echo(f'{pre}{color} {node.name} {Style.RESET_ALL}')
        elif node_id in node_ids:
            click.echo(f'{pre} {node.name}')
        else:
            click.echo('Neither node nor folder.')


        

def open_vim(data):
    str = data['title'] + '\n'
    str += html_to_text(data['body'])

    EDITOR = os.environ.get('EDITOR','vim') 

    initial_message = bytearray(str, encoding='utf8')

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        call([EDITOR, tf.name])

        # do the parsing with `tf` using regular File operations.
        # for instance:
        # tf.seek(0)
        # edited_message = tf.read()
        # print (edited_message.decode("utf-8"))

def open_less_page(str):
    import pydoc
    pydoc.pager(str)


def print_created_attachment_response(response, print_json):
    if print_json:
        click.echo(json.dumps(response, indent=2))
    else:
        click.echo('\nAttachment successfully uploaded: \n')
        print_keys_in_dict(response)

def print_created_content_response(response, print_json):
    if print_json:
        click.echo(json.dumps(response, indent=2))
    else:
        click.echo('\nContent successfully created: \n')
        print_keys_in_dict(response)

def print_deleted_content_response():
    click.echo('\nContent successfully deleted.\n')

def print_updated_content_response(response, print_json):
    if print_json:
        click.echo(json.dumps(response, indent=2))
    else:
        click.echo('\nContent successfully updated: \n')
        print_keys_in_dict(response)