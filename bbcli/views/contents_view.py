from anytree import Node as Nd, RenderTree
from colorama import Fore, Style
from bbcli.utils.utils import html_to_text
import click
import tempfile, os
from subprocess import call

def list_tree(folder_ids, root, only_folders = False):
    color = Fore.RESET if only_folders else Fore.BLUE
    for pre, fill, node in RenderTree(root):
        if not node.children and only_folders == False:
            click.echo("%s%s" % (pre, node.name))
        else:
            folder_id = folder_ids[node.name]
            click.echo(f'{pre}{color}{folder_id} {node.name} {Style.RESET_ALL}')

def open_vim(data):
    str = data['title'] + '\n'
    str += html_to_text(data['body'])

    EDITOR = os.environ.get('EDITOR','vim') #that easy!

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
