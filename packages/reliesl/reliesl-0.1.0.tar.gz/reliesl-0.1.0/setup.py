# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['reliesl', 'reliesl.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'requests>=2.22,<3.0',
 'semver>=2.8,<3.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['reliesl = reliesl.cli:main']}

setup_kwargs = {
    'name': 'reliesl',
    'version': '0.1.0',
    'description': 'Reliesl is a tool for automatic release managment using the Gitlab CI.',
    'long_description': '<p align="center">\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n# reliesl\nreliesl helps you automate your releases using `poetry` and GitLab CI.\n\n<div align="center">\n    <img src="assets/liesl.jpg" alt="Liesl" width=200px align="middle">\n</div>\n\n"You\'ve had a long day at work. Bugs have been squashed, features wered added and breaking changes documented. You\'ve poured your heart and soul into this piece of software and the last thing seperating you from popping a bottle of champagne is having to release the newest version of your project on GitLab. Thank God there\'s reliesl to release your new software on GitLab (and maybe even open that bottle of champagne)."\n\\- reliesl\'s secret admirer\n\n## How to use\nreliesl provides two different command line scripts for you:\n\n### reliesl release\nCan be added to your existing CI pipeline to manually trigger a new GitLab release based on the releasenotes given in CHANGELOG.md. Also adds the .whl of the package to the Asset section.\n\n### reliesl bump\nCan be run locally to take care of all cumbersome version edits in various files. Automatically parses the CHANGELOG.md to create a version from the current UNRELEASED section and adds a new section.\n\nAdditional files where version changes are needed can be configured as a command line argument. This makes it flexible to use if you already have a script for reusable commands, like a Makefile.\n\n## Install\nCurrently the only way to install this repository is through git.\n\n### poetry:\nSimply add\n```\nreliesl = {git = "https://gitlab.com/luminovo/public/reliesl.git", branch="master"}\n```\nto your pyproject.toml under `[tool.poetry.dependencies]`\n\n### GitLab-CI\nTo your .gitlab-ci.yml you need to add:\n\n - A new `- deploy` stage if you do not already have one (The release process should be the last stage)\n\n - A new job:\n```\nrelease:\n  stage: deploy\n  when: manual\n  script:\n    - pip install pip --upgrade pip\n    - pip install git+https://gitlab.com/luminovo/public/reliesl.git@master\n    - reliesl release\n```\n\n\n### Environment Variables\nThe release script needs access to the GitLab API to create a new release. This requires a new environment variable(Under Settings > CI / CD > Variables):\n * Key: `PRIVATE_TOKEN`\n * Value: a valid private token that gives access to api calls for your project(Profile > Settings > Access Tokens)\n\n### Makefile(Optional)\nOptionally you can add \n```\nbump: ## Bump Version \n\tpoetry run reliesl bump\n```\nto your makefile to have easy access from the command line to the version bumper.\n\n\n# Tips\n\nUsing the `reliesl release --pypi-release <value>` option, you can also automatically release to either `pypi` or `testpypi`. For authentication this requires the environement variables  `PYPI_USERNAME` and  and `PYPI_PASSWORD` or `TESTPYPI_USERNAME` and `TESTPYPI_PASSWORD`.\n\n\nUse `reliesl bump --additional-file-edits <file> <pythonregexpr>` to specify other locations for version changes. \nUse the `--dry-run` flag to only visualize changes to debug the regular expression. \nThe second capture group must be the semantic version you want to change.\nExample:\n```\nreliesl bump --additional-file-edits "file.txt" \'(semver = )(.*)()\' "file2.txt" \'(version: )(.*)\'\n```\n\nFor more information on python regular expressions use https://docs.python.org/3.7/howto/regex.html\n\n## Development\n\n### Pre-commit\nPlease make sure to have the pre-commit hooks installed.\nInstall [pre-commit](https://pre-commit.com/) and then run `pre-commit install` to register the hooks with git.\n\n### Poetry\nUse [poetry](https://poetry.eustace.io/) to manage your dependencies.\nPlease make sure it is installed for your current python version.\nThen start by adding your dependencies:\n```console\npoetry add bump2version\n```\n\n### Makefile\nWe use [make](https://www.gnu.org/software/make/) to streamline our development workflow.\nRun `make help` to see all available commands.\n\n<!-- START makefile-doc -->\n```\n$ make help \nhelp                 Show this help message\ncheck                Run all static checks (like pre-commit hooks)\ntest                 Run all tests\ndev-install          Install all the packages in the local python environment for development\nbump                 Bump Version  \n```\n<!-- END makefile-doc -->\n\n## Other\n\nPicture Source: https://ladiesoftheatre.tumblr.com/post/155234955388/you-may-think-this-kind-of-adventure-never-may\n',
    'author': 'Benedikt Wiberg',
    'author_email': 'benedikt@luminovo.ai',
    'url': 'https://gitlab.com/luminovo/public/reliesl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
