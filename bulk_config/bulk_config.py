import getpass
from time import sleep
import re
from netmiko import ConnectHandler

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

with open('hosts.txt', 'r') as hosts:
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
                             
            with ConnectHandler(**device_params) as ssh:
                ssh.enable()
                #result = ssh.send_command(command)
                result = ssh.send_config_from_file('command.txt')
                print(result)
        else:
            print 'Unrecognized device: ' + line
 