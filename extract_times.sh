#!/bin/sh
tail -n 1 generated/*/log.txt | sed "s/.\+ \([0-9]\+\) steps/\1/" | sed 'N;N;/^$/d;s/\n/ /g;P;D'
