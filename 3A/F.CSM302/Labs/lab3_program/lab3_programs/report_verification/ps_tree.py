#!/usr/bin/env python3
"""
ps_tree.py - build a process tree (like Figure 3.7 of the textbook) from `ps` output.

  ps -ael > ps_ael.txt                      # 1) collect the process information
  python3 ps_tree.py --input ps_ael.txt     # 2) print the tree (ASCII)
  python3 ps_tree.py --input ps_ael.txt --focus 4242 --tikz   # 3) LaTeX/TikZ code

Without --input the script runs `ps -eo pid,ppid,comm` itself.
The tree is built exactly as the textbook describes: every process is attached to
its parent (PPID), starting at the root (PID 1: init / systemd).

Options
  --input FILE   output of `ps -ael` (or `ps -eo pid,ppid,comm`)
  --focus PID    show only the ancestors of PID and all descendants of PID
  --no-kernel    hide kernel threads (children of kthreadd, PID 2)
  --tikz         print TikZ code instead of the ASCII tree
"""
import argparse, subprocess, sys

def read_processes(path):
    text = open(path, encoding="utf-8", errors="replace").read() if path else \
           subprocess.run(["ps", "-eo", "pid,ppid,comm"], capture_output=True, text=True, check=True).stdout
    lines = [l.rstrip("\n") for l in text.splitlines() if l.strip()]
    header = lines[0].split()
    ipid, ippid = header.index("PID"), header.index("PPID")
    icmd = header.index("CMD") if "CMD" in header else header.index("COMMAND")
    procs = {}
    for l in lines[1:]:
        f = l.split(None, len(header) - 1)
        if len(f) < len(header):
            continue
        procs[int(f[ipid])] = (int(f[ippid]), f[icmd].strip())
    return procs

def build(procs, focus=None, no_kernel=False):
    children = {}
    for pid, (ppid, _) in procs.items():
        children.setdefault(ppid, []).append(pid)
    for k in children:
        children[k].sort()
    def is_kernel(pid):
        return pid == 2 or procs[pid][0] == 2
    keep = set(procs)
    if no_kernel:
        keep = {p for p in keep if not is_kernel(p)}
    if focus is not None:
        anc, p = set(), focus
        while p in procs:
            anc.add(p); p = procs[p][0]
        desc, stack = set(), [focus]
        while stack:
            q = stack.pop(); desc.add(q); stack.extend(children.get(q, []))
        keep &= (anc | desc)
    roots = sorted(p for p in keep if procs[p][0] not in keep)
    return children, keep, roots

def ascii_tree(procs, children, keep, roots):
    out = []
    def walk(pid, prefix, last):
        out.append(f"{prefix}{'└── ' if last else '├── '}{procs[pid][1]} ({pid})" if prefix is not None else f"{procs[pid][1]} ({pid})")
        kids = [c for c in children.get(pid, []) if c in keep]
        for i, c in enumerate(kids):
            child_prefix = "" if prefix is None else prefix + ("    " if last else "│   ")
            walk(c, child_prefix, i == len(kids) - 1)
    for r in roots:
        walk(r, None, True)
    return "\n".join(out)

def tex_escape(s):
    for a, b in (("\\", r"\textbackslash{}"), ("_", r"\_"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("$", r"\$"), ("{", r"\{"), ("}", r"\}"), ("~", r"\~{}"), ("^", r"\^{}")):
        s = s.replace(a, b)
    return s

def tikz_tree(procs, children, keep, roots):
    def node(pid, indent):
        sp = "  " * indent
        label = r"\texttt{%s}\\{\scriptsize %d}" % (tex_escape(procs[pid][1]), pid)
        kids = [c for c in children.get(pid, []) if c in keep]
        s = "node[proc] {%s}" % label
        for c in kids:
            s += "\n" + sp + "  child { " + node(c, indent + 1) + " }"
        return s
    body = "\n".join("\\" + node(r, 0) + ";" for r in roots[:1])
    return body

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input"); ap.add_argument("--focus", type=int)
    ap.add_argument("--no-kernel", action="store_true"); ap.add_argument("--tikz", action="store_true")
    a = ap.parse_args()
    procs = read_processes(a.input)
    children, keep, roots = build(procs, a.focus, a.no_kernel)
    if not keep:
        sys.exit("no processes to show")
    print(tikz_tree(procs, children, keep, roots) if a.tikz else ascii_tree(procs, children, keep, roots))
