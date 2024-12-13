#!/bin/sh

for file in $(ls levels); do
    (
        for i in 1 2 3 4 5; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait

        for i in 6 7 8 9 10; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait

        for i in 11 12 13 14 15; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait

        for i in 16 17 18 19 20; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait

        for i in 21 22 23 24 25; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait

        for i in 26 27 28 29 30; do
            python main.py "levels/$file" "generated/${file}_$i" -ql &
        done
        wait
    ) &
done

wait
