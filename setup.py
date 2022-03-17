from setuptools import setup

setup(
    name='cli',
    # version='0.1.0',
    # py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'bb=bbcli.__main__:main', # the cli() function runs inside the bbcli.py. cli is the command that is used to run the command
        ],
    },
)