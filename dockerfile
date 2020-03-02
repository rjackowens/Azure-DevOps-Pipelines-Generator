FROM ubuntu:latest as base

LABEL Maintainer="Jack Owens - owensr@stifel.com"

WORKDIR .

RUN apt-get update -y && install -y python3-pip python3.7

COPY . .

# set FLASK_APP=run.py
RUN export FLASK_APP=src/__init__.py
RUN pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

CMD [ "python3", "run.py"]
