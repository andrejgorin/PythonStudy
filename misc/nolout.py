#!/usr/bin/env python
# coding: utf-8
import subprocess 
import time
from sys import argv

def tmux(command):
    subprocess.call('tmux %s' % command, shell=True)
    
s = argv[1]
while 1 > 0:
    i = 1
    a = 0
    print 'nologout.py script is working...'
    IP = open (("%sip.txt" % s), "r")
    tmux_before = []
    for lin in IP:    
        proc = subprocess.Popen('tmux capture-pane -p -t ns%s:%d' % (s, i), stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        output_list = output.split()
        tmux_before.append(output_list)        
        i +=1
        a +=1
    #print tmux_before[4]    
    IP.close()
    time.sleep(600)
    i = 1
    a = 0
    IP = open (("%sip.txt" % s), "r")
    tmux_after= []
    #print '##############################################################'
    for lin in IP:
        proc = subprocess.Popen('tmux capture-pane -p -t ns%s:%d' % (s, i), stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        output_list = output.split()
        tmux_after.append(output_list)
        if tmux_before[a] == tmux_after[a]:
            tmux('send-keys -t ns%s:%d "/"' % (s, i))
            tmux('send-keys -t ns%s:%d "BSpace"' % (s, i))
            i +=1
            a +=1
    #print tmux_after[4]
    #time.sleep(6)
    IP.close()
