#!/usr/bin/env bash
# Helper for the 1-minute screen recording (Lab 3, Programming Problems).
#
#   1. Build once BEFORE you start recording:   make
#   2. Start your screen recorder + microphone.
#   3. Run:                                     ./demo.sh
#
# Each scene stays on screen for SCENE_TIME seconds (default 6) so that you
# have time to explain it in your own voice.  7 scenes x 6 s + 4 s intro = 46 s,
# which leaves a safety margin below the 1-minute limit.
# Use e.g.  SCENE_TIME=5 ./demo.sh  to make the video even shorter.
# A suggested narration is in VIDEO_SCRIPT_mn.md.
cd "$(dirname "$0")" || exit 1
SCENE_TIME=${SCENE_TIME:-6}
PIDS=()
trap 'for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done' EXIT

title() { printf '\n\033[1;36m=== %s ===\033[0m\n' "$1"; }
run()   { printf '\033[0;33m$ %s\033[0m\n' "$*"; eval "$*"; }
begin() { title "$1"; T0=$SECONDS; }
end_()  { while (( SECONDS - T0 < SCENE_TIME )); do sleep 0.2; done; }

# servers for 3.23 - 3.25 are started quietly in the background
( cd p3_23_quote_server && exec java QuoteServer >/dev/null 2>&1 ) & PIDS+=("$!")
( cd p3_24_haiku_server && exec java HaikuServer >/dev/null 2>&1 ) & PIDS+=("$!")
( cd p3_25_echo_server  && exec java EchoServer  >/dev/null 2>&1 ) & PIDS+=("$!")
sleep 1.5
clear

T0=$SECONDS; title "Lab 3 - Chapter 3 Processes - Programming Problems"
while (( SECONDS - T0 < 4 )); do sleep 0.2; done

begin "3.18  Zombie process"
./p3_18_zombie/zombie & ZP=$!; disown
sleep 1
run "ps -l | awk 'NR==1 || /zombie/'"
kill -9 $ZP 2>/dev/null
end_

begin "3.19  Elapsed time of a command (shared memory / pipe)"
run "./p3_19_time/time_shm  sleep 1"
run "./p3_19_time/time_pipe sleep 1"
end_

begin "3.20  PID manager (bitmap, pids 300..5000)"
run "./p3_20_pid_manager/pid_test | head -8"
end_

begin "3.21 / 3.22  Collatz: fork  and  shared memory"
run "./p3_21_collatz_fork/collatz_fork 35"
run "./p3_22_collatz_shm/collatz_shm 35"
end_

begin "3.23 / 3.24 / 3.25  Sockets: quote (6017), haiku (5575), echo"
run "java -cp p3_23_quote_server DateClient 127.0.0.1 6017"
run "java -cp p3_24_haiku_server DateClient 127.0.0.1 5575"
run "echo 'Hello there!' | java -cp p3_25_echo_server EchoClient"
end_

begin "3.26  Reverse the case with two pipes"
run "./p3_26_reverse_case/reverse_case 'Hi There'"
end_

begin "3.27  File copy through a pipe"
printf 'Hello from the pipe!\n' > /tmp/input.txt
run "./p3_27_filecopy/filecopy /tmp/input.txt /tmp/copy.txt"
run "cmp /tmp/input.txt /tmp/copy.txt && echo 'files are identical'"
end_
