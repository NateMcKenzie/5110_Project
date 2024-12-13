#!/bin/sh
for file in $(ls levels); do
    python main.py levels/$file generated/$file -q
done
