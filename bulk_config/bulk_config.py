import getpass
from time import sleep
import re
from netmiko import ConnectHandler
import argparse

parser = argparse.ArgumentParser(description='Bulk config script')
parser.add_argument('-f', action="store", dest="file_hosts", help='File with list of hosts', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e', action="store", dest="file_comms", help='File with list of commands')
group.add_argument('-c', nargs='+', dest="commands", help='List of commands')
args = parser.parse_args()
"""print args
for command in args.commands:
    print command"""
def execute_from_file(**device_params):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        result = ssh.send_config_from_file(args.file_comms)
        print result

def execute_from_commands(**device_params):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        for command in args.commands:
            result = ssh.send_command(command)
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

user = raw_input('username: ')
passw = getpass.getpass()
enable_pass = getpass.getpass(prompt='Enable password: ')

with open(args.file_hosts, 'r') as hosts:
    for line in hosts:
        line = line.rstrip()
        box_type = search_vendor(line)
        if box_type != 'no vendor':
            #sleep(0.2)
            print('Connection to device ' + line)
            device_params = {'device_type': box_type,
                             'ip': line,
                             'username': user,
                             'password': passw,
                             'secret': enable_pass}
            if args.file_comms:                 
                execute = execute_from_file(**device_params)
            elif args.commands:
                execute = execute_from_commands(**device_params)
        else:
            print 'Unrecognized device: ' + line
 