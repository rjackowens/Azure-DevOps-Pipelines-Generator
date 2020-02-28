def make_request(*args, **kwargs):
    """Sends HTTP requests to Azure DevOps API"""
    url = organization_url + "".join(args)
    if kwargs.get("is_release"):
        url = release_url + "".join(args)

    if kwargs.get("request_method") == "get":
        handler = requests.get
    elif kwargs.get("request_method") == "post":
        handler = requests.post
    elif kwargs.get("request_method") == "put":
        handler = requests.put
    elif kwargs.get("request_method") == "delete":
        handler = requests.delete
    else:
        log.error("No requests method selected")
        raise LookupError
    response = handler(url, auth=(username, PAT), verify=False, data=kwargs.get("data"), headers=kwargs.get("headers"))
    return response.json()
