Programs and scripts used for the "Баталгаажуулалт" (verification) parts of the report
(Practice Exercises 3.1 - 3.17).  Everything here is only for the report, NOT one of the
numbered Programming Problems 3.18 - 3.27.

Quick way to reproduce everything (Linux):   ./run_verification.sh
(run `make` in the parent directory first if you also want the 3.10 zombie demo)

  fig3_30.c        3.1   Figure 3.30 as printed in the book (+ <sys/wait.h>)
  fig3_30_debug.c  3.1   same, but the child also prints the value and its address
  fig3_31_count.c  3.2   Figure 3.31 with one printf per process        -> 8 lines = 8 processes
  fig3_32_count.c  3.11  Figure 3.32 with one printf per process        -> 16 lines = 16 processes
  fig3_33.c        3.12  Figure 3.33 (+ <sys/wait.h>); DEMO ONLY: the program to exec is read from
                         argv[1] (default /bin/ls) and the printf calls end with a newline, so that
                         both cases can be shown:   ./fig3_33   and   ./fig3_33 /bin/no_such_program
  fig3_34.c        3.13  Figure 3.34 (+ <sys/wait.h>), newline added to every printf
  fig3_35.c        3.16  Figure 3.35 exactly as printed (+ <sys/wait.h>)

  session.sh       3.9   starts a small process hierarchy and runs `ps -ael` (writes ps_ael.txt)
  ps_tree.py       3.9   builds the process tree (ASCII or TikZ) from `ps -ael` output by linking
                         every process to its parent (PPID), exactly as the textbook describes.
                         To build the tree on YOUR OWN machine:
                             ps -ael > ps_ael.txt
                             python3 ps_tree.py --input ps_ael.txt --focus <PID of your shell> --no-kernel
                         (add --tikz to get LaTeX code; without --input it runs ps itself)

Notes
  * 3.10: on a normal desktop Linux an orphan is adopted by PID 1 (systemd) or by the nearest
    "subreaper" (for example `systemd --user`), so the new PPID printed by run_verification.sh
    may differ from 1.  The PIDs in your output will of course differ from those in the report.
  * Written for Linux (procps-ng `ps`).  On macOS the gcc programs work, but `ps --ppid` does not.
