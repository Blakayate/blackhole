# Built-in #
import argparse
import json
import re
import os
############

# Core #
from cve import get_CVE
from scan import get_services
from report import generate_report
from colors import info, error
from subdomains import get_subdomains
import searchsploit as s
from bruteforce import bruteforce
########

# Python file path
FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

# argparse object
args_parser = argparse.ArgumentParser(description="Blackhole : Pentest Toolbox")

# Command line arguments
# Target
args_parser.add_argument(
    'target',
    help="IP address or domain to scan.",
)

# Ports range
args_parser.add_argument(
    '-p', '--ports',
    default=False,
    help="Take a range of ports to scan. (like 1-65535)"
)

# JSON output
args_parser.add_argument(
    '-j', '--json',
    action='store_true',
    default=False,
    help="Output result to blackhole_report.json file."
)

# Bruteforce
args_parser.add_argument(
    '-b', '--bruteforce',
    action='store_true',
    default=False,
    help="Enable Bruteforce if applicable to the target. You will be prompt to enter some additionnals info."
)

# Subdomains enumeration
args_parser.add_argument(
    '-s', '--subdomains',
    action='store_true',
    default=False,
    help="Enumerate subdomains of given target. Must be a domain name."
)
# Verbose
args_parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=False,
    help="Increase output verbosity."
)

# Parse args and create constants
args = args_parser.parse_args()

# args and flags #
TARGET = args.target
JSON_OUTPUT = args.json
VERBOSE = args.verbose
SUBDOMAINS = args.subdomains
BRUTEFORCE = args.bruteforce
PORTS_RANGE = args.ports
##################

if SUBDOMAINS:
    subdomains_list = ''

    # Subdomains, check if target is a domain name
    if re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', TARGET):
        error("Target is an IP adress, can't enumerate subdomains.")
    else:
        subdomains_list = get_subdomains(TARGET, VERBOSE)

services = get_services(TARGET, PORTS_RANGE, VERBOSE)
info('NMAP finished !')

info('Checking for CVEs and exploits...')

bruteforce_services = list()

# Merge CVEs and exploits for each detected service
# Also, detect if SSH or FTP are presents and get respective port
for service in services:
    if service['name'] == 'ssh':
        bruteforce_services.append(['ssh',service['port']])
    elif service['name'] == 'ftp':
        bruteforce_services.append(['ftp',service['port']])
    else:
        SSH_PORT = False
        FTP_PORT = False

    service['cve'] = list()
    # Match services and applicable CVEs.
    cves = get_CVE(service)
    if not cves == 'Not enough enumeration info':
        for cve in cves:

            # Search for available exploits on EDB
            exploits = s.searchsploit_by_cve(cve['id'], VERBOSE)
            cve['exploits'] = exploits

            service['cve'].append(cve)

info("Got CVEs and exploits !")

# BRUTEFORCE #
# Blackhole only support bruteforce for SSH and FTP

if BRUTEFORCE:
    if len(bruteforce_services) >= 0:

        info('Bruteforce is possible. Do you want to proceed ? (Y/N)')
        user_input = input("Y or N ? ")

        if user_input in ['y', 'Y']:
            info('Please provide a username to test')
            username = input("Enter a username : ")

            info("If you have a wordlist to provide, please give filename (must be in same dir) else, using 'wordlist.txt'.")
            wordlist_file = input('Wordlist filename : ')
            if wordlist_file:
                credentials = bruteforce(bruteforce_services, TARGET, username, VERBOSE, wordlist_file)
            else:
                credentials = bruteforce(bruteforce_services, TARGET, username, VERBOSE)
        else:
            info('Bruteforce skipped !')
            credentials = 'No bruteforce data'


# Add TARGET to first index of list
services.insert(0, TARGET)

# Add found credentials
services.append({"bruteforce" : credentials})

# Add subdomains enumeration (if exist)
if SUBDOMAINS:
    if subdomains_list:
        services.append({"subdomains" : subdomains_list})
    else:
        services.append({"subdomains" : 'No subdomains enumeration'})

info('Creating report...')
generate_report(services)

if JSON_OUTPUT:
    json_path = FILE_DIR + "report/blackhole_report.json"

    with open(json_path, "w") as f:
        json.dump(services, f, indent=4)
        info("Output to JSON file !")