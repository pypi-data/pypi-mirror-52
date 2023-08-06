<p align="center">
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# reliesl
reliesl helps you automate your releases using `poetry` and GitLab CI.

<div align="center">
    <img src="assets/liesl.jpg" alt="Liesl" width=200px align="middle">
</div>

"You've had a long day at work. Bugs have been squashed, features wered added and breaking changes documented. You've poured your heart and soul into this piece of software and the last thing seperating you from popping a bottle of champagne is having to release the newest version of your project on GitLab. Thank God there's reliesl to release your new software on GitLab (and maybe even open that bottle of champagne)."
\- reliesl's secret admirer

## How to use
reliesl provides two different command line scripts for you:

### reliesl release
Can be added to your existing CI pipeline to manually trigger a new GitLab release based on the releasenotes given in CHANGELOG.md. Also adds the .whl of the package to the Asset section.

### reliesl bump
Can be run locally to take care of all cumbersome version edits in various files. Automatically parses the CHANGELOG.md to create a version from the current UNRELEASED section and adds a new section.

Additional files where version changes are needed can be configured as a command line argument. This makes it flexible to use if you already have a script for reusable commands, like a Makefile.

## Install
Currently the only way to install this repository is through git.

### poetry:
Simply add
```
reliesl = {git = "https://gitlab.com/luminovo/public/reliesl.git", branch="master"}
```
to your pyproject.toml under `[tool.poetry.dependencies]`

### GitLab-CI
To your .gitlab-ci.yml you need to add:

 - A new `- deploy` stage if you do not already have one (The release process should be the last stage)

 - A new job:
```
release:
  stage: deploy
  when: manual
  script:
    - pip install pip --upgrade pip
    - pip install git+https://gitlab.com/luminovo/public/reliesl.git@master
    - reliesl release
```


### Environment Variables
The release script needs access to the GitLab API to create a new release. This requires a new environment variable(Under Settings > CI / CD > Variables):
 * Key: `PRIVATE_TOKEN`
 * Value: a valid private token that gives access to api calls for your project(Profile > Settings > Access Tokens)

### Makefile(Optional)
Optionally you can add 
```
bump: ## Bump Version 
	poetry run reliesl bump
```
to your makefile to have easy access from the command line to the version bumper.


# Tips

Using the `reliesl release --pypi-release <value>` option, you can also automatically release to either `pypi` or `testpypi`. For authentication this requires the environement variables  `PYPI_USERNAME` and  and `PYPI_PASSWORD` or `TESTPYPI_USERNAME` and `TESTPYPI_PASSWORD`.


Use `reliesl bump --additional-file-edits <file> <pythonregexpr>` to specify other locations for version changes. 
Use the `--dry-run` flag to only visualize changes to debug the regular expression. 
The second capture group must be the semantic version you want to change.
Example:
```
reliesl bump --additional-file-edits "file.txt" '(semver = )(.*)()' "file2.txt" '(version: )(.*)'
```

For more information on python regular expressions use https://docs.python.org/3.7/howto/regex.html

## Development

### Pre-commit
Please make sure to have the pre-commit hooks installed.
Install [pre-commit](https://pre-commit.com/) and then run `pre-commit install` to register the hooks with git.

### Poetry
Use [poetry](https://poetry.eustace.io/) to manage your dependencies.
Please make sure it is installed for your current python version.
Then start by adding your dependencies:
```console
poetry add bump2version
```

### Makefile
We use [make](https://www.gnu.org/software/make/) to streamline our development workflow.
Run `make help` to see all available commands.

<!-- START makefile-doc -->
```
$ make help 
help                 Show this help message
check                Run all static checks (like pre-commit hooks)
test                 Run all tests
dev-install          Install all the packages in the local python environment for development
bump                 Bump Version  
```
<!-- END makefile-doc -->

## Other

Picture Source: https://ladiesoftheatre.tumblr.com/post/155234955388/you-may-think-this-kind-of-adventure-never-may
