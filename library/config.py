# Python edgegrid module
""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys, os

if sys.version_info[0] >= 3:
     # python3
     from configparser import ConfigParser
     import http.client as http_client
else:
     # python2.7
     from ConfigParser import ConfigParser
     import httplib as http_client

import argparse
import logging

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description='Process command line options.')
class EdgeGridConfig():

    def __init__(self, config_values, configuration, flags=None):

        parser.add_argument('--verbose', '-v', default=False, action='count')
        parser.add_argument('--debug', '-d', default=False, action='count')
        parser.add_argument('--config_file', '-c', default='~/.edgerc')
        parser.add_argument('--config_section', '-s', action='store')

        if flags:
            for argument in flags.keys():
                parser.add_argument('--' + argument, action=flags[argument])

        arguments = {}
        for argument in config_values:
        	if config_values[argument]:
        		if config_values[argument] == "False" or config_values[argument] == "True":
        			parser.add_argument('--' + argument, action='count')
        		parser.add_argument('--' + argument)
        		arguments[argument] = config_values[argument]
        try:
            args = parser.parse_args()
        except:
            sys.exit()
        arguments = vars(args)

        if arguments['debug']:
            http_client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        if "config_section" in arguments and arguments["config_section"]:
            configuration = arguments["config_section"]
        arguments["config_file"] = os.path.expanduser(arguments["config_file"])
        if os.path.isfile(arguments["config_file"]):
            config = ConfigParser()
            config.readfp(open(arguments["config_file"]))
            if not config.has_section(configuration):
                err_msg = "ERROR: No section named %s was found in your %s file\n" % (configuration, arguments["config_file"])
                err_msg += "ERROR: Please generate credentials for the script functionality\n"
                err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n" % configuration
                sys.exit( err_msg )
            for key, value in config.items(configuration):
            	# ConfigParser lowercases magically
            	if key not in arguments or arguments[key] == None:
            		arguments[key] = value
        else:
            	print ("Missing configuration file.  Run python gen_edgerc.py to get your credentials file set up once you've provisioned credentials in LUNA.")
            	return None

        for option in arguments:
            setattr(self,option,arguments[option])

        self.create_base_url()

    def create_base_url(self):
        self.base_url = "https://%s" % self.host
