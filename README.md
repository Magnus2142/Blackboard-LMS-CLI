[![Under Development](https://img.shields.io/badge/under-development-orange.svg)](https://github.com/cezaraugusto/github-template-guidelines) [![Public Domain](https://img.shields.io/badge/public-domain-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/) [![Travis](https://img.shields.io/travis/cezaraugusto/github-template-guidelines.svg)](http://github.com/cezaraugusto/github-template-guidelines)

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/Magnus2142/Blackboard-LMS-CLI/issues">
    <img src="https://user-images.githubusercontent.com/54250237/162905944-761af968-d419-42ba-9864-3a443782cd4a.png" alt="Logo" width="140" height="140">
  </a>

  <h3 align="center">Blackboard-LMS-CLI</h3>

  <p align="center">
    Command-line tool suite for Blackboard LMS
    <br />
    <a href="https://github.com/Magnus2142/Blackboard-LMS-CLI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://asciinema.org/a/6OQm4JDG0Uh71YrX1BXF7Hi6P">View Demo</a>
    ·
    <a href="https://github.com/Magnus2142/Blackboard-LMS-CLI/issues">Report Bug</a>
    ·
    <a href="https://github.com/Magnus2142/Blackboard-LMS-CLI/issues">Request Feature</a>
  </p>
</div>

---

<!-- ABOUT THE PROJECT -->

## About The Project

```Shell
user@computer:~$ bb

Usage: bb [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  announcements              Commands for listing, creating, deleting and...
  assignments                Commands for creating, listing and...
  contents                   Commands for listing, creating, deleting,...
  courses                    Commands for listing courses
  login                      Authorize user with username and password.
  logout                     Logout user.

```

```Shell
user@computer:~$ bb courses list

Id           Course Name

_33050_1     Donn Alexander Morrison testrom
_32909_1     Sammenslått - Ingeniørfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 VÅR)
_31606_1     INGT2300 Ingeniørfaglig systemtenkning (2022 VÅR)
_32736_1     Sammenslått - Matematiske metoder 3 for dataingeniører IMAX2150 (2021 HØST)
_28936_1     IMAT2150 Matematiske metoder 3 for dataingeniører (2021 HØST)
_27251_1     IDATT2900 Bacheloroppgave  (start 2021 HØST)

```

Blackboard LMS CLI is a command-line tool suite that students and staff can use to communicates with the Blackboard Learn REST API. It was created because the blackboard web interface can be ineffective and awkward to use. The CLI aims to offer a simple, intuitive and effective way to execute tasks in the Blackboard LMS.

### Built With

The software is written in python. Several libraries were used, but the most essential ones are:

-   [Click](https://click.palletsprojects.com/en/8.1.x/) - A python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
-   [Requests](https://docs.python-requests.org/en/latest/) - A library used to send HTTP requests in a simple and elegant way.
-   [Beautiful Soup](crummy.com/software/BeautifulSoup/bs4/doc/) - A library used to pull data out from HTML and XML files.

A complete list of all libraries can be found in the [dependencies](https://github.com/Magnus2142/Blackboard-LMS-CLI#dependencies) section.

<!-- GETTING STARTED -->

## Getting Started

Some instructions on how to quickly make the CLI available on your computer!

### Prerequisites

To run this CLI you need python and pip installed.

### Installation

**NB!** Currently, this CLI can only be installed using pip, but we are planning to support other installation methods later.

```Shell
pip install Blackboard-LMS-CLI
```

Test if the installation was successful by running `$ bb --version` command:

```Shell
bb --version
```

If it was successfull, the output should be something like this:

```Shell
bb, version 0.1.0
```

**Shell completion:** The CLI also supports shell completion with TAB, but is currently only comaptible with bash, zsh and fish. To activate this you can follow the guide here: [Click shell completion help page](https://click.palletsprojects.com/en/8.1.x/shell-completion/).

<!--
```Shell
bb activate-shell-completion {YOUR_SHELL}
```

This feauture is still unstable and if you encounter any problems, please check the [Click shell completion help page](https://click.palletsprojects.com/en/8.1.x/shell-completion/).
-->

## Usage

First of all, you can either login using the command:

```Shell
bb login
```

or just execute the command you want, and you'll be logged in if you aren't already.

The CLI is designed in such a way that its commands and subcommands, is structured much alike like the Blackboard Learn REST API modules. `bb` is the main command, then for example is `courses` a subcommand of `bb`, and at last, `list` is a subcommand of `courses`. See [demo here](https://asciinema.org/a/6OQm4JDG0Uh71YrX1BXF7Hi6P)

All commands contains a help page that can be accessed through adding the flag `--help`, for example if I want to see the help page about creating a file content:

```Shell
bb contents create file --help
```

**Output:**

```Shell
Usage: bb contents create file [OPTIONS] TITLE FILE_PATH

  Creates a file content.

Options:
  -c, --course TEXT   COURSE ID, of the course where the content exists
                      [required]
  -f, --folder TEXT   FOLDER ID, of the folder you want to create content in.
                      [required]
  -n, --new-window
  --end-date TEXT     When to make content unavailable. Format: DD/MM/YY
                      HH:MM:SS
  --start-date TEXT   When to make content available. Format: DD/MM/YY
                      HH:MM:SS
  -r, --reviewable    Make content reviewable
  -h, --hide-content  Hide contents for students
  --help              Show this message and exit.
```

Using the `--help` flag is very useful, because many commands have many possible options which can be hard to memorize in the beginnning.

**Example usage of the CLI:**

-   [List announcements demo](https://asciinema.org/a/8sxEjQXw2eJmnEFYvIqKnKS0H)
-   [Create announcement demo](https://asciinema.org/a/I81I5PKOPissGIyO5GPIJNXyB)
-   [List course content demo](https://asciinema.org/a/mEQRuVIzT3rZYHvtGwlV5zhHV)
-   [Get spesific course content demo](https://asciinema.org/a/8OwCw8D6Zms2n2AGawfRjxIUc)
-   [Create a file content demo](https://asciinema.org/a/QGq3fg4Pfx8ILRHKYLdfXACYg)

## Dependencies

For this CLI to work you need python and pip installed on your computer.

**The following libraries are required:**

-   [Click](https://click.palletsprojects.com/en/8.1.x/)
-   [colorama](https://pypi.org/project/colorama/)
-   [requests](https://docs.python-requests.org/en/latest/)
-   [python-dotenv](https://pypi.org/project/python-dotenv/)
-   [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
-   [lxml](https://pypi.org/project/lxml/)
-   [shellingham](https://pypi.org/project/shellingham/1.2.5/)
-   [anytree](https://pypi.org/project/anytree/)
-   [html2text](https://pypi.org/project/html2text/)
-   [python-dateutil](https://pypi.org/project/python-dateutil/1.4/)
-   [tabulate](https://pypi.org/project/tabulate/)

## Configuration

At the moment, the CLI is not configurable. However, this is something we plan on adding in the future.

**Ideas configurable elements**:

-   A setting that chooses whether ID's such as course id and content id is used as positional arguments or required options.
-   If they want the responses in json byt default or just plain text, formatted by the CLI.

## How to test the software

Unit tests have been created for almost all service methods, in other words, where the HTTP requests and processing of data from the Blackboard Learn REST API takes place.

**To run the tests:**

1. Make sure to create a virtual python environment in the project. With python package `virtualenv` it can be created like this:

    ```Shell
    virtualenv venv
    source venv/bin/activate
    ```

2. Make sure all requirements are installed:

    ```Shell
    python -m pip install -r requirements.txt
    ```

3. Run tests using pytest:

    ```Shell
    python -m pytest
    ```

## Known issues

Even though this CLI aims to be more effective than the Blackboard web interface, we do acknowledge that it has its weaknesses. However, this is issues that isn't about bugs or needed functionality, but limitations of the CLI that either isn't possible to change or requires a comprehensive rework of the project. For bugs or desirable functionality, an issue should be created or [contact us by mail](https://github.com/Magnus2142/Blackboard-LMS-CLI#getting-help).

**Cryptic IDs:**

All IDs for courses, announcements, contents, etc. have a cryptic ID with the format `_33050_1`, which is hard to read and awkward to type. For example, it would be more convenient if the ID of a course would be `IDATT1001` and announcements and contents could be fetched using their title. However, this isn't possible because it can't guarantee that all course names, announcements, and content titles are unique.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker, or mail us:

**Mail info:**

-   hansw0701@gmail.com
-   mattias.a.eggen@gmail.com
-   magnus.bredeli@hotmail.com

## Getting involved

This started as a project for our Bachelor Thesis in Computer Engineering and we designed and developed the project in such a way that it was easy to understand and contribute. It was not enough time to implement all desired functionality and invite anyone who wants, to help fix bugs, implement new functionality, etc. One the biggest motivating factors when developing the CLI, was that if it was successful, with useful functionality and a more effective alternative to the Blackboard web interface, both teachers and students on NTNU will use it in their everyday student/work-life.

If you think this is a cool project and want to help us make it great by contributing, please read the [CONTRIBUTING](CONTRIBUTING.md) file to see how.

---

## Open source licensing info

1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

---

## Credits and references

Below is a list of useful reasources and guides that had a meaningful impact or influence on this project:

-   [How to build a python CLI](https://medium.com/nerd-for-tech/how-to-build-and-distribute-a-cli-tool-with-python-537ae41d9d78) - Gave us a quick introduction on how to setup a python project with some basic Click commands.
-   [Build a Command-Line To-Do App With Python and Typer](https://realpython.com/python-typer-cli/) - Another quick introduction to create a command-line tool in python, but with typer instead of click. Typer is a pyhton library based on Click, so the syntax was pretty much the same and this article gave us the idea of using the Model-View-Controller software design pattern.
