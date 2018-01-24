import pexpect
from time import sleep
import getpass

password = getpass.getpass()

with open('hosts.txt', 'r') as hosts:
    for line in hosts:
        ssh = pexpect.spawn('ssh user@' + line)
        ssh.expect('assword')
        sleep(1)
        ssh.sendline(password)
        ssh.expect('[>#]')
        ssh.sendline('terminal length 0')
        ssh.expect('[>#]')
        ssh.sendline('sh ver')
        ssh.expect('[>#]')
        show_output = ssh.before.decode('utf-8')
        print show_output
        ssh.close
        
        
