# Blackboard LMS CLI

----
<img src="/uploads/a2b91adfa7cb2daea2c6865253afd5e5/cli-logo.png" align="left" width="192px" height="192px"/>
<img align="left" width="0" height="192px" hspace="10"/>

> Command-line tool suite for Blackboard LMS

[![Under Development](https://img.shields.io/badge/under-development-orange.svg)](https://github.com/cezaraugusto/github-template-guidelines) [![Public Domain](https://img.shields.io/badge/public-domain-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/) [![Travis](https://img.shields.io/travis/cezaraugusto/github-template-guidelines.svg)](http://github.com/cezaraugusto/github-template-guidelines)

Blackboard LMS CLI is a command-line tool suite that students and staff can use to communicates with the Blackboard Learn REST API. It was created because the blackboard web interface can be ineffective and awkward to use. The CLI aims to offer a simple, intuitive and effective way to execute tasks in the Blackboard LMS. The software is written in python and based on the python package [Click](https://click.palletsprojects.com/en/8.1.x/)


<!-- <br>
<p align="center">
<strong>Templates included:</strong>
<a href="/.github/README.md">README</a> • <a href="/.github/CONTRIBUTING.md">CONTRIBUTING </a> • <a href="/.github/PULL_REQUEST_TEMPLATE.md">PULL REQUEST</a> • <a href="/.github/ISSUE_TEMPLATE.md">ISSUE TEMPLATE</a> • <a href="/.github/CONTRIBUTORS.md">CONTRIBUTORS</a>
</p>
<br> -->

**Links to production or demo instances:** LInksssss


![Image](/uploads/8780c8ce8ccb66bfe0bad77eb9410769/image.png)

## Installation

**NB!** Currently, this CLI can only be installed using pip, but we are planning to support other installation methods later.

1. Install pip package

    ```Shell
    pip install Blackboard-LMS-CLI
    ```
2. Install ```magic``` dependecy
    ```Shell
    # Windows:
    pip install python-magic-bin

    # Linux:
    sudo apt-get install libmagic1

    # Mac OS X
    brew install libmagic1
    ```

Test if the installation was successful by running ```$ bb --version``` command. You should see something like this:

![bb-version-command](/uploads/7ac03cafbe917fd399267a2bde3b90f4/image.png)

TODO: Add shell completion add

## Dependencies

For this CLI to work you need python and pip installed on your computer. The CLI also uses the library [magic](https://pypi.org/project/python-magic/).

**The following libraries are required:**

- Click
- colorama
- requests
- python-dotenv
- beautifulsoup4
- lxml
- shellingham
- anytree
- html2text
- python-dateutil


## Configuration

TODO:

If the software is configurable, describe it in detail, either here or in other documentation to which you link.

## Usage

TODO:

Show users how to use the software.
Be specific.
Use appropriate formatting when showing code snippets.



## How to test the software

TODO:

If the software includes automated tests, detail how to run those tests.

## Known issues

TODO:

Document any known significant shortcomings with the software.

## Getting help

TODO:

Instruct users how to get help with this software; this might include links to an issue tracker, wiki, mailing list, etc.

**Example**

TODO:

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

TODO:

This section should detail why people should get involved and describe key areas you are
currently focusing on; e.g., trying to get feedback on features, fixing certain bugs, building
important pieces, etc.

General instructions on _how_ to contribute should be stated with a link to [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info

TODO:

1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----

## Credits and references

TODO:

1. Projects that inspired you
2. Related projects
3. Books, papers, talks, or other sources that have meaningful impact or influence on this project

#### CFPB Open Source Project Template Instructions

1. Create a new project.
2. [Copy these files into the new project](#installation)
3. Update the README, replacing the contents below as prescribed.
4. Add any libraries, assets, or hard dependencies whose source code will be included
   in the project's repository to the _Exceptions_ section in the [TERMS](TERMS.md).
  - If no exceptions are needed, remove that section from TERMS.
5. If working with an existing code base, answer the questions on the [open source checklist](opensource-checklist.md)
6. Delete these instructions and everything up to the _Project Title_ from the README.
7. Write some great software and tell people about it.

> Keep the README fresh! It's the first thing people see and will make the initial impression.