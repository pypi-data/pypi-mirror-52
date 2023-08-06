import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union
from urllib.parse import urljoin

import click
import requests
import semver

from reliesl.cli.bump import get_version_and_name
from reliesl.cli.bump import load_changelog

# Type Definitions
Header = Dict[str, str]
Asset = Dict[str, str]
Json = object


def get_project_data(project_api_url: str, auth: Header) -> Json:
    project_data = requests.get(project_api_url, headers=auth)
    project_data.raise_for_status()
    return project_data.json()


def upload_file(path: Path, project_api_url: str, auth: Header) -> Json:
    uploads_url = project_api_url + "/uploads"
    file = {"file": (path.name, path.open("rb"), "application/zip")}
    result = requests.post(uploads_url, files=file, headers=auth)
    result.raise_for_status()
    return result.json()


def release_version(
    semver: str,
    release_description: str,
    assets: Union[Asset, List[Asset]],
    project_api_url: str,
    auth: Header,
    ref: str = "master",
) -> Json:
    if not isinstance(assets, list):
        assets = [assets]
    release_url = project_api_url + "/releases"
    release_name = "v" + semver
    release_data = {
        "name": release_name,
        "tag_name": release_name,
        "ref": ref,
        "description": release_description,
        "assets": {"links": assets},
    }
    auth["Content-Type"] = "application/json"
    result = requests.post(release_url, json=release_data, headers=auth)
    result.raise_for_status()
    return result.json()


def upload_wheel(
    wheel_path: Path, project_api_url: str, project_url: str, auth: Header
) -> Asset:
    wheel_reply = upload_file(
        path=wheel_path, project_api_url=project_api_url, auth=auth
    )
    wheel_asset = {"name": wheel_reply["alt"], "url": project_url + wheel_reply["url"]}
    return wheel_asset


def find_wheel(project_name: str, version: str) -> Path:
    click.echo(
        f"Trying to find wheel... - {project_name}-{semver.finalize_version(version)}*.whl"
    )
    wheel_path = list(
        Path("dist/").glob(f"{project_name}-{semver.finalize_version(version)}*.whl")
    )
    if len(wheel_path) != 1:
        raise SystemExit(
            f"Wheel could either not be found or is ambiguous: {wheel_path}"
        )
    wheel_path = wheel_path[0]
    return wheel_path


def get_project_url(project_api_url: str, auth: Header) -> str:
    try:
        project_data = get_project_data(project_api_url=project_api_url, auth=auth)
    except requests.exceptions.HTTPError:
        raise SystemExit("Could not connect to gitlab api. Is the given token correct?")
    project_url = project_data["web_url"]
    return project_url


def get_commit(branch: str, project_api_url: str, auth: Header) -> str:
    result = requests.get(
        project_api_url + f"/repository/branches/{branch}", headers=auth
    )
    result.raise_for_status()
    return result.json()["commit"]["short_id"]


def check_for_version_conflict(version: str, project_api_url: str, auth: Header):
    result = requests.get(project_api_url + f"/releases", headers=auth)
    result.raise_for_status()
    result = result.json()
    if result:
        current_version = result[0]["tag_name"]
        if semver.compare(version, current_version[1:]) != 1:
            raise SystemExit(
                f"Release version v{version} is not newer than current version {current_version}!"
            )


def _get_release_notes() -> str:
    changelog = load_changelog()  # Only interested in newest release notes
    newest_release = 0
    try:  # Check if Release 0 is not an unreleased version
        semver.parse(changelog[newest_release]["version"])
    except ValueError:
        newest_release = 1
    patch = changelog[newest_release]
    return patch["release_notes"]


def _parse_project_url(ctx, param, value: str) -> str:
    if not value:
        value = "gitlab.com"
    if not value.endswith("/"):
        value += "/"
    if not value.startswith("http"):
        value = "https://" + value
    return value


@click.command(help="Release a new version of your project on GitLab.")
@click.option(
    "--project-dir",
    envvar="CI_PROJECT_DIR",
    type=click.Path(exists=True),
    help="Root directory of the project you want to release.",
)
@click.option(
    "--project-id",
    envvar="CI_PROJECT_ID",
    help="Unique GitLab ID for projects, available in Project Settings > General.",
)
@click.option(
    "--project-url",
    callback=_parse_project_url,
    envvar="CI_PROJECT_URL",
    help="URL of GitLab server.",
)
@click.option(
    "--pypi-release", type=click.Choice(["pypi", "testpypi"]), help="Release to PyPi"
)
def release(project_dir: str, project_id: str, project_url: str, pypi_release: str):
    project_dir = Path(project_dir)
    branch = os.environ.get("CI_COMMIT_REF_NAME")
    private_token = os.environ.get("PRIVATE_TOKEN")
    if not private_token:
        raise SystemExit("No private token given. Set $PRIVATE_TOKEN")
    auth = {"PRIVATE-TOKEN": private_token}
    if not branch:
        raise SystemExit("No branch specified. Set $CI_COMMIT_REF_NAME")
    if pypi_release:
        env_username = pypi_release.upper() + "_USERNAME"
        env_password = pypi_release.upper() + "_PASSWORD"
        username = os.environ.get(env_username)
        password = os.environ.get(env_password)
        if not (username and password):
            raise SystemExit(
                f"Try to publish to {pypi_release}, but environment variable {env_username} or {env_password} not set!"
            )
    # Change to the projects directory in a revertible way
    prevdir = Path.cwd()
    os.chdir(project_dir.resolve())
    try:
        version, name = get_version_and_name()
        project_api_url = urljoin(project_url, f"/api/v4/projects/{project_id}")
        project_url = get_project_url(project_api_url, auth)

        check_for_version_conflict(version, project_api_url, auth)

        commit = get_commit(branch, project_api_url, auth)
        click.echo(f'Release v{version} on branch "{branch}", commit "{commit}"')
        os.system(f"poetry build")
        wheel_path = find_wheel(name, version)

        wheel_asset = upload_wheel(
            wheel_path=wheel_path,
            project_api_url=project_api_url,
            auth=auth,
            project_url=project_url,
        )
        release_version(
            semver=version,
            release_description=_get_release_notes(),
            assets=wheel_asset,
            project_api_url=project_api_url,
            ref=branch,
            auth=auth,
        )
        if pypi_release:
            if pypi_release == "testpypi":
                os.system(
                    f"poetry publish -r {pypi_release} -u {username} -p {password}"
                )
            else:
                os.system(f"poetry publish -u {username} -p {password}")
    finally:
        os.chdir(prevdir)


if __name__ == "__main__":  # Helpful for debugging
    release(["--pypi-release", "testpypi"])
