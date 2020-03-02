import yaml

repository = "remote"
repo_type = "git"
inputs = "inputs"
repo_name = "DevOps/CICD.Scripts"
ref = "refs/heads/master"

repo_dict = {}

repo_dict["repository"] = repository #input("Enter command: ")
repo_dict["type"] = repo_type #input("Enter projects: ")
repo_dict["name"] = repo_name #input("Feeds to use: ")
repo_dict["ref"] = ref #input("Enter verbosity for restore: ")

# print(repo_dict)

repos_dict = {}
repos_dict["repositories"] = repo_dict

resource_object = yaml.dump([{'task': repository, 'resources': repos_dict}], default_flow_style=False, sort_keys=False)
print(resource_object)
