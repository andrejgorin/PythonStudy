#!/usr/bin/env python

import re
arg = []
z = 0
file = open('output.txt', 'w')
with open('input.txt', 'r') as input:
    for line in input:
        match = re.search("%.+%", line)
        if match:
            arg.append(input("Please enter arg: "))
            mod_line = line.replace(match.group(), arg[z])
            z = z + 1
            file.write(mod_line)
        else:
            file.write(line)
file.close()
