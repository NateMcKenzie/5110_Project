#!/bin/sh
tail -n 2 generated/*/log.txt | sed "s/==> generated\/\(.\+\)\/.\+/\1,/" | sed "s/.\+ \([0-9]\+\) .\+/\1,/" | sed 'N;s/\n/ /' | sed 'N;s/\n/ /' | sed 's/\(.\+\), /\1/'
#tail -n 2 generated/*/log.txt | sed "s/.\+ \([0-9]\+\) .\+/\1/" | sed 'N;N;/^$/d;s/\n/ /g;P;D'
