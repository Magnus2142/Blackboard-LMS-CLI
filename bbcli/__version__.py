VERSION = (0, 0, 3)
PRERELEASE = None  # alpha, beta or rc
REVISION = None


def generate_version(version, prerelease=None, revision=None):
    version_parts = ['.'.join(map(str, version))]
    if prerelease is not None:
        version_parts.append('-{}'.format(prerelease))
    if revision is not None:
        version_parts.append('.{}'.format(revision))
    return ''.join(version_parts)

__title__ = 'Blackboard LMS CLI'
__description__ = 'A command-line tool suite for communicating with the Blackboard Learn Managment System'
__url__ = 'https://gitlab.stud.idi.ntnu.no/mattiaae/idatt2900-072'
__version__ = generate_version(VERSION, prerelease=PRERELEASE, revision=REVISION)
__authors__ = 'Hans William Forebrigd, Mattias Aggentoft Eggen, Magnus Bredeli'
__author_emails__ = 'hansw0701@gmail.com, mattias.a.eggen@gmail.com, magnus.bredeli@hotmail.com'
__license__ = 'Willyeh Wonkmeh 2.0'