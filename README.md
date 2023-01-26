# ansible-akamai
Ansible module for working with Akamai OPEN APIs

# Prerequisites
- Python 3+
- [Edgegrid-Python](https://github.com/akamai/AkamaiOPEN-edgegrid-python) (install with `pip install edgegrid-python`).

# Install
- Drop `akamai.py` into `./library` in any Ansible playbook, then invoke it like any standard module

# Credentials
- Akamai OPEN credentials are required to use this module.  A reference to get the credentials can be found here - [Get Credentials](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials)
- The currently supported method for storing credentials is via an `.edgerc` file; the recommended location to store the file is in the home directory

# Variables
    section: default
Section header of `.edgerc` INI file used for authentication

    endpoint: /papi/v1/search/find-by-value?=
API endpoint to hit

    method: POST
PUT, GET or POST, similar to HTTPie and the Akamai CLI

    body: /my/json_request_file.json
The request body file that needs to used only for POST method.

    headers:
      Content-Type: application/json
      PAPI-Use-Prefixes: true
The request headers that needs to used only for POST method

## Example JSON file for the body
Example path `/my/json_request_file.json` in above `body:` argument:
```
    {
    "propertyName": "my.property.name"
    }
```

# Acknowledgements
- The Akamai Technologies [api-kickstart](https://github.com/akamai/api-kickstart) repository where many other Akamai API examples are available!
- The Akamai API Catalog: https://developer.akamai.com/api/
