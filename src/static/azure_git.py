import requests
import urllib3
import yaml
import json
import base64
from .config import organization_url, username, PAT, output_file

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_request(*args, **kwargs):
    """Sends HTTP requests to Azure DevOps API"""
    url = organization_url + "".join(args)
    if kwargs.get("is_release"):
        url = release_url + "".join(args)

    if kwargs.get("request_method") == "get":
        handler = requests.get
    elif kwargs.get("request_method") == "post":
        handler = requests.post
    elif kwargs.get("request_method") == "put":
        handler = requests.put
    elif kwargs.get("request_method") == "delete":
        handler = requests.delete
    else:
        log.error("No requests method selected")
        raise LookupError
    response = handler(url, auth=(username, PAT), verify=False, data=kwargs.get("data"), headers=kwargs.get("headers"))
    if response.status_code == 409:
        print("Repository already exists")
    return response.json()

def create_repository(project_name: str, repo_name: str) -> None:
    """Creates a new repo under the specified project"""
    # Load the repo request data from disk
    try:
        with open("C:\\Users\\owensr\\Documents\\Scripts\\Python\\Azure-DevOps-Pipelines-Generator\\src\\static\\repo_request_body.json", "r") as file:
            repo_request_body = json.load(file)
    except IOError as e:
        raise Exception(e, "Unable to open repo_request_body.json")

    # Update JSON dictionary with new ID from server API
    repo_request_body["project"]["id"] = make_request(
        "_apis/projects/",
        project_name,
        "?api-version=5.1-preview.1",
        request_method="get"
    ).get("id")

    # Update JSON dictionary with new repo name
    repo_request_body["name"] = repo_name

    # Make the server request to create the repo
    make_request(
        project_name,
        "/_apis/git/repositories",
        "?api-version=5.1-preview.1",
        request_method="post",
        data=json.dumps(repo_request_body),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Basic eWFtbF9nZW5lcmF0b3JfcGF0OnBxb2JhdnNvNGlkZWY2ZG0ydnZiNGw0bnl4ZDZra2U0ZnRlcXFpNHBjcW52cWFxNGJta2E',
        }
    )

def commit_yaml_file(project_name: str, repo_name: str) -> None:
    """Commit YAML file to new repository"""
    # Load commit request data from disk
    try:
        with open("C:\\Users\\owensr\\Documents\\Scripts\\Python\\Azure-DevOps-Pipelines-Generator\\src\\static\\commit_request_body.json", "r") as file:
            commit_request_body = json.load(file)
    except IOError as e:
        raise Exception(e, "Unable to open commit_request_body.json")

    def convertYAMLBase64():
        """ Convert YAML file to Base64"""
        try:
            with open (f".\\{output_file}", "rb") as file:
                _yaml_64 = base64.b64encode(file.read())
        except IOError as e:
            raise Exception(e, f"Unable to open {output_file}")
        return _yaml_64

    # Converting azure-pipelines.yml to base64 and removing 'b' prefix
    yaml_64 = convertYAMLBase64().decode("utf-8")

    # Update JSON dictionary with base64 YAML content
    commit_request_body["commits"][0]["changes"][0]["newContent"]["content"] = yaml_64

    # Make request to commit YAML file
    make_request(
        f"/{project_name}/_apis/git/repositories/{repo_name}/pushes?api-version=5.1",
        request_method="post",
        data=json.dumps(commit_request_body),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Basic eWFtbF9nZW5lcmF0b3JfcGF0OnBxb2JhdnNvNGlkZWY2ZG0ydnZiNGw0bnl4ZDZra2U0ZnRlcXFpNHBjcW52cWFxNGJta2E',
        }
    )
