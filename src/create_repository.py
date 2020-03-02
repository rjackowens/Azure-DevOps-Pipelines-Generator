import requests
import urllib3
import yaml
import json
from config import organization_url, username, PAT


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

project_name = input("Enter project name: ")
repo_name = input("Enter new repo name: ")

# project_name = "utilities"
# repo_name = "test97"

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
    # print(response.status_code)
    # print(response.json())


class RepositoryMaker:
    """Creates new Azure DevOps repositories"""
    def __init__(self, project_name, repo_name):
        self.project_name = project_name
        self.repo_name = repo_name
        with open("./repo_request_body.json", "r") as file:
            self.data = json.load(file)


    def get_project_id(self):
        """Returns the Azure DevOps project ID for a project name"""
        _request_object = make_request(
            "_apis/projects/",
            self.project_name,
            "?api-version=5.1-preview.1",
            request_method = "get"
            )
        return _request_object.get("id")


    def update_project_id(self):
        """Updates JSON dictionary with new ID"""
        new_id = self.get_project_id()
        self.data["project"]["id"] = new_id


    def update_repo_name(self):
        """Updates JSON dictionary with new repo name"""
        self.data["name"] = self.repo_name
        return self.data


    json_content_type = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic eWFtbF9nZW5lcmF0b3JfcGF0OnBxb2JhdnNvNGlkZWY2ZG0ydnZiNGw0bnl4ZDZra2U0ZnRlcXFpNHBjcW52cWFxNGJta2E='
        }


    def create_repository(self): #need to add repo name too
        """Creates a new repo under the specified project"""
        self.update_project_id()
        repo_request_body = self.update_repo_name()
        make_request(
            self.project_name,
            "/_apis/git/repositories",
            "?api-version=5.1-preview.1",
            request_method = "post",
            data = json.dumps(repo_request_body),
            headers = self.json_content_type
        )


x = RepositoryMaker(project_name, repo_name)

x.create_repository()


class YamlMaker:
    def __init__(self):
        # to-do

