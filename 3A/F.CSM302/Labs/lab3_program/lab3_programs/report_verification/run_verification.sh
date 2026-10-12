#!/bin/bash
# Re-runs the experiments behind the "Баталгаажуулалт" (verification) paragraphs of lab3_report.tex.
# Linux, needs: gcc, bash, procps (ps), python3.      Usage: ./run_verification.sh
cd "$(dirname "$0")" || exit 1
TMP=$(mktemp -d)
RPID=""
cleanup() { [ -n "$RPID" ] && kill "$RPID" 2>/dev/null; rm -rf "$TMP"; }
trap cleanup EXIT

for f in fig3_30 fig3_31_count fig3_32_count fig3_33 fig3_34 fig3_35; do
  gcc -Wall -Wextra -o "$TMP/$f" "$f.c" || { echo "compile error in $f.c"; exit 1; }
done

echo "== 3.1   Figure 3.30 (expected: PARENT: value = 5) =="
"$TMP/fig3_30"; echo
echo "== 3.2   Figure 3.31: number of processes (expected 8) =="
"$TMP/fig3_31_count" | wc -l
echo "== 3.11  Figure 3.32: number of processes (expected 16) =="
"$TMP/fig3_32_count" | wc -l

echo "== 3.12  Figure 3.33: execlp() succeeds / fails =="
mkdir "$TMP/dir" && touch "$TMP/dir/a.txt" "$TMP/dir/b.txt"
( cd "$TMP/dir" && echo '$ ./fig3_33' && "$TMP/fig3_33" \
  && echo '$ ./fig3_33 /bin/no_such_program' && "$TMP/fig3_33" /bin/no_such_program )

echo "== 3.13  Figure 3.34: pid values (A=0, B=C=child pid, D=parent pid) =="
"$TMP/fig3_34"
echo "== 3.16  Figure 3.35: LINE X then LINE Y =="
"$TMP/fig3_35"; echo

echo "== 3.14  named pipe (FIFO) between two independent processes =="
mkfifo "$TMP/demo_fifo"
cat "$TMP/demo_fifo" & RPID=$!                       # process 1: reader (blocks until a writer appears)
sleep 0.2
echo "message from an independent writer" > "$TMP/demo_fifo"   # process 2: writer
wait "$RPID"; RPID=""
echo "file type of the FIFO after both processes finished ('p' = FIFO): $(ls -l "$TMP/demo_fifo" | cut -c1)"

echo "== 3.9   process tree built from  ps -ael  (see ps_tree.py) =="
./session.sh "$TMP" 2>/dev/null
SPID=$(sed 's/.*=//' "$TMP/session_pid.txt")
python3 ps_tree.py --input "$TMP/ps_ael.txt" --focus "$SPID" --no-kernel

Z=../p3_18_zombie/zombie
if [ -x "$Z" ]; then
  echo "== 3.10  a zombie whose parent dies is adopted (PPID changes) and later reaped =="
  "$Z" >/dev/null 2>&1 & ZP=$!
  sleep 1
  CP=$(ps -o pid= --ppid "$ZP" | tr -d ' ')
  ps -o pid,ppid,stat,comm -p "$ZP,$CP"                    # child is Z (zombie)
  kill -9 "$ZP"; wait "$ZP" 2>/dev/null; sleep 0.3
  echo "-- 0.3 s after the parent was killed (new PPID = PID 1 or a 'subreaper'):"
  ps -o pid,ppid,stat,comm -p "$CP"
  sleep 2.5
  echo "-- 2.8 s later (only the header = the zombie was reaped):"
  ps -o pid,ppid,stat,comm -p "$CP"
else
  echo "(3.10 demo skipped: run 'make' in the parent directory first to build p3_18_zombie/zombie)"
fi

exit 0
