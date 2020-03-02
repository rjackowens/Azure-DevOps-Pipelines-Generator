from flask import Flask

app = Flask(__name__) # template_folder="static/templates"

from src import routes

app.run(host="0.0.0.0", port=80)