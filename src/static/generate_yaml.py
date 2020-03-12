import sys
import yaml
import os
from pathlib import Path
from .config import output_file

def yaml_dumper(data, default_flow_style=True):
    """Output YAML object to file"""
    file = "./" + output_file

    try:
        with open(file, mode="a") as f:
            yaml.dump(data, f, sort_keys=False)
            f.write("\n")
    except IOError as e:
        raise Exception(e, "Unable to output YAML file")

def delete_yaml_file():
    """Deletes existing YAML file"""
    if Path(f"./{output_file}").exists():
        try:
            os.remove(f"./{output_file}")
        except IOError as e:
            raise Exception(e, f"Unable to remove {output_file}")

def generate_base_resources(
    projectName, projectApi, buildConfiguration,
    branch="master", yml_trigger_exclusion=False, pool="AWS"):
    """Deletes existing YAML file and generates base resources"""

    resource_object = {
        "resources": {
                "repositories": [
                    {
                        "repository": "remote",
                        "type": "git",
                        "name": "DevOps/CICD.Scripts",
                        "refs": "refs/heads/master"
                    }
                ]
            }
        }
    trigger_object = {
            "trigger": {
                "branches": {
                    "include": [branch
                    ]
                },
                "paths": {
                    "exclude": [
                        "azure-pipelines.yml"
                    ]
                }
            }
        }
    if yml_trigger_exclusion:
        trigger_object = {"trigger": {"branches": {"include": [branch]}}}

    pool_object = {"pool": pool}
    variables_object = {
                'variables': {
                "projectName": projectName,
                "projectApi": projectApi,
                "buildConfiguration": buildConfiguration
            }
        }
    name_object = {"name": "$(BuildDefinitionName)_$(Build.BuildId)"}
    steps_object = "steps:"

    _resource_objects = [
        resource_object,
        trigger_object,
        pool_object,
        variables_object,
        name_object,
        steps_object
    ]

    delete_yaml_file()

    for object in _resource_objects:
        yaml_dumper(object)

def generate_dotnet_pipeline(*args, **kwargs):
    """Generate YAML build pipeline for .NET application"""
    generate_base_resources(*args, **kwargs)
    restore_object = [
        {
                'task': "DotNetCoreCLI@2",
                'displayName': ".NET Restore",
                'inputs': {"command": "restore",
                "projects": "$(projectApi)",
                "feedsToUse": "select",
                "verbosityRestore": "Minimal"
                }
            }
         ]
    unit_test_object = [
                {
                    'task': "DotNetCoreCLI@2",
                    'displayName': "Run Unit Tests",
                    'inputs': {"command": "test", "projects": "$(projectTest)", "configuration": "$(buildConfiguration)"
                    }
                }
            ]
    dotnet_publish_object = [
            {
                'task': "DotNetCoreCLI@2",
                'displayName': ".NET Publish",
                'inputs': {"command": "publish", "projects": "$(projectApi)", "configuration": "$(buildConfiguration)",
                "arguments": "-o Artifacts/$(projectName)",
                "modifyOutputPath": "true",
                "zipAfterPublish": "false"
            }
        }
    ]
    publish_artifact_object = [
                {
                    'task': "PublishBuildArtifacts@1",
                    'displayName': "Publish $(projectName) Artifact",
                    'inputs': {"PathtoPublish": "$(System.DefaultWorkingDirectory)/Artifacts/$(projectName)",
                    "ArtifactName": "drop", "publishLocation": "Container"
                    }
                }
            ]
    for object in restore_object, unit_test_object, dotnet_publish_object, publish_artifact_object:
        yaml_dumper(object)
