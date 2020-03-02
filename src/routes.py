from src import app
from flask import render_template, request
from .static.generate_yaml import Generate_Base_Resources, Generate_Dotnet_Pipeline

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        agent_pool = request.form.get("agent-pool-answer")
        repo_name = request.form.get("repo-name")
        api_name = request.form.get("app-name")
        build_config = request.form.get("build-config-name")

        Generate_Dotnet_Pipeline(repo_name, api_name, build_config, pool=agent_pool)

    return render_template("form.html")
