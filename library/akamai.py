#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides authentication using local `.edgerc` files for Akamai API calls.
Note this replaces the ansible.builtin.uri module which will not do
Akamai authentication with `.edgerc` files.
"""

# Copyright: (c) 2018, Jacob Hudson <jacob.alan.hudson@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json

from urllib.parse import urljoin
from os.path import expanduser

import requests

try:
    from akamai.edgegrid import EdgeGridAuth, EdgeRc
except ImportError:
    print("Please install `edgegrid-python` using pip")

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: ansible-akamai
short_description: Ansible module for working with Akamai OPEN APIs
description:
    - Ansible Module for working with Akamai OPEN APIs
    - Provides .edgerc Akamai API authentication which is not available in ansible.builtin.uri
    - For more information, see https://github.com/akamai/AkamaiOPEN-edgegrid-python
      and https://techdocs.akamai.com/home/page/products-tools-a-z?sort=api
author: "Jacob Hudson (@jacob-hudson)"
options:
    section:
        description:
            - Section header of .edgerc ini file.
            - .edgerc file described in more detail at
              https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: null
    endpoint:
        description:
            - Trailing API URI path after the API baseurl in format `https://host`.
            - Needs to include the starting slash.
            - Provides a re-usable and inspecific way to access any Akamai API endpoint.
        required: true
    method:
        description:
            - HTTP method to use for the API request.
            - Provides a re-usable and inspecific way to access any Akamai API endpoint.
        required: true
        default: null
        choices:
          - GET
          - POST
          - PUT
        aliases: []
        version_added: null
    body:
        description:
            - The request body that needs to used only for POST method.
            - This needs to be path to a JSON-formatted file.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: null
    headers:
        description:
            - The request headers that needs to used only for POST method
            - Must be written in sentences.
        required: true
        default:
          - Content-Type: application/json
        choices: []
        aliases: []
        version_added: null
notes:
    - Install the typical way for using an ansible module
    - Easiest install is create a library directory in same directory as your playbook
    - More info: https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html
requirements:
    - Python module edgegrid-python
    - Python 3.x - support for Python 2.x was deprecated
'''

EXAMPLES = r'''
- name: Search Akamai properties to find latest active Production version
  akamai:
    section: papi
    endpoint: /papi/v1/search/find-by-value?=
    method: POST
    body: property_search_body.json
    headers:
      Accept: application/json
      PAPI-Use-Prefixes: adipisicing anim et pariatur
      Content-Type: application/json
'''

RETURN = r'''
'''


def get_request_file(json_file):
    """
    Opens the json file that includes the API call body. For more information
    see https://techdocs.akamai.com/home/page/products-tools-a-z?sort=api
    """
    with open(json_file, mode='r', encoding='utf-8') as json_body:
        body = json.load(json_body)
    return body


def authenticate(params):
    """
    Authenticate and send HTTP request to the Akamai API
    """
    # get home location
    home = expanduser("~")
    filename = f'{home}/.edgerc'

    # extract edgerc properties
    edgerc = EdgeRc(filename)

    # values from ansible
    endpoint = params["endpoint"]
    section = params["section"]

    # capture the host from the specified ini section of edgerc
    edgerc_host = edgerc.get(section, 'host')
    # creates baseurl for akamai
    baseurl = f'https://{edgerc_host}'

    session_request = requests.Session()
    session_request.auth = EdgeGridAuth.from_edgerc(edgerc, section)

    if params["method"] == "GET":
        response = session_request.get(urljoin(baseurl, endpoint))
        if response.status_code not in (400, 404):
            return False, False, response.json()
        return True, False, response.json()
    if params["method"] == "POST":
        body = get_request_file(params["body"])
        headers = {'content-type': 'application/json'}
        response = session_request.post(urljoin(baseurl, endpoint), json=body, headers=headers)
        if response.status_code not in (400, 404):
            return False, True, response.json()
        return True, False, response.json()
    if params["method"] == "PUT":
        body = get_request_file(params["body"])
        headers = {'content-type': 'application/json'}
        response = session_request.put(urljoin(baseurl, endpoint), json=body, headers=headers)
        if response.status_code not in (400, 404):
            return False, True, response.json()
        return True, False, response.json()


def main():  # pylint: disable=missing-function-docstring
    fields = {
        "section": {"required": True, "type": "str"},
        "endpoint": {"required": True, "type": "str"},
        "method": {"required": True, "type": "str"},
        "body": {"required": False, "type": "str"},
        "headers": {"required": False, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = authenticate(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)


if __name__ == "__main__":
    main()
