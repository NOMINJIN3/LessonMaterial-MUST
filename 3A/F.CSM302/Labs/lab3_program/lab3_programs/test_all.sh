#!/usr/bin/env bash
# Regression test for the Chapter 3 programming problems (3.18 - 3.27).
#   ./test_all.sh            (takes about 20 seconds because of the zombie test)
# If "javac" is not installed, run:  JAVAC="java -m jdk.compiler/com.sun.tools.javac.Main" ./test_all.sh
cd "$(dirname "$0")" || exit 1

pass=0; fail=0
PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done; }
trap cleanup EXIT

ok()   { printf 'PASS  %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf 'FAIL  %s\n' "$1"; [ -n "$2" ] && printf '      got: %s\n' "$2"; fail=$((fail+1)); }
expect_eq() { [ "$2" == "$3" ] && ok "$1" || bad "$1" "$2"; }   # desc got want

make -s c java JAVAC="${JAVAC:-javac}" || { echo "build failed"; exit 1; }
echo "build OK"
echo

# ---- 3.18 zombie --------------------------------------------------------
./p3_18_zombie/zombie >/dev/null &
ZP=$!; PIDS+=("$ZP"); disown "$ZP"
sleep 1
st=$(ps -o stat= --ppid "$ZP" | tr -d ' ')
[[ "$st" == Z* ]] && ok "3.18 child is a zombie (state $st) 1 s after start" || bad "3.18 zombie state" "$st"
sleep 10
st=$(ps -o stat= --ppid "$ZP" | tr -d ' ')
[[ "$st" == Z* ]] && ok "3.18 zombie still present after 11 s (>= 10 s)" || bad "3.18 zombie after 11 s" "$st"
kill -9 "$ZP" 2>/dev/null

# ---- 3.19 time ----------------------------------------------------------
for v in time_shm time_pipe; do
    t=$(./p3_19_time/$v sleep 0.3 | sed -n 's/^Elapsed time: //p')
    awk -v t="$t" 'BEGIN{exit !(t >= 0.30 && t < 0.60)}' \
        && ok "3.19 $v sleep 0.3 -> $t s" || bad "3.19 $v" "$t"
done

# ---- 3.20 pid manager ---------------------------------------------------
./p3_20_pid_manager/pid_test >/dev/null && ok "3.20 pid manager self-test" || bad "3.20 pid manager"

# ---- 3.21 / 3.22 Collatz --------------------------------------------------
for v in collatz_fork collatz_shm; do
    d=p3_2$([ $v == collatz_fork ] && echo 1_collatz_fork || echo 2_collatz_shm)
    expect_eq "3.2x $v 8"  "$(./$d/$v 8)"  "8, 4, 2, 1"
    expect_eq "3.2x $v 35" "$(./$d/$v 35)" "35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1"
    for badarg in 0 -4 abc 2.5; do
        ./$d/$v "$badarg" >/dev/null 2>&1 && bad "3.2x $v rejects '$badarg'" "" || ok "3.2x $v rejects '$badarg'"
    done
done
[ ! -e /dev/shm/collatz_shm ] && ok "3.22 shared-memory object removed" || bad "3.22 shm object left behind"

# ---- 3.23 / 3.24 / 3.25 sockets --------------------------------------------
( cd p3_23_quote_server && exec java QuoteServer >/dev/null 2>&1 ) & PIDS+=("$!")
( cd p3_24_haiku_server && exec java HaikuServer >/dev/null 2>&1 ) & PIDS+=("$!")
( cd p3_25_echo_server  && exec java EchoServer  >/dev/null 2>&1 ) & PIDS+=("$!")
sleep 2

q=$(cd p3_23_quote_server && java DateClient 127.0.0.1 6017)
python3 -c "import sys; t=sys.argv[1]; sys.exit(0 if 0 < len(t) < 512 and all(c=='\n' or 32<=ord(c)<127 for c in t) else 1)" "$q" \
    && ok "3.23 quote server (port 6017): printable ASCII, < 512 chars" || bad "3.23 quote server" "$q"

h=$(cd p3_24_haiku_server && java DateClient 127.0.0.1 5575)
n=$(printf '%s\n' "$h" | grep -c .)
[ "$n" -eq 3 ] && ok "3.24 haiku server (port 5575): 3 lines" || bad "3.24 haiku server" "$h"

e=$(echo "Hello there!" | (cd p3_25_echo_server && java EchoClient 127.0.0.1 6007))
expect_eq "3.25 echo server echoes 'Hello there!'" "$e" "echo: Hello there!"

# ---- 3.26 reverse case ------------------------------------------------------
r=$(./p3_26_reverse_case/reverse_case "Hi There" | sed -n 's/^Received: //p')
expect_eq "3.26 'Hi There' -> 'hI tHERE'" "$r" "hI tHERE"

# ---- 3.27 filecopy ------------------------------------------------------------
tmp=$(mktemp -d)
head -c 1000000 /dev/urandom > "$tmp/in.bin"
./p3_27_filecopy/filecopy "$tmp/in.bin" "$tmp/out.bin" >/dev/null && cmp -s "$tmp/in.bin" "$tmp/out.bin" \
    && ok "3.27 filecopy of a 1 MB binary file is identical" || bad "3.27 filecopy"
rm -rf "$tmp"

echo
echo "passed: $pass   failed: $fail"
[ "$fail" -eq 0 ]
