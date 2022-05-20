# Guidance on how to contribute

> All contributions to this project will be released under the CC0 public domain
> dedication. By submitting a pull request or filing a bug, issue, or
> feature request, you are agreeing to comply with this waiver of copyright interest.
> Details can be found in our [TERMS](TERMS.md) and [LICENSE](LICENSE).

There are two primary ways to help:

-   Using the issue tracker, and
-   Changing the code-base.

## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions.
This is also a great way to connect with the developers of the project as well
as others who are interested in this solution.

Use the issue tracker to find ways to contribute. Find a bug or a feature, mention in
the issue that you will take on that effort, then follow the _Changing the code-base_
guidance below.

## Changing the code-base

Generally speaking, you should fork this repository, make changes in your
own fork, and then submit a pull request. All new code should have associated
unit tests that validate implemented features and the presence or lack of defects.
Additionally, the code should follow any stylistic and architectural guidelines
prescribed by the project. In the absence of such guidelines, mimic the styles
and patterns in the existing code-base.

## Setup the project

Follow this quick guide to clone and setup the project and be able to run and develop the project on your own computer.

1. Clone GitLab project

    **With SSH:**

    ```Shell
    git clone git@github.com:Magnus2142/Blackboard-LMS-CLI.git
    cd Blackboard-LMS-CLI
    ```

    **With HTTPS:**

    ```Shell
    git clone https://github.com/Magnus2142/Blackboard-LMS-CLI.git
    cd Blackboard-LMS-CLI
    ```

2. Create a virtual environment inside project folder

    ```Shell
    virtualenv venv
    source venv/bin/activate
    #Install all the requirements
    python -m pip install -r requirements.txt
    ```

3. Setup bb script inside the root of the project

    ```Shell
    pip install --editable . OR pip3 install --editable .
    ```

    At last, enter “bb” and a help page with list of commands should pop up like this:

```Shell
(venv) user@data:~/gitlab/idatt2900-072$ bb
Usage: bb [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  announcements  Commands for listing, creating, deleting and updating...
  assignments    Commands for creating, listing and submitting assignments
  contents       Commands for listing, creating, deleting, updating and...
  courses        Commands for listing courses
  login          Authorize user with username and password
  logout         Logout user

```

## Browser support

We configure our build chain tools
(typically [Autoprefixer](https://github.com/postcss/autoprefixer)
and [Babel](https://babeljs.io))
to support a reasonable set of backward compatibility with older browsers.

Please read up on
[our current browser support guidance](https://github.com/cfpb/development/blob/main/guides/browser-support.md)
and follow it when contributing to this project.
