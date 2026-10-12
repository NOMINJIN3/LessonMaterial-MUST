#!/bin/bash
# Exercise 3.9: builds a small, REAL process hierarchy and lists it with `ps -ael`.
# This script is the "session shell"; it starts several children (two of them get their own
# child) and then runs the command required by the exercise:  ps -ael
# Usage: ./session.sh [output_dir]   (default: current directory)
# Output: <output_dir>/ps_ael.txt (the ps -ael listing) and <output_dir>/session_pid.txt (PID of this script)
OUT="${1:-.}"
sleep 300 & P1=$!                 # background command 1
sleep 301 & P2=$!                 # background command 2
sh -c 'sleep 302; true' & P3=$!   # a shell that has its own child
( sleep 303; true ) & P4=$!       # a subshell that has its own child
sleep 0.5
echo "SESSION_SHELL_PID=$$" > "$OUT/session_pid.txt"
ps -ael > "$OUT/ps_ael.txt"       # <- the command required by the exercise
pkill -P "$P3"; pkill -P "$P4"    # clean up: kill the grandchildren (by parent PID) ...
kill "$P1" "$P2" "$P3" "$P4" 2>/dev/null   # ... and the children
wait 2>/dev/null
