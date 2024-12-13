#!/bin/sh
tail -n 2 generated/*/log.txt | sed "s/.\+ \([0-9]\+\) .\+/\1/" | sed 'N;s/\n/ /' | sed 'N;s/\n/ /'
#tail -n 2 generated/*/log.txt | sed "s/.\+ \([0-9]\+\) .\+/\1/" | sed 'N;N;/^$/d;s/\n/ /g;P;D'
