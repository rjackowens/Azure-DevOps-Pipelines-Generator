from src import app
from flask import render_template, request
from .static.generate_yaml import Generate_Base_Resources, Generate_Dotnet_Pipeline
from .static.create_repository import create_repository

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        agent_pool = request.form.get("agent-pool-answer")
        project_name = request.form.get("project-name")
        repo_name = request.form.get("repo-name")
        api_name = request.form.get("app-name")
        build_config = request.form.get("build-config-name")

        Generate_Dotnet_Pipeline(repo_name, api_name, build_config, pool=agent_pool)

        create_repository(project_name, repo_name)

    return render_template("form.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
