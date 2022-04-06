import os
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'bbcli', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

requires = [
    'Click',
    'colorama',
    'requests',
    'python-dotenv',
    'beautifulsoup4',
    'lxml>=4.8.0',
    'html2text',
    'python-magic'
]

def setup_package():
    metadata = dict(
        name=about['__title__'],
        version=about['__version__'],
        description=about['__description__'],
        long_description=readme,
        long_description_content_type='text/markdown',
        url=about['__url__'],
        author=about['__authors__'],
        author_email=about['__author_emails__'],
        license=about['__license__'],
        packages=find_packages(),
        include_package_data=True,
        dependency_links=['https://github.com/c0fec0de/anytree, https://github.com/sarugaku/shellingham'],
        install_requires=requires,
        entry_points={
            'console_scripts': [
                'bb=bbcli.__main__:main', # the cli() function runs inside the bbcli.py. cli is the command that is used to run the command
            ],
        }
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
    
    setup(**metadata)

if __name__ == '__main__':
    setup_package()

# setup(
#     name='bb',
#     # version='0.1.0',
#     # py_modules=['yourscript'],
#     install_requires=[
#         'Click',
#     ],
#     entry_points={
#         'console_scripts': [
#             'bb=bbcli.__main__:main', # the cli() function runs inside the bbcli.py. cli is the command that is used to run the command
#         ],
#     },
# )