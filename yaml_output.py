import sys
import yaml
import os
from pathlib import Path
# from ..config import output_file

output_file = "azure-pipelines.yml"

# resource_object = {"resources": {"repositories": [{"repository": "remote", "type": "git", "name": "DevOps/CICD.Scripts", "refs": "refs/heads/master"}]}}
# trigger_object = {"trigger": {"branches": {"include": ["master"]},"paths": {"exclude": ["azure-pipelines.yml"]}}}
# pool_object = {"pool": "AWS"}
# variables_object = {'variables': {"projectName": "enrollment.api", "projectApi": "**/Enrollment.Api.sln", "buildConfiguration": "Release"}}
# name_object = {"name": "$(BuildDefinitionName)_$(Build.BuildId)"}
# steps_object = "steps:"
# task_object = [{'task': "DotNetCoreCLI@2", 'displayName': ".NET Restore", 'inputs': {"command": "restore", "projects": "**/*.csproj", "feedsToUse": "select", "verbosityRestore": "Minimal"}}]


def yaml_dumper(data, default_flow_style=True):
    """Output YAML object to file"""
    file = "./" + output_file

    try:
        with open(file, mode="a") as f:
            yaml.dump(data, f, sort_keys=False)
            f.write("\n")
    except IOError as e:
        raise Exception(e, "Unable to output YAML file")

if Path("./azure-pipelines.yml").exists():
    try:
        os.remove("./azure-pipelines.yml")
    except IOError as e:
        raise Exception(e, "Unable to remove azure-pipelines.yml")


### TO-DO: YAML GENERATOR CLASS ###
def create_resources():
    """Add remote repository to pipeline"""
    resource_object = {"resources": {"repositories": [{"repository": "remote", "type": "git", "name": "DevOps/CICD.Scripts", "refs": "refs/heads/master"}]}}
    yaml_dumper(resource_object)


def create_trigger(branch="master", yml_exclusion=False):
    """Specify a branch with CI trigger"""
    trigger_object = {"trigger": {"branches": {"include": [branch]},"paths": {"exclude": ["azure-pipelines.yml"]}}}
    if yml_exclusion:
        trigger_object = {"trigger": {"branches": {"include": [branch]}}}
    yaml_dumper(trigger_object)


def create_pool(pool="AWS"):
    """Agent pool build will run on"""
    pool_object = {"pool": pool}
    yaml_dumper(pool_object)


def create_variables():
    """Build pipeline variables"""
    variables_object = {'variables': {"projectName": "enrollment.api", "projectApi": "**/Enrollment.Api.sln", "buildConfiguration": "Release"}}
    yaml_dumper(variables_object)


def create_name():
    """Set build pipeline name"""
    name_object = {"name": "$(BuildDefinitionName)_$(Build.BuildId)"}
    yaml_dumper(name_object)


def create_steps():
    """Creates steps keyword"""
    steps_object = "steps:"
    yaml_dumper(steps_object)


def create_restore_task():
    """Create .NET restore build pipeline task"""
    restore_object = [{'task': "DotNetCoreCLI@2", 'displayName': ".NET Restore", 'inputs': {"command": "restore", "projects": "$(projectApi)", "feedsToUse": "select", "verbosityRestore": "Minimal"}}]
    yaml_dumper(restore_object)


def create_unit_test_task():
    """Create .NET unit test pipeline task"""
    unit_test_object = [{'task': "DotNetCoreCLI@2", 'displayName': "Run Unit Tests", 'inputs': {"command": "test", "projects": "$(projectTest)", "configuration": "$(buildConfiguration)"}}]
    yaml_dumper(unit_test_object)


def create_dotnet_publish_task():
    """Create .NET publish pipeline task"""
    dotnet_publish_object = [{'task': "DotNetCoreCLI@2", 'displayName': ".NET Publish", 'inputs': {"command": "publish", "projects": "$(projectApi)", "configuration": "$(buildConfiguration)", "arguments": "-o Artifacts/$(projectName)", "modifyOutputPath": "true", "zipAfterPublish": "false"}}]
    yaml_dumper(dotnet_publish_object)


def create_publish_artifact_task():
    """Create pipeline artifact publish task"""
    publish_artifact_object = [{'task': "PublishBuildArtifacts@1", 'displayName': "Publish $(projectName) Artifact", 'inputs': {"PathtoPublish": "$(System.DefaultWorkingDirectory)/Artifacts/$(projectName)", "ArtifactName": "drop", "publishLocation": "Container"}}]
    yaml_dumper(publish_artifact_object)


create_resources()
create_trigger()
create_pool()
create_variables()
create_name()
create_steps()
create_restore_task()
create_unit_test_task()
create_dotnet_publish_task()
create_publish_artifact_task()

# yaml_dumper(resource_object)
# yaml_dumper(trigger_object)
# yaml_dumper(pool_object)
# yaml_dumper(variables_object, default_flow_style=False)
# yaml_dumper(name_object)
# yaml_dumper(steps_object)
# yaml_dumper(task_object)
