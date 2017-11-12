#!/usr/bin/env python

from ansible.module_utils.basic import *
import json
import os
try:
    from akamai.edgegrid import EdgeGridAuth
except ImportError:
    print "Attemping to install required library: edgegrid-python"
    print "pip install edgegrid-python"
    os.system("pip install edgegrid-python")

DOCUMENTATION = ''' docs '''
EXAMPLES = ''' examples '''

def main():

    fields = {
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = open_json(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)

if __name__ == "__main__":
    main()
