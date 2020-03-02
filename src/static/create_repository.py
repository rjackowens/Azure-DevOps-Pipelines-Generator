import requests
import urllib3
import yaml
import json
from .config import organization_url, username, PAT

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
    # Load the repo request data from disk.
    with open("C:\\Users\\owensr\\Documents\\Scripts\\Python\\Azure-DevOps-Pipelines-Generator\\src\\static\\repo_request_body.json", "r") as file:
        data = json.load(file)

    # Update JSON dictionary with new ID from server API
    data["project"]["id"] = make_request(
        "_apis/projects/",
        project_name,
        "?api-version=5.1-preview.1",
        request_method="get"
    ).get("id")

    # Update JSON dictionary with new repo name
    data["name"] = repo_name

    # Make the server request to create the repo.
    make_request(
        project_name,
        "/_apis/git/repositories",
        "?api-version=5.1-preview.1",
        request_method="post",
        data=json.dumps(data),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Basic eWFtbF9nZW5lcmF0b3JfcGF0OnBxb2JhdnNvNGlkZWY2ZG0ydnZiNGw0bnl4ZDZra2U0ZnRlcXFpNHBjcW52cWFxNGJta2E',
        }
    )
