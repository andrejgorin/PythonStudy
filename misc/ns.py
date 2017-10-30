#!/usr/bin/env python
# coding: utf-8
import subprocess
import getpass 
import time
from sys import argv

def tmux(command):
    subprocess.call('tmux %s' % command, shell=True)

s = argv[1]
log = raw_input("login: ")
password = getpass.getpass()
tmux("kill-session -t ns%s" % s)
tmux("new-session -d -s ns%s" % s)
i = 1

IP = open (("%sip.txt" % s), "r")

for lin in IP:
    output_list = "string"
    tmux("new-window -t %d" % i)
    tmux('select-window -t %d' % i)
    tmux('rename-window "%s"' % lin.replace("-asr", ""))
    tmux('send-keys "telnet %s"' % lin)

    while "Username:" not in output_list:
        proc = subprocess.Popen('tmux capture-pane -p -t ns%s:%d' % (s, i), stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        output_list = output.split()
    tmux('send-keys "%s" "Enter"' % log)

    while "Password:" not in output_list:
        proc = subprocess.Popen('tmux capture-pane -p -t ns%s:%d' % (s, i), stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        output_list = output.split()

    time.sleep(1)
    tmux('send-keys "%s" "Enter"' % password)
    i +=1
tmux('send-keys -t ns%s:0 "./nolout.py %s" "Enter"' % (s, s))
tmux("attach -t ns%s" % s)
IP.close()

