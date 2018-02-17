#!/usr/bin/env python

from ansible.module_utils.basic import *
import json
import requests
import os
from config import EdgeGridConfig
from urlparse import urljoin
try:
    from akamai.edgegrid import EdgeGridAuth
except ImportError:
    print "Attemping to install required library: edgegrid-python using Pip in your System Path"
    print "pip install edgegrid-python"
    os.system("pip install edgegrid-python")

DOCUMENTATION = ''' docs '''
EXAMPLES = ''' examples '''

def authenticate(params):

    session = requests.Session()

    config = EdgeGridConfig({},params["section"])

    if hasattr(config, "debug") and config.debug:
	       debug = True

    if hasattr(config, "verbose") and config.verbose:
	       verbose = True

     # set the config options
    session.auth = EdgeGridAuth(
        client_token=config.client_token,
        client_secret=config.client_secret,
        access_token=config.access_token
        )

    baseurl = config.host

    if params["method"] == "GET":
        session.get(urljoin(baseurl, endpoint))
    elif params["method"] == "POST":
        session.post()
    else:
        # error

    return

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
