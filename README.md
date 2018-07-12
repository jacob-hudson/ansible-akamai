# ansible-akamai
Ansible Module for working with Akamai OPEN APIs

# Prerequisites
- Python 2.7.10+ (NOTE:  This is higher then Ansible, which can run on Python 2.6 - 2.7.9)
- Edgegrid-Python (install with `pip install edgegrid-python`), works with Python 2.7.10+

# Install
- Drop `akamai.py` into `./library` in any Ansible playbook, then invoke it like any standard module

# Credentials
- Akamai OPEN credentials are required to use this module.  A reference to get the credentials can be found here - [Get Credentials](https://developer.akamai.com/introduction/Prov_Creds.htm)

- The currently supported method for storing credentials is via an `.edgerc` file, the recommended location to store the file is in the home directory

# Variables
- `section` - Section of `.edgerc` file
- `endpoint` - API endpoint to hit
- `method` - GET or POST, similar to HTTPie and the Akamai CLI
- `body` - The request body that needs to used only for POST method
    * "productId": "prd_Alta",
    * "propertyName": "my.new.property.com",
- `headers` - The request headers that needs to used only for POST method
    * "Content-Type": "application/json"
    * "PAPI-Use-Prefixes": "true"

# Acknowledgements
- The Akamai Technologies [api-kickstart](https://github.com/akamai/api-kickstart) repository where many other Akamai API examples are available!
- The Akamai API Catalog: https://developer.akamai.com/api/
