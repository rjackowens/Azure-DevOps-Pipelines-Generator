import os

class Config(object):
    SECRET_KY = os.environ.get("SECRET_KEY") or "secret_string" # Validate cookies
    SERVER_NAME = "localhost:5000" # local dev environment
