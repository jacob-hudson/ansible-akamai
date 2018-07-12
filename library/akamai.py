#!/usr/bin/env python

from ansible.module_utils.basic import *
import requests, json
try:
    from akamai.edgegrid import EdgeGridAuth, EdgeRc
except ImportError:
    print "Please install `edgegrid-python` using pip"
from os.path import expanduser
from urlparse import urljoin

DOCUMENTATION = ''' docs '''
EXAMPLES = ''' examples '''

def authenticate(params):
    # get home location
    home = expanduser("~")
    filename = "%s/.edgerc" % home

    # extract edgerc properties
    edgerc = EdgeRc(filename)

    # values from ansible 
    endpoint = params["endpoint"]
    section = params["section"]

    # creates baseurl for akamai
    baseurl = 'https://%s' % edgerc.get(section, 'host')

    s = requests.Session()
    s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

    if params["method"] == "GET":
        response = s.get(urljoin(baseurl, endpoint))
        if response.status_code != 400 and response.status_code != 404:
            print response.content
        else:
            print response.content
    elif params["method"] == "POST":

        body = json.loads(params["body"])

        headers = json.loads(params["headers"])

        response = s.post(urljoin(baseurl, endpoint), json=body, headers=headers)
        print response.content
    else:  # error
        pass

def main():

    fields = {
        "section": {"required": True, "type": "str"},
        "endpoint": {"required": True, "type": "str"},
        "method": {"required": True, "type": "str"},
        "body": {"required": False, "type": "str"},
        "headers": {"required": False, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = authenticate(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)


if __name__ == "__main__":
    main()
