import yaml
import sys

test = {
    1: "one",
    2: "two",
    3: "three"
}

list1 = [1, 3, 5, 7, 9]
list2 = [2, 4, 6, 8, 10]

test_object = zip(list1, list2)

yaml_object = yaml.dump(test)
print(yaml_object)


def validate_yaml(x):
    try:
        yaml.safe_load(x)
        return x
    except:
        sys.exit(f"Failed to validate{x}")

print(validate_yaml(yaml_object))

#### YAML GENERATOR ####

# project_name = input("Enter project name: ")
# build_configuration = input("Enter build configuration: ")

project_name = "enrollment.api"
build_configuration = "release"

variables_dict = {}

variables_dict["projectName"] = project_name
variables_dict["buildConfiguration"] = build_configuration

variables_object = yaml.dump({'Variables': variables_dict}, default_flow_style=False)

print(variables_object)

#####

task_name = "DotNetCoreCLI@2"
display_name = ".NET Restore"
inputs = "inputs"
command = "restore"
projects = "**/*.csproj"
feeds_to_use = "select"
verbosity_restore = "Minimal"

task_dict = {}

task_dict["command"] = command #input("Enter command: ")
task_dict["projects"] = projects #input("Enter projects: ")
task_dict["feedsToUse"] = feeds_to_use #input("Feeds to use: ")
task_dict["verbosityRestore"] = verbosity_restore #input("Enter verbosity for restore: ")


task_object = yaml.dump([{'task': task_name, 'displayName': display_name, 'inputs': task_dict}], default_flow_style=False, sort_keys=False)

print(task_object)

print(yaml.dump({"pool": "AWS"}))


