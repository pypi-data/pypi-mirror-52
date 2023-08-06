import datetime
import os
import re
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

import click
import semver
import toml

CHANGELOG = Path("CHANGELOG.md")
PYPROJECT = Path("pyproject.toml")
PYPROJECT_BUMP_CONFIG = (PYPROJECT, '(version = ")(.*)(")')
EMPTY_PATCH = {
    "version": "UNRELEASED",
    "date": "YYYY-MM-DD\n",
    "release_notes": "\n### Added\n### Fixed\n### Changed\n\n",
}

RELEASE_CHOICES = {
    "1": {
        "description": "MAJOR version when you make incompatible API changes",
        "function": semver.bump_major,
    },
    "2": {
        "description": "MINOR version when you add functionality in a backwards compatible manner",
        "function": semver.bump_minor,
    },
    "3": {
        "description": "PATCH version when you make backwards compatible bug fixes",
        "function": semver.bump_patch,
    },
}
PRERELEASE_CHOICES = {
    "4": {
        "description": "RELEASE version when you want to release this version",
        "function": semver.finalize_version,
    },
    "5": {
        "description": "PRERELEASE version when you want to add a new prerelease",
        "function": semver.bump_prerelease,
    },
}


# Type Definitions
Releasenotes = Dict[str, str]
Changelog = List[Releasenotes]


def _get_date() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")


def load_changelog(changelog_file: Path = CHANGELOG) -> Changelog:
    """

    Args:
        changelog_file: path to changelog in keepachangelog.com format

    Returns: List of releasenote dicts with the following fields:
        - version: Version number of the patch
        - date: Date of the patch
        - release_notes: Markdown formatted release_notes

    """
    with changelog_file.open() as file:
        changelog = []
        current_version = None
        for line in file:
            if line.startswith("## "):
                # Guarantees that only valid release_notes are added
                if current_version:
                    changelog += [current_version]
                parts = line.split(" ")
                patch_version = parts[1]
                try:  # Additional check in case no date is given and as such can not be parsed
                    patch_date = parts[3]
                except IndexError:
                    patch_date = "YYYY-MM-DD"
                current_version = {
                    "version": patch_version,
                    "date": patch_date,
                    "release_notes": "",
                }
            else:
                if current_version:
                    current_version["release_notes"] += line
    changelog += [current_version]
    return changelog


def _format_release_notes(release_notes: Releasenotes) -> str:
    return f"## {release_notes['version']} - {release_notes['date']}{release_notes['release_notes']}"


def save_changelog(changelog: Changelog, filename: Path):
    """

    Args:
        changelog: Changelog in the same format as returned by load_changelog()
        filename: filepath under which the changelog will be saved

    """
    click.echo("Saving changelog...")
    tmpfile = filename.with_suffix(".tmp")
    with tmpfile.open("w+") as file:
        for release in changelog:
            file.write(_format_release_notes(release))
    tmpfile.rename(filename)


def change_version_in_files(
    additional_file_edits: List[Tuple[Path, str]], version: str, dry_run: bool = False
):
    """

    Args:
        additional_file_edits: List of tuples containing a filepath and a regexpr
        version: Changed Version
        dry_run: Flag to check if no edits should be made. Helpful when debugging
            the regular expression.

    """
    for file, regexp in additional_file_edits:
        # Use tmpfile in case of crash, will replace original later
        # Careful when using, you need to guarantee that the whole line gets matched
        click.echo(f"Changes in {file} :")
        tmp_file = file.with_suffix(".tmp")
        with file.open("r") as realfile, tmp_file.open("w+") as tmpfile:
            if dry_run:
                click.echo(f"{regexp} finds: ")
            regexp = re.compile(regexp)
            for line in realfile:
                re.compile(regexp)
                line_match = regexp.match(line)
                if line_match:
                    click.echo(f"\t{line[:-1]} -> ", nl=False)
                    matches = list(line_match.groups())
                    matches[1] = version
                    line = "".join(matches) + "\n"
                    click.echo(line)
                tmpfile.write(line)
        if dry_run:
            tmp_file.unlink()
        else:
            tmp_file.rename(file)


def ask_patchtype(project_current_version: str):
    click.echo(f"The current version is: {project_current_version}")
    click.echo("What kind of update do you want to make?")
    if semver.parse(project_current_version)["prerelease"]:
        RELEASE_CHOICES.update(PRERELEASE_CHOICES)
    for key, value in RELEASE_CHOICES.items():
        click.echo(
            f"({key}) {value['function'](project_current_version)}\t - {value['description']}"
        )
    click.echo("For more information visit https://semver.org/")
    patch_type = click.prompt("> ", type=click.Choice(RELEASE_CHOICES.keys()))
    patch_type = RELEASE_CHOICES[patch_type]
    return patch_type["function"](project_current_version)


def _show_release_notes(release_notes: Releasenotes):
    click.echo(_format_release_notes(release_notes))
    click.echo("-----")
    click.confirm(
        "This is how the new release_notes will look like. Do you want to continue?",
        abort=True,
    )


def get_version_and_name(pyproject_file: Path = PYPROJECT):
    with pyproject_file.open() as file:
        pyproject = toml.load(file)
    project_pyproject = pyproject["tool"]["poetry"]
    project_current_version = project_pyproject["version"]
    project_name = project_pyproject["name"]
    return project_current_version, project_name


def _parse_file_edits(ctx, params, value):
    return [(Path(file_regex[0]), file_regex[1]) for file_regex in value]


@click.command(help="Bump the version number for your project.")
@click.option(
    "--project-dir",
    default=Path.cwd(),
    callback=lambda ctx, params, value: Path(value),
    help="Directory in which to look for the CHANGELOG.md and pyproject.toml",
)
@click.option(
    "--additional-file-edits",
    "-f",
    nargs=2,
    multiple=True,
    callback=_parse_file_edits,
    help="Specify <file> <regex> for additional files and a corresponding regex where "
    "the version number needs to be bumped.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Do a dry run to check if file edits work correctly without changing any files.",
)
@click.option(
    "--prerelease",
    is_flag=True,
    default=False,
    help="Change new version to a prerelease.",
)
def bump(
    project_dir: Path, additional_file_edits: List[str], dry_run: bool, prerelease: bool
):
    additional_file_edits.append(PYPROJECT_BUMP_CONFIG)
    # Change to the projects directory in a revertible way
    prevdir = Path.cwd()
    os.chdir(project_dir.resolve())
    try:
        if dry_run:
            click.echo("It's a dry run.")
            click.echo("The following file edits would be made:")
            change_version_in_files(
                additional_file_edits, version="<NEWVER>", dry_run=True
            )
            click.echo(
                "\nP.S. Be careful to capture the whole line, not captured parts will be deleted!"
            )
            exit(0)

        project_current_version, project_name = get_version_and_name()
        new_version = ask_patchtype(project_current_version)
        if prerelease:
            new_version = semver.bump_prerelease(new_version)
        changelog = load_changelog(CHANGELOG)

        if changelog[0]["version"] != "UNRELEASED":
            raise SystemExit(
                "No new release_notes detected. (Start with '## UNRELEASED')"
            )

        changelog[0]["version"] = new_version
        changelog[0]["date"] = _get_date() + "\n"
        _show_release_notes(changelog[0])

        # Start of all permanent changes
        changelog.insert(0, EMPTY_PATCH)
        save_changelog(changelog, CHANGELOG)

        # Bump in all other files
        change_version_in_files(additional_file_edits, version=new_version)
    finally:
        os.chdir(prevdir)
