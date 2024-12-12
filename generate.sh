#!/bin/sh
for file in $(ls levels); do
    echo $file
    python main.py levels/$file generated/$file -q
done
