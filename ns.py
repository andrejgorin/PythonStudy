#!/usr/bin/env python
# coding: utf-8
import subprocess
import getpass
import time

def tmux(command):
   subprocess.call('tmux %s' % command, shell=True)

log = raw_input("login: ")
password = getpass.getpass()
tmux("kill-session -t ns")
tmux("new-session -d -s ns")
i = 1

with open ("ip.txt", "r") as IP:

   for line in IP:
       output_list = "string"
       tmux("new-window -t %d" % i)
       tmux('select-window -t %d' % i)
       tmux('rename-window "%s"' % line)
       tmux('send-keys "telnet %s"' % line)
       #time.sleep(1)

       while "Username:" not in output_list:
           proc = subprocess.Popen('tmux capture-pane -p -t ns:%d' % i, stdout=subprocess.PIPE, shell=True)
           output = proc.stdout.read()
           output_list = output.split()
       time.sleep(1)
       tmux('send-keys "%s" "Enter"' % log)

       while "Password:" not in output_list:
           proc = subprocess.Popen('tmux capture-pane -p -t ns:%d' % i, stdout=subprocess.PIPE, shell=True)
           output = proc.stdout.read()
           output_list = output.split()

       #time.sleep(1)
       tmux('send-keys "%s" "Enter"' % password)
       i +=1
tmux("attach")