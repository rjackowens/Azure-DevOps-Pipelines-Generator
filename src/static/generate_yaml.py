import sys
import yaml
import os
from pathlib import Path
# from ..config import output_file

output_file = "azure-pipelines.yml"

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


class Generate_Base_Resources:
    """Generate base resources for YAML pipeline"""
    def __init__(self, projectName, projectApi, buildConfiguration, yml_trigger_exclusion=False, pool="AWS"):
        self.projectName = projectName
        self.projectApi = projectApi
        self.buildConfiguration = buildConfiguration
        self.yml_trigger_exclusion = yml_trigger_exclusion
        self.pool = pool

        self.create_resources()
        self.create_trigger()
        self.create_pool()
        self.create_variables()
        self.create_steps()

    def create_resources(self):
        """Add remote repository to pipeline"""
        resource_object = {"resources": {"repositories": [{"repository": "remote", "type": "git", "name": "DevOps/CICD.Scripts", "refs": "refs/heads/master"}]}}
        yaml_dumper(resource_object)

    def create_trigger(self, branch="master", yml_trigger_exclusion=False):
        """Specify a branch with CI trigger"""
        trigger_object = {"trigger": {"branches": {"include": [branch]},"paths": {"exclude": ["azure-pipelines.yml"]}}}
        if self.yml_trigger_exclusion:
            trigger_object = {"trigger": {"branches": {"include": [branch]}}}
        yaml_dumper(trigger_object)

    def create_pool(self, pool="AWS"):
        """Agent pool build will run on"""
        self.pool_object = {"pool": self.pool}
        yaml_dumper(self.pool_object)

    def create_variables(self):
        """Build pipeline variables"""
        variables_object = {'variables': {"projectName": self.projectName, "projectApi": self.projectApi, "buildConfiguration": self.buildConfiguration}}
        yaml_dumper(variables_object)

    def create_name(self):
        """Set build pipeline name"""
        name_object = {"name": "$(BuildDefinitionName)_$(Build.BuildId)"}
        yaml_dumper(name_object)

    def create_steps(self):
        """Creates steps keyword"""
        steps_object = "steps:"
        yaml_dumper(steps_object)


class Generate_Dotnet_Pipeline(Generate_Base_Resources):
    """Generate YAML build pipeline for .NET application"""
    def __init__(self, *args, **kwargs):
        # super().__init__("test_project", "**/Enrollment.Api.sln", "Release")
        super().__init__(*args, **kwargs)
        # self.create_base_resources()

        self.create_restore_task()
        self.create_unit_test_task()
        self.create_dotnet_publish_task()
        self.create_publish_artifact_task()

    def create_restore_task(self):
        """Create .NET restore build pipeline task"""
        restore_object = [{'task': "DotNetCoreCLI@2", 'displayName': ".NET Restore", 'inputs': {"command": "restore", "projects": "$(projectApi)", "feedsToUse": "select", "verbosityRestore": "Minimal"}}]
        yaml_dumper(restore_object)

    def create_unit_test_task(self):
        """Create .NET unit test pipeline task"""
        unit_test_object = [{'task': "DotNetCoreCLI@2", 'displayName': "Run Unit Tests", 'inputs': {"command": "test", "projects": "$(projectTest)", "configuration": "$(buildConfiguration)"}}]
        yaml_dumper(unit_test_object)

    def create_dotnet_publish_task(self):
        """Create .NET publish pipeline task"""
        dotnet_publish_object = [{'task': "DotNetCoreCLI@2", 'displayName': ".NET Publish", 'inputs': {"command": "publish", "projects": "$(projectApi)", "configuration": "$(buildConfiguration)", "arguments": "-o Artifacts/$(projectName)", "modifyOutputPath": "true", "zipAfterPublish": "false"}}]
        yaml_dumper(dotnet_publish_object)

    def create_publish_artifact_task(self):
        """Create pipeline artifact publish task"""
        publish_artifact_object = [{'task': "PublishBuildArtifacts@1", 'displayName': "Publish $(projectName) Artifact", 'inputs': {"PathtoPublish": "$(System.DefaultWorkingDirectory)/Artifacts/$(projectName)", "ArtifactName": "drop", "publishLocation": "Container"}}]
        yaml_dumper(publish_artifact_object)


# Generate_Base_Resources("test_project", "**/Enrollment.Api.sln", "Release")
Generate_Dotnet_Pipeline("test_project2", "api_testtt", "debug", yml_trigger_exclusion=True, pool="Local")


