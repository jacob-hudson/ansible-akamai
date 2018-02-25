#!/usr/bin/env python

from ansible.module_utils.basic import *
import json
import requests
import os
try:
    from akamai.edgegrid import EdgeGridAuth
except ImportError:
    print "Attemping to install required library: edgegrid-python using Pip in your System Path"
    print "pip install edgegrid-python"
    os.system("pip install edgegrid-python")
from os.path import expanduser
import re
from urlparse import urljoin


DOCUMENTATION = ''' docs '''
EXAMPLES = ''' examples '''

def extract_creds(section):
    home = expanduser("~")

    host = ""
    client_secret = ""
    client_token = ""
    access_token = ""
    i = -1
    edgerc_file = open(home + '/.edgerc')

    for line in edgerc_file:
        # this is needed to deal with client_secret not getting populated
        if "client_secret" in line:
            if ":" in line:
                tmp = line.split(':')
                client_secret = tmp[1].strip()
            elif re.match(r'...=...', line):
                tmp = line.split('=')
                client_secret = tmp[1].strip()

        # getting the section we want
        if section in line and i == -1:
            i = 10
        elif i >= 10:
            i = i + 1
        else:
            i = -1

        if i == 14:
            break

        if "client_secret" in line:
            if ":" in line:
                tmp = line.split(':')
                client_secret = tmp[1].strip()
            elif re.match(r'...=...', line):
                tmp = line.split('=')
                client_secret = tmp[1].strip()

        if "host" in line:
            if ":" in line:
                tmp = line.split(':')
                host = tmp[1].strip()
            elif re.match(r'...=...', line):
                tmp = line.split('=')
                host = tmp[1].strip()

        if "client_token" in line:
            if ":" in line:
                tmp = line.split(':')
                client_token = tmp[1].strip()
            elif re.match(r'...=...', line):
                tmp = line.split('=')
                client_token = tmp[1].strip()

        if "access_token" in line:
            if ":" in line:
                tmp = line.split(':')
                access_token = tmp[1].strip()
            elif re.match(r'...=...', line):
                tmp = line.split('=')
                access_token = tmp[1].strip()

    return host, client_secret, client_token, access_token

def authenticate(params):
    session = requests.Session()
    host, client_secret, client_token, access_token = extract_creds(params["section"])

     # set the config options
    session.auth = EdgeGridAuth(
        client_token=client_token,
        client_secret=client_secret,
        access_token=access_token
        )

    baseurl = "https://" + host
    endpoint = params["endpoint"]

    if params["method"] == "GET":
        response = session.get(urljoin(baseurl, endpoint))
        if response.status_code != 400 and response.status_code != 404:
            return False, False, response.json()
        else:
            return True, False, response.json()
    elif params["method"] == "POST":
        session.post()
    else: #error
        pass


def main():

    fields = {
        "section": {"required": True, "type": "str"},
        "endpoint": {"required": True, "type": "str"},
        "method": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = authenticate(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)

if __name__ == "__main__":
    main()
