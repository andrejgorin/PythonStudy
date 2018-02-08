# -*- coding: utf-8 -*-

import threading
import getpass
import datetime
from time import sleep
import re
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import argparse

ATTENTION = '''
###############################################
#                                             #
#  There was some problems. See conf_log.log  #
#                                             #
###############################################
'''

parser = argparse.ArgumentParser(description='Bulk config script')
parser.add_argument('-f', action="store", dest="file_hosts", help='File with list of hosts', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', action="store", dest="file_comms", help='File with list of commands')
group.add_argument('-c', nargs='+', dest="commands", help='List of commands')
args = parser.parse_args()

class UnknownBox(Exception):
    def __init__(self, mismatch):
        self.mismatch = mismatch
    def __str__(self):
        return 'Unrecognized device: ' + self.mismatch

def execute_from_file(**kwargs):
    with ConnectHandler(**kwargs) as ssh:
        ssh.enable()
        result = '\n\n' + ssh.find_prompt() + '\n' + ssh.send_config_from_file(args.file_comms)
        print result

def execute_from_commands(**kwargs):
    with ConnectHandler(**kwargs) as ssh:
        ssh.enable()
        for command in args.commands:
            result = '\n\n' + ssh.find_prompt() + '\n' + ssh.send_command(command) 
            print result        
        
def search_vendor(line):
    match = re.search('(ios$|hpc$|cnx$|csb$)', line)
    if match:
        vendor = match.group()
        ven_list = {'ios': 'cisco_ios',
                    'hpc': 'hp_procurve',
                    'cnx': 'cisco_nxos',
                    'csb': 'cisco_s300'}    
        result = ven_list[vendor]    
        return result
    else:
        return 'no vendor'

def get_cred():
    user = raw_input('username: ')
    passw = getpass.getpass()
    enable_pass = getpass.getpass(prompt='Enable password: ')
    return user, passw, enable_pass
    
def conn_process(line):
    try:
        line = line.rstrip()
        box_type = search_vendor(line)
        if box_type != 'no vendor':
            print('Connection to device ' + line)
            device_params = {'device_type': box_type,
                             'ip': line,
                             'username': cred[0],
                             'password': cred[1],
                             'secret': cred[2]}
            if args.file_comms:                 
                execute = execute_from_file(**device_params)
            elif args.commands:
                execute = execute_from_commands(**device_params)
        else:
            raise UnknownBox(line)
    except (NetMikoTimeoutException, NetMikoAuthenticationException, UnknownBox)as oops: 
        error_log = ('='*30+'\n'+str(oops)+' at '+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'\n'+'='*30+'\n') 
        with open('conf_log.log', 'a') as log:
            log.write(error_log)
            if_errors.append(error_log)
                
def conn_multi(function):
    threads = []
    with open(args.file_hosts, 'r') as hosts:
        for line in hosts:
            th = threading.Thread(target = function, args = (line,))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

cred = get_cred()
if_errors = []        
                    
conn_multi(conn_process)       
if if_errors:
    print ATTENTION
