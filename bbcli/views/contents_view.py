from anytree import Node as Nd, RenderTree
from colorama import Fore, Style
from bbcli.utils.utils import html_to_text
import click
import sys, tempfile, os
from subprocess import call



def list_tree(colors, root, only_folders = False):
    color = Fore.RESET if only_folders else Fore.BLUE
    for pre, fill, node in RenderTree(root):
        if not node.children and only_folders == False:
            click.echo("%s%s" % (pre, node.name))
        else:
            folder_id = colors[node.name]
            click.echo(f'{pre}{color}{folder_id} {node.name} {Style.RESET_ALL}')


def create_tree(root, nodes):
    parents = []
    root_node = Nd(root.data['title'])
    parent = root_node
    parents.append(parent)
    folders = dict()
    folders[root.data['title']] = root.data['id']

    for i in range(len(nodes)):
        id = nodes[i].data['id']
        title = nodes[i].data['title']
        if (nodes[i].has_children):
            for parent in parents:
                if (parent.name == nodes[i].parent.data['title']):
                    node = Nd(title, parent)
                    folders[title] = id
                    parents.append(node)
                    continue

            node = Nd(title, root_node)
            folders[title] = id
            parents.append(node)

        else:
            for parent in parents:
                if (parent.name == nodes[i].parent.data['title']):
                    node = Nd(title, parent)
                    folders[title] = ''

    for pre, fill, node in RenderTree(root_node):
        folder_id = folders[node.name]
        if folder_id == '':
            click.echo("%s%s" % (pre, node.name))
        else:
            click.echo(f'{pre}{Fore.BLUE}{folder_id} {node.name} {Style.RESET_ALL}')

def open_vim(data):
    str += data['title'] + '\n'
    str += html_to_text(data['body'])

    EDITOR = os.environ.get('EDITOR','vim') #that easy!

    # initial_message = b"" # if you want to set up the file somehow
    # initial_message = bytearray(str) 
    initial_message = bytearray(str, encoding='utf8')


    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        call([EDITOR, tf.name])

        # do the parsing with `tf` using regular File operations.
        # for instance:
        tf.seek(0)
        edited_message = tf.read()
        print (edited_message.decode("utf-8"))
