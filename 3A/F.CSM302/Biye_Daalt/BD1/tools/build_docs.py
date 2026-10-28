#!/usr/bin/env python3
"""
build_docs.py — docs/IV-2-9_BD1_Report.pdf, docs/IV-2-9_Manual.pdf-ийг үүсгэнэ.

Туршилтын бодит үр дүнг (build/test_output.txt, docs/results/*.csv) болон эх кодын
хэсгүүдийг шууд уншиж HTML болгоод, Chromium (playwright)-оор PDF болгоно.
  make && sh tests/run_tests.sh > build/test_output.txt && sh tests/experiments.sh
  python3 tools/build_docs.py
Гишүүдийн мэдээллийг доорх MEMBERS жагсаалтад бөглөнө.
"""
import csv
import html
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(DOCS, "src")

# ---- Багийн мэдээлэл (бөглөнө) ------------------------------------------------
CODE = "IV-2-9"
MEMBERS = [
    ("[Гишүүн 1 нэр]", "[B2xxxxxxx]", "Thread pool цөм (src/threadpool.c), mutex/semaphore"),
    ("[Гишүүн 2 нэр]", "[B2xxxxxxx]", "Туршилтын программ (src/main.c), тест"),
    ("[Гишүүн 3 нэр]", "[B2xxxxxxx]", "Interactive UI, сервер, тайлан"),
]
REPO = "https://github.com/<team>/IV-2-9-threadpool"
DATE = "2026 оны 11-р сар"
REVIEW_TARGET = "II-4-2 (Linux Kernel Module for Task Information)"
REVIEWED_BY = "II-4-6"

e = html.escape


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def csv_rows(name):
    with open(os.path.join(DOCS, "results", name), encoding="utf-8") as f:
        return list(csv.reader(f))


def table(rows, head=True, cls=""):
    h = f'<table class="{cls}">'
    for i, r in enumerate(rows):
        tag = "th" if head and i == 0 else "td"
        h += "<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in r) + "</tr>"
    return h + "</table>"


def code(txt, lang=""):
    return f'<pre class="code">{e(txt.strip())}</pre>'


def snippet(path, start, end):
    s = read(path)
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j].rstrip()


def fig(img, caption, w="100%"):
    return (f'<figure><img src="../img/{img}" style="width:{w}"><figcaption>{caption}</figcaption></figure>')


def env_info():
    def sh(c):
        try:
            return subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()
        except Exception:
            return "?"
    return [
        ["OS", sh("grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'") + ", kernel " + sh("uname -r")],
        ["CPU", sh("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2").strip() + f", {sh('nproc')} core, " + sh("uname -m")],
        ["Compiler", sh("gcc --version | head -1")],
        ["libc / pthread", sh("ldd --version | head -1")],
        ["Python (UI сервер)", sh("python3 --version")],
        ["Браузер (UI, screenshot)", "Chromium 153 (headless, playwright)"],
    ]


# ---- Тестийн бодит гаралтыг задлах ---------------------------------------------
EXPECT = {
    "basic_default": ("Номын анхдагч: 3 worker, queue 10, tests/basic.txt (10 task)", "10 хүлээн авна, 0 татгалзана, нэгэн зэрэг ≤ 3"),
    "burst_reject": ("10 task t=0-д, 2 worker, queue 3, reject", "3..5 хүлээн авч, ≥ 5 татгалзана (номын 'дүүрвэл 1 буцаана')"),
    "burst_retry": ("Дээрхтэй ижил, policy=retry", "10 бүгд хүлээн авагдана, queue ≤ 3"),
    "fifo_one_worker": ("1 worker, tests/fifo.txt", "Task-ууд ирсэн дарааллаараа (FIFO) ажиллана"),
    "long_short_mix": ("1 урт (1500 ms) + 7 богино, 3 worker", "Урт task нэг worker-ийг эзлэхэд бусад нь богинуудыг гүйцэтгэнэ"),
    "random_seeded": ("4 worker, queue 8, 20 санамсаргүй task, seed 7", "20 бүгд хүлээн авагдана"),
    "queue_cap_1": ("Захын: queue 1, 1 worker, 6 task t=0", "≥ 1 татгалзал, queue хэзээ ч 1-ээс хэтрэхгүй"),
    "more_workers": ("Захын: 8 worker, 3 task", "3 task, 5 worker idle хэвээр, зөв зогсоно"),
    "max_workers_64": ("Захын: 64 worker (дээд хязгаар), 64 task", "64 нэгэн зэрэг ажиллаж болно"),
    "single_task": ("Захын: 1 task, 1 ms", "1 хүлээн авч дуусгана"),
    "stress_500": ("Ачаалал: 500 task, 8 worker, queue 16, retry", "500 бүгд яг 1 удаа ажиллана"),
}


def parse_tests():
    txt = read("build/test_output.txt")
    rows, errs = [], []
    blocks = re.findall(r"\[(\w+)\] \./build/threadpool_sim ([^\n]*)\n\s+(accepted=[^\n]*)\n(?:\s+[^\n]*\n)*?\s+(PASS|FAIL) \1", txt)
    for name, args, stats, res in blocks:
        cond, exp = EXPECT.get(name, ("", ""))
        rows.append([f"<b>{name}</b><br><span class='mono small'>{e(args)}</span>", cond, exp,
                     f"<span class='mono small'>{e(stats)}</span>", f"<b class='{res.lower()}'>{res}</b>"])
    for name, msg in re.findall(r"PASS (err_\w+) → ([^\n]*)", txt):
        errs.append([f"<span class='mono'>{name}</span>", f"<span class='small'>{e(msg)}</span>", "<b class='pass'>PASS</b>"])
    total = re.search(r"Нийт: (\d+) PASS, (\d+) FAIL", txt)
    client_ok = "PASS book_client" in txt
    return rows, errs, total.groups() if total else ("?", "?"), client_ok


CSS = """
@page { size: A4; margin: 18mm 17mm 18mm 17mm; }
* { box-sizing: border-box; }
body { font: 10.4pt/1.55 Inter, "DejaVu Sans", sans-serif; color: #1c1d21; margin: 0; }
h1 { font-size: 19pt; margin: 0 0 4mm; letter-spacing: -.2px; }
h2 { font-size: 13.5pt; margin: 8mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 1.5px solid #1c1d21; break-after: avoid; }
h3 { font-size: 11pt; margin: 5mm 0 2mm; break-after: avoid; }
p { margin: 0 0 2.6mm; text-align: justify; }
ul, ol { margin: 0 0 3mm; padding-left: 6mm; } li { margin: .6mm 0; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 9pt; break-inside: auto; }
th, td { border: 1px solid #c9c8c2; padding: 1.4mm 2mm; vertical-align: top; text-align: left; }
th { background: #efeee9; font-weight: 600; }
tr { break-inside: avoid; }
.mono, code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; }
.small { font-size: 8.4pt; }
pre.code { font: 8.1pt/1.42 "DejaVu Sans Mono", monospace; background: #f5f4f0; border: 1px solid #dedcd5; border-left: 3px solid #2f5bd3;
           padding: 2.5mm 3mm; white-space: pre-wrap; margin: 2mm 0 4mm; break-inside: avoid; }
figure { margin: 3mm 0 5mm; break-inside: avoid; text-align: center; }
figure img { border: 1px solid #dedcd5; max-width: 100%; }
figcaption { font-size: 8.8pt; color: #555; margin-top: 1.5mm; }
.pass { color: #1f8a4c; } .fail { color: #c8322b; }
.box { border: 1px solid #c9c8c2; background: #faf9f6; padding: 3mm 4mm; margin: 3mm 0; break-inside: avoid; }
.cover { height: 255mm; display: flex; flex-direction: column; break-after: page; }
.cover .top { font-size: 10pt; color: #555; letter-spacing: .5px; }
.cover .code { display: inline-block; font: 600 13pt "DejaVu Sans Mono", monospace; background: #1c1d21; color: #fff; padding: 1mm 3mm; border-radius: 1mm; margin: 40mm 0 5mm; }
.cover h1 { font-size: 27pt; line-height: 1.15; margin-bottom: 3mm; }
.cover .sub { font-size: 12.5pt; color: #333; }
.cover .meta { margin-top: auto; }
.cover table td:first-child { width: 42mm; font-weight: 600; background: #f5f4f0; }
.toc li { margin: .8mm 0; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.kv td:first-child { width: 45mm; font-weight: 600; background: #f8f7f3; }
.page-break { break-before: page; }
svg text { font-family: Inter, "DejaVu Sans", sans-serif; }
"""


def arch_svg():
    return """<svg viewBox="0 0 680 250" width="100%" xmlns="http://www.w3.org/2000/svg" font-size="11">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#333"/></marker></defs>
<rect x="10" y="20" width="150" height="80" rx="6" fill="#eef2fd" stroke="#2f5bd3"/><text x="85" y="45" text-anchor="middle" font-weight="600">ui/index.html</text><text x="85" y="62" text-anchor="middle">параметр, Run/Reset</text><text x="85" y="78" text-anchor="middle">timeline, playback</text>
<rect x="250" y="20" width="160" height="80" rx="6" fill="#f3f0ff" stroke="#7a5af5"/><text x="330" y="45" text-anchor="middle" font-weight="600">tools/server.py</text><text x="330" y="62" text-anchor="middle">POST /api/run</text><text x="330" y="78" text-anchor="middle">subprocess → бинар</text>
<rect x="500" y="10" width="170" height="230" rx="6" fill="#f5f4f0" stroke="#333"/><text x="585" y="30" text-anchor="middle" font-weight="600">build/threadpool_sim</text>
<rect x="515" y="42" width="140" height="44" rx="4" fill="#fff" stroke="#888"/><text x="585" y="60" text-anchor="middle">main.c (client)</text><text x="585" y="76" text-anchor="middle" font-size="10">task үүсгэх, submit</text>
<rect x="515" y="100" width="140" height="70" rx="4" fill="#fff" stroke="#888"/><text x="585" y="118" text-anchor="middle">threadpool.c</text><text x="585" y="134" text-anchor="middle" font-size="10">queue + qmutex</text><text x="585" y="148" text-anchor="middle" font-size="10">sem work_available</text><text x="585" y="162" text-anchor="middle" font-size="10">N worker thread</text>
<rect x="515" y="184" width="140" height="44" rx="4" fill="#fff" stroke="#888"/><text x="585" y="202" text-anchor="middle">trace + шалгалт</text><text x="585" y="218" text-anchor="middle" font-size="10">JSON → stdout</text>
<line x1="585" y1="86" x2="585" y2="100" stroke="#333" marker-end="url(#a)"/><line x1="585" y1="170" x2="585" y2="184" stroke="#333" marker-end="url(#a)"/>
<line x1="160" y1="50" x2="250" y2="50" stroke="#333" marker-end="url(#a)"/><text x="205" y="44" text-anchor="middle" font-size="10">JSON параметр</text>
<line x1="410" y1="50" x2="515" y2="60" stroke="#333" marker-end="url(#a)"/><text x="460" y="44" text-anchor="middle" font-size="10">-w -q -n -d -a -f</text>
<path d="M515 210 L460 210 L460 85 L410 85" fill="none" stroke="#333" marker-end="url(#a)"/><text x="455" y="160" text-anchor="end" font-size="10">trace JSON</text>
<line x1="250" y1="85" x2="160" y2="85" stroke="#333" marker-end="url(#a)"/><text x="205" y="98" text-anchor="middle" font-size="10">trace + stderr</text>
<rect x="10" y="150" width="150" height="60" rx="6" fill="#fff" stroke="#888" stroke-dasharray="4 3"/><text x="85" y="172" text-anchor="middle" font-weight="600">examples/*.json</text><text x="85" y="190" text-anchor="middle">offline trace ачаалах</text>
<line x1="85" y1="150" x2="85" y2="100" stroke="#333" stroke-dasharray="4 3" marker-end="url(#a)"/>
</svg>"""


def flow_svg():
    return """<svg viewBox="0 0 680 230" width="100%" xmlns="http://www.w3.org/2000/svg" font-size="11">
<defs><marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#333"/></marker></defs>
<rect x="10" y="80" width="120" height="60" rx="6" fill="#fff" stroke="#333"/><text x="70" y="103" text-anchor="middle" font-weight="600">pool_submit()</text><text x="70" y="120" text-anchor="middle" font-size="10">lock → enqueue</text><text x="70" y="133" text-anchor="middle" font-size="10">unlock → sem_post</text>
<rect x="190" y="70" width="230" height="80" rx="6" fill="#f3f0ff" stroke="#7a5af5"/><text x="305" y="64" text-anchor="middle" font-weight="600">Тойрог queue [cap] — qmutex хамгаална</text>
<g font-family="DejaVu Sans Mono" font-size="11"><rect x="205" y="92" width="38" height="36" fill="#7a5af5" opacity=".75"/><text x="224" y="115" text-anchor="middle" fill="#fff">T3</text><rect x="247" y="92" width="38" height="36" fill="#7a5af5" opacity=".75"/><text x="266" y="115" text-anchor="middle" fill="#fff">T4</text><rect x="289" y="92" width="38" height="36" fill="#7a5af5" opacity=".75"/><text x="308" y="115" text-anchor="middle" fill="#fff">T5</text><rect x="331" y="92" width="38" height="36" fill="none" stroke="#aaa" stroke-dasharray="3 2"/><rect x="373" y="92" width="38" height="36" fill="none" stroke="#aaa" stroke-dasharray="3 2"/></g>
<text x="224" y="142" text-anchor="middle" font-size="9">head</text><text x="350" y="142" text-anchor="middle" font-size="9">tail</text>
<line x1="130" y1="110" x2="190" y2="110" stroke="#333" marker-end="url(#b)"/>
<rect x="250" y="175" width="110" height="40" rx="20" fill="#fff6e5" stroke="#b7791f"/><text x="305" y="192" text-anchor="middle" font-weight="600">sem work_available</text><text x="305" y="206" text-anchor="middle" font-size="10">= queue дахь task-ийн тоо</text>
<path d="M70 140 L70 195 L250 195" fill="none" stroke="#b7791f" stroke-dasharray="4 3" marker-end="url(#b)"/><text x="150" y="190" font-size="10" fill="#b7791f">sem_post</text>
<g><rect x="490" y="20" width="180" height="50" rx="6" fill="#eef2fd" stroke="#2f5bd3"/><text x="580" y="40" text-anchor="middle" font-weight="600">worker 0</text><text x="580" y="57" text-anchor="middle" font-size="10">sem_wait → dequeue → execute</text>
<rect x="490" y="85" width="180" height="50" rx="6" fill="#eef2fd" stroke="#2f5bd3"/><text x="580" y="105" text-anchor="middle" font-weight="600">worker 1</text><text x="580" y="122" text-anchor="middle" font-size="10">running T2 (mutex-ээс гадна)</text>
<rect x="490" y="150" width="180" height="50" rx="6" fill="#f5f4f0" stroke="#888"/><text x="580" y="170" text-anchor="middle" font-weight="600">worker N-1</text><text x="580" y="187" text-anchor="middle" font-size="10">idle: sem_wait дээр блоклогдсон</text></g>
<line x1="420" y1="100" x2="490" y2="48" stroke="#333" marker-end="url(#b)"/><text x="455" y="68" font-size="10">dequeue</text>
<path d="M360 195 L470 195 L490 180" fill="none" stroke="#b7791f" stroke-dasharray="4 3" marker-end="url(#b)"/><text x="420" y="212" font-size="10" fill="#b7791f">сэрээнэ</text>
</svg>"""


def report():
    tests, errs, (npass, nfail), client_ok = parse_tests()
    worker_code = snippet("src/threadpool.c", "static void *worker(void *param)", "/* ---------------- API")
    submit_code = snippet("src/threadpool.c", "int pool_submit_id(", "int pool_submit(void")
    shutdown_code = snippet("src/threadpool.c", "void pool_shutdown(void)", "void pool_get_stats")
    exp1, exp2, exp3 = csv_rows("exp1_workers.csv"), csv_rows("exp2_queue.csv"), csv_rows("exp3_policy.csv")
    exp1_t = [["Worker", "Хүлээн авсан", "Makespan, ms", "Дундаж хүлээлт, ms", "Дундаж turnaround, ms", "Ашиглалт, %", "Хурдатгал"]]
    base = float(exp1[1][3])
    for r in exp1[1:]:
        exp1_t.append([r[0], r[1], f"{float(r[3]):.0f}", f"{float(r[4]):.0f}", f"{float(r[5]):.0f}", f"{float(r[6]):.1f}", f"{base/float(r[3]):.2f}×"])
    exp2_t = [["Queue багтаамж", "Хүлээн авсан", "Татгалзсан", "Queue дээд урт", "Makespan, ms"]] + \
             [[r[0], r[1], r[2], r[3], f"{float(r[4]):.0f}"] for r in exp2[1:]]
    exp3_t = [["Policy", "Хүлээн авсан task", "Татгалзсан оролдлого", "Makespan, ms", "Дундаж хүлээлт, ms"]] + \
             [[r[0], r[1], r[2], f"{float(r[3]):.0f}", f"{float(r[4]):.0f}"] for r in exp3[1:]]
    members = table([["Гишүүн", "Оюутны код", "Хариуцсан ажил"]] + [list(m) for m in MEMBERS])

    body = f"""
<section class="cover">
  <div class="top">F.CSM302 ҮЙЛДЛИЙН СИСТЕМ · БИЕ ДААЛТ 1 · СУДАЛГАА, ХЭРЭГЖИЛТ, ТУРШИЛТЫН ТАЙЛАН</div>
  <div><span class="code">{CODE}</span></div>
  <h1>Designing a Thread Pool</h1>
  <div class="sub">Pthreads, POSIX mutex ба semaphore ашигласан thread pool,<br>“Worker activity” interactive дүрслэлийн хамт</div>
  <div class="meta">
    <table class="kv">
      <tr><td>Хичээл</td><td>F.CSM302 Үйлдлийн систем</td></tr>
      <tr><td>Сурах бичиг</td><td>Operating System Concepts (2018), 7-р бүлэг “Synchronization Examples”, Programming Project 1</td></tr>
      <tr><td>Хуваарилалтын код</td><td>{CODE} — IV өдөр, 2-р цаг, 9-р сэдэв</td></tr>
      <tr><td>UI дүрслэл</td><td>Worker activity</td></tr>
      <tr><td>Repository</td><td class="mono">{REPO}</td></tr>
      <tr><td>Шүүмжлэх баг</td><td>{REVIEW_TARGET}</td></tr>
      <tr><td>Огноо</td><td>{DATE}</td></tr>
    </table>
    {members}
  </div>
</section>

<h2>Хураангуй</h2>
<p><b>Асуудал.</b> Хүсэлт бүрт шинэ thread үүсгэх нь үүсгэх/устгах зардалтай. Мөн нэгэн зэрэг ажиллах thread-ийн тоог хязгаарладаггүй. Thread pool нь цөөн тооны worker thread-ийг урьдчилан үүсгэж, ажлыг хуваалцсан queue-ээр дамжуулан хуваарилна. Энэ үед queue руу олон thread зэрэг хандах тул race condition үүсэх аюултай. Мөн ажилгүй worker-уудыг CPU үрэхгүйгээр хүлээлгэх шаардлагатай.</p>
<p><b>Шийдэл.</b> Номын POSIX хувилбарын API-г (<code>pool_init</code>, <code>pool_submit</code>, <code>pool_shutdown</code>) C хэл дээр хэрэгжүүлсэн. Queue нь тойрог массив бөгөөд <code>pthread_mutex</code>-ээр хамгаалагдсан. Worker-ууд <code>sem_wait</code> дээр блоклогдон хүлээж, task орж ирэхэд <code>sem_post</code>-оор сэрнэ. Программ бүх үйл явдлыг микросекундын нарийвчлалтай бүртгэж JSON trace гаргана. Interactive UI нь энэ trace-ээр worker бүрийн idle/running/completed төлөв, queue-ийн дүүргэлт, татгалзлыг хугацааны тэнхлэг дээр алхамчлан харуулна. UI-ийн “Ажиллуулах” товч C программыг бодитоор ажиллуулдаг.</p>
<p><b>Туршилт ба үр дүн.</b> {npass} автомат тест бүгд амжилттай ({nfail} алдаа). Үүнд номын <code>client.c</code> жишээ, үндсэн 6, захын 5, буруу оролтын 17 тест багтана. Тест бүрийн trace-ийг C кодоос хамааралгүй Python шалгагчаар дахин шалгасан. Шалгасан шинжүүд: task бүр яг 1 удаа ажилласан, нэг worker давхар ажил аваагүй, queue FIFO дарааллаар ажилласан, багтаамжаас хэтрээгүй. ThreadSanitizer race condition илрүүлээгүй. 40 task-ийн ачаалалд worker-ийн тоог 1→16 болгоход makespan {float(exp1[1][3]):.0f} ms-ээс {float(exp1[-1][3]):.0f} ms болж буурсан ({base/float(exp1[-1][3]):.1f}× хурдатгал).</p>

<h2>Агуулга</h2>
<ol class="toc"><li>Удиртгал</li><li>Сурах бичгийн шаардлага</li><li>Онолын үндэс</li><li>Системийн зохиомж</li><li>Хэрэгжилт</li><li>Туршилт ба UI дүрслэл</li><li>Туршилтын арга</li><li>Үр дүн</li><li>Хэлэлцүүлэг</li><li>Дүгнэлт</li><li>GitHub дээрх ажиллагаа, AI ашиглалт</li><li>Ашигласан материал · Хавсралт A</li></ol>

<h2>1. Удиртгал</h2>
<p><b>Зорилго.</b> Сурах бичгийн 7-р бүлгийн Programming Project 1-ийн POSIX хувилбарыг бүрэн хэрэгжүүлэх. Worker-ийн тоо, queue-ийн багтаамж, ачааллыг өөрчилж турших боломжтой программ бүтээх. Thread pool-ийн ажиллагааг “Worker activity” дүрслэлээр нотлох.</p>
<p><b>Ач холбогдол.</b> Thread pool нь вэб сервер, өгөгдлийн сан, Java <code>ExecutorService</code>, Linux kernel-ийн <code>workqueue</code> зэрэг олон системийн үндэс юм. Энэ төсөл нь 6–7-р бүлгийн mutex, semaphore, bounded buffer (producer–consumer) ойлголтуудыг бодит программд нэгтгэж харуулна. Pool-д task өгөгч thread нь producer, worker-ууд нь consumer болно.</p>
<p><b>Хамрах хүрээ.</b> Хамарсан: Linux дээрх POSIX хувилбар, номын API, массиваар хэрэгжүүлсэн queue, тохируулах параметр, trace, тест, interactive UI. Хамаараагүй: Java хувилбар (номонд сонголтоор өгсөн), task-ийн priority, worker-ийн тоог динамикаар өөрчлөх.</p>

<h2>2. Сурах бичгийн шаардлага</h2>
<p>Номын Project 1 (P-35…P-38) дахь POSIX хувилбарын шаардлага ба хэрэгжүүлэлтийн харгалзаа:</p>
{table([
    ["#", "Номын шаардлага", "Хэрэгжүүлэлт", "Нотолгоо"],
    ["1", "<code>pool_init()</code> нь thread-үүдийг эхэнд үүсгэж, mutex ба semaphore-ийг эхлүүлнэ", "<code>pool_init()</code> (3 worker, queue 10) ба <code>pool_init_ex(n, cap)</code>", "POOL_INIT, IDLE үйл явдал; book_client тест"],
    ["2", "<code>pool_submit()</code> task struct-ийг <code>enqueue()</code>-ээр queue-д хийнэ; worker <code>dequeue()</code> хийнэ", "<code>task {{function, data, id}}</code>, тойрог массив <code>enqueue/dequeue</code>", "SUBMIT/START, FIFO шалгалт"],
    ["3", "Массив queue дүүрсэн бол 1 буцаана, бусад үед 0", "<code>POOL_FULL=1</code>, <code>POOL_OK=0</code> (+ <code>POOL_ERR=2</code> shutdown-ы дараа)", "burst_reject, queue_cap_1"],
    ["4", "<code>worker()</code> ажил хүлээж, авснаа <code>execute()</code>-ээр ажиллуулна; мэдэгдэлд semaphore", "<code>sem_t work_available</code>; <code>sem_wait</code> → dequeue → <code>execute()</code>", "worker_exclusive шалгалт"],
    ["5", "Queue-д хандахад mutex заавал", "<code>pthread_mutex_t qmutex</code>", "ThreadSanitizer: 0 race"],
    ["6", "<code>pool_shutdown()</code> worker-уудыг зогсоож <code>pthread_join()</code> хийнэ; бүх task дууссаны дараа", "shutdown флаг + N удаа <code>sem_post</code> → үлдсэн task-уудыг гүйцээгээд гарна → <code>pthread_join</code>", "SHUTDOWN → WORKER_EXIT, counts_consistent"],
    ["7", "Номын <code>client.c</code> жишээ ажиллана", "<code>examples/client.c</code> — 5 нийлбэр", f"book_client: {'PASS' if client_ok else 'FAIL'}"],
])}
<p>Хуваарилалтын файлын 9-р сэдвийн хүрэх үр дүн: <i>“Worker-ийн тоо, task queue, ажлын параметрийг өөрчилж, worker бүрийн idle, running, completed төлөвийг хугацааны явцад харуулна.”</i> Үүнийг 6-р хэсэгт тайлбарласан UI хангана.</p>

<h2>3. Онолын үндэс</h2>
<h3>3.1 Thread pool (номын 4.5.1)</h3>
<p>Pool эхлэхдээ тогтмол тооны thread үүсгэнэ. Ирсэн ажил queue-д ордог бөгөөд чөлөөтэй thread түүнийг авч гүйцэтгэнэ. Давуу тал нь гурав. Нэгдүгээрт, байгаа thread-ээр үйлчлэх нь шинэ thread үүсгэхээс хурдан. Хоёрдугаарт, нэгэн зэрэг ажиллах thread-ийн тоо хязгаарлагдмал тул систем хэт ачаалагдахгүй. Гуравдугаарт, ажлыг ажиллуулах механизмаас тусгаарласан тул хуваарилах стратегийг тусад нь өөрчилж болно.</p>
<h3>3.2 Mutex lock (номын 6.5, 7.3.1)</h3>
<p>Queue-ийн <code>head</code>, <code>tail</code>, <code>count</code> хувьсагчдыг хэд хэдэн thread зэрэг өөрчилбөл race condition үүснэ. Жишээлбэл хоёр worker нэг task-ийг зэрэг dequeue хийж болно. <code>pthread_mutex_lock/unlock</code> нь энэ critical section-д нэг удаад нэг л thread орохыг баталгаажуулна.</p>
<h3>3.3 Semaphore (номын 6.6, 7.3.2)</h3>
<p>Тоолдог semaphore-ийн утга нь queue дахь task-ийн тоотой тэнцүү. <code>sem_wait()</code> утга 0 бол thread-ийг <b>блоклоно</b>, өөрөөр хэлбэл busy-wait хийхгүй. Утга 0-ээс их бол утгыг 1-ээр бууруулна. <code>sem_post()</code> утгыг нэмэгдүүлж, хүлээж буй нэг thread-ийг сэрээнэ. Номд unnamed semaphore (<code>sem_init(&amp;sem, 0, 0)</code>) ашиглахыг зөвлөсөн: <code>pshared=0</code> бол зөвхөн нэг процессын thread-үүд хуваалцана.</p>
<h3>3.4 Bounded buffer-тэй холбоо (номын 7.1.1)</h3>
<p>Thread pool-ийн queue бол bounded-buffer бодлогын нэг хэлбэр. Номын шийдэлд <code>empty</code>, <code>full</code>, <code>mutex</code> гэсэн гурван semaphore бий. Thread pool-д <code>full</code>-ийн үүргийг <code>work_available</code> гүйцэтгэнэ. <code>empty</code>-ийн оронд дүүрсэн queue-д producer-ийг блоклохгүйгээр шууд 1 буцаадаг. Энэ нь номын <code>pool_submit()</code>-ийн тодорхойлолт юм. <code>retry</code> горимд client өөрөө хүлээгээд дахин оролдоно.</p>
<h3>3.5 Thread-ийг зогсоох (номын 4.6.3)</h3>
<p>Номд <code>pthread_cancel()</code>-ийг санал болгосон: <code>sem_wait()</code> бол cancellation point. Гэвч deferred cancellation нь task ажиллаж байх үед <code>nanosleep</code> гэх мэт cancellation point дээр thread-ийг таслах боломжтой. Ингэвэл task дутуу үлдэж, түүний барьсан нөөц суллагдахгүй байж болно. Тиймээс бид “хамтран зогсох” (cooperative) аргыг сонгосон. Энэ нь “бүх task дууссаны дараа зогсоно” гэсэн API-ийн тайлбартай нийцнэ (5.4-т дэлгэрэнгүй).</p>

<h2>4. Системийн зохиомж</h2>
<h3>4.1 Компонентууд ба өгөгдлийн урсгал</h3>
<figure>{arch_svg()}<figcaption>Зураг 1. Компонентууд: UI ↔ сервер ↔ C программ. Trace нь дүрслэлийн цорын ганц эх сурвалж.</figcaption></figure>
{table([
    ["Компонент", "Хэл", "Үүрэг"],
    ["<code>src/threadpool.c/.h</code>", "C11, Pthreads", "Thread pool цөм: queue, mutex, semaphore, worker, shutdown, trace бүртгэл"],
    ["<code>src/main.c</code>", "C11", "Туршилтын client: CLI параметр/файл уншиж шалгах, task үүсгэх, хугацаанд нь submit хийх, үр дүнг тооцох, 8 инвариант шалгах, JSON гаргах"],
    ["<code>examples/client.c</code>", "C11", "Номын client.c жишээ — API-г өөрчлөлтгүй ашиглана"],
    ["<code>tools/server.py</code>", "Python 3 stdlib", "UI-ийн параметрийг CLI аргумент болгож бинарыг ажиллуулна; алдааг дамжуулна"],
    ["<code>ui/index.html</code>", "HTML/CSS/JS", "Worker activity дүрслэл, playback, бүртгэл; гадны сангүй, offline горимтой"],
    ["<code>tests/</code>", "sh, Python", "Тестийн өгөгдөл, тест ажиллуулагч, хараат бус trace шалгагч, туршилтын скрипт"],
])}
<h3>4.2 Pool доторх урсгал</h3>
<figure>{flow_svg()}<figcaption>Зураг 2. Submit → queue → semaphore → worker. Task-ийг mutex-ийн гадна ажиллуулдаг тул worker-ууд зэрэгцэн ажиллана.</figcaption></figure>
<h3>4.3 Өгөгдлийн бүтэц</h3>
{code('''typedef struct { void (*function)(void *p); void *data; int id; } task;
static task *queue;  static int qcap, qhead, qtail, qcount;   /* тойрог массив */
static pthread_mutex_t qmutex;          /* queue + тоолуурыг хамгаална */
static sem_t           work_available;  /* queue дахь task-ийн тоо     */
typedef struct { long long t_us; pool_event_type type; int worker, task, qlen; } pool_event;''')}
<h3>4.4 Trace-ийн формат</h3>
<p>Үйл явдал бүр <code>{{t, type, w, task, q}}</code> бүтэцтэй. <code>t</code> нь <code>pool_init</code>-ээс хойшх микросекунд, <code>q</code> нь үйл явдлын дараах queue-ийн урт. Төрлүүд: <code>POOL_INIT, IDLE, SUBMIT, REJECT, START, END, SHUTDOWN, WORKER_EXIT</code>. Цагийг trace-ийн mutex дотор авдаг тул массивын дараалал хугацааны дараалалтай давхцана. <code>SUBMIT</code> ба <code>START</code>-ийг queue-ийн mutex дор бүртгэдэг тул бүртгэсэн <code>q</code> нь бодит queue-ийн урттай яг тэнцүү.</p>

<h2>5. Хэрэгжилт</h2>
<h3>5.1 Хэл, сан, орчин</h3>
<p>Цөм нь C11 дээр бичигдсэн бөгөөд зөвхөн libc ба <code>pthread</code> ашиглана. Build-ийг <code>make</code>, compiler-ийг <code>gcc -std=c11 -Wall -Wextra -O2</code> гүйцэтгэнэ. Сервер нь Python 3-ийн стандарт сантай (<code>http.server</code>, <code>subprocess</code>), UI нь цэвэр JavaScript ба SVG. macOS unnamed semaphore-ийг дэмждэггүй тул тэнд <code>dispatch_semaphore</code>-тэй жижиг wrapper ашиглана. Linux дээр жинхэнэ POSIX <code>sem_init/sem_wait/sem_post</code> ажиллана.</p>
<h3>5.2 Worker функц</h3>
{code(worker_code)}
<p>Гол шийдлүүд: (1) <code>sem_wait</code> нь mutex-ээс <i>гадна</i> байна. Mutex барьсан чигээрээ блоклогдвол бусад thread submit хийж чадахгүй тул deadlock болно. (2) <code>execute()</code>-ийг mutex-ийг суллаад ажиллуулна. Тэгэхгүй бол worker-ууд дараалж ажиллан pool утгагүй болно. (3) <code>sem_wait</code>-ийг <code>EINTR</code>-д давтана.</p>
<h3>5.3 Submit</h3>
{code(submit_code)}
<p><code>sem_post</code>-ийг mutex суллагдсаны дараа дууддаг. Ингэснээр сэрсэн worker тэр даруй mutex-ийг авах боломжтой. Task queue-д орсон тохиолдолд л post хийдэг тул semaphore-ийн утга queue-ийн уртаас хэзээ ч их болохгүй.</p>
<h3>5.4 Shutdown</h3>
{code(shutdown_code)}
<p><b>Зөв байдлын тайлбар.</b> Shutdown-ы өмнө queue-д <i>k</i> task байлаа гэж үзье. Semaphore-ийн утга <i>k + N</i> болно (task тус бүрийн post + worker тус бүрт нэг гарах дохио). Worker queue хоосон байхад л гардаг тул эхний <i>k</i> удаа сэрэхдээ task авна. Үлдсэн <i>N</i> удаагийн сэрэлт нь worker бүрийг нэг удаа гаргана. Тиймээс бүх task гүйцэтгэгдэж, бүх worker гарч, <code>pthread_join</code> блоклогдож үлдэхгүй. <code>counts_consistent</code> шалгалт (submitted = completed) үүнийг тест бүрт нотолсон.</p>
<h3>5.5 Оролтын шалгалт ба алдааны мэдээлэл</h3>
<p>Бүх тоог <code>strtol</code>-оор мөр бүтнээрээ уншдаг. Иймээс “12abc” болон хоосон утгыг хүлээж авахгүй. Хязгаар: worker 1–64, queue 1–4096, task 1–10000, хугацаа 1–60000 ms, ирэх зай 0–60000 ms, MIN ≤ MAX. Task-ийн файлын алдааг <code>файл:мөр</code> байршил, буруу утгын хамт мэдээлнэ. Буруу оролтын үед exit code 2 буцаана. Сервер энэ мэдээллийг UI-ийн улаан хайрцагт дамжуулдаг (Зураг 9, 10).</p>
<h3>5.6 Зөв ажиллагааны дотоод шалгалт</h3>
<p>Ажиллаж дууссаны дараа <code>main.c</code> trace-ээс 8 инвариант шалгана. Task бүр нийлбэр тооцоолдог тул үр дүн нь хүлээгдсэн утгатай тэнцэх ёстой. Мөн task бүрийн ажилласан тоог тусдаа mutex-тэй тоолуураар бүртгэнэ. Инвариантууд: accepted_run_once, results_correct, rejected_not_run, worker_exclusive, concurrency ≤ workers, queue ≤ capacity, start ≥ submit, submitted = completed. Аль нэг нь унавал exit code 4 буцаана.</p>

<h2>6. Туршилт ба UI дүрслэл</h2>
<h3>6.1 Юуг өөрчилж турших вэ</h3>
{table([
    ["Параметр", "UI / CLI", "Ажиглах зүйл"],
    ["Worker-ийн тоо", "Worker thread / <code>-w</code>", "Зэрэгцээ ажиллах lane-ийн тоо, makespan, ашиглалт"],
    ["Queue багтаамж", "Queue багтаамж / <code>-q</code>", "Queue-ийн slot, дүүрэх үеийн REJECT (✕)"],
    ["Дүүрэх үеийн бодлого", "Дүүрэх үед / <code>-p reject|retry</code>, <code>-r</code>", "Татгалзсан task алга болох уу, эсвэл client хүлээгээд дахин оролдох уу"],
    ["Ачаалал", "Task-ийн тоо, хугацаа, ирэх зай, seed / <code>-n -d -a -s</code>", "Queue-ийн урт өсөх/буурах, хүлээлтийн хугацаа"],
    ["Тодорхой сценари", "Task жагсаалт, бэлэн тест / <code>-f</code>", "Burst, FIFO, урт+богино холимог"],
])}
<h3>6.2 UI-ийн элементүүд ба OS ойлголт</h3>
{table([
    ["UI элемент", "Харуулах зүйл", "OS ойлголт"],
    ["Worker lane (timeline)", "Өнгөт bar = task ажиллаж буй хугацаа; судалтай саарал = idle", "Worker <code>sem_wait</code> дээр блоклогдсон / <code>execute()</code>"],
    ["Worker карт", "t агшин дахь төлөв (running Tk / idle / exited), явцын шугам, ✓ дууссан тоо", "idle, running, completed (сэдвийн шаардлага)"],
    ["Queue slot", "Хүлээж буй task-ууд FIFO дарааллаар, багтаамжийн хоосон slot", "Тойрог массив, <code>qcount</code>"],
    ["Queue-ийн урт (step chart)", "Queue хугацааны явцад хэр дүүрсэн", "Semaphore-ийн утга = queue-ийн урт"],
    ["client мөр: | ба ✕", "Submit хийсэн агшин, татгалзсан агшин", "<code>pool_submit()</code> 0 / 1 буцаалт"],
    ["shutdown зураас, хар бүс", "<code>pool_shutdown()</code> дуудагдсан ба worker гарсан агшин", "Cooperative shutdown, <code>pthread_join</code>"],
    ["Үйл явдлын тайлбар", "Тухайн агшны үйл явдлыг API-ийн нэрээр", "sem_post → sem_wait-аас сэрэх → dequeue"],
    ["Playback", "▶/⏸, өмнөх/дараагийн үйл явдал, гулсуур, 0.25×–10× хурд, timeline дээр дарж/чирэх, бүртгэлийн мөр дээр дарах", "Алхамчилж эргэн шалгах"],
])}
<p>Дүрслэл бүхэлдээ C программын trace-ээс зурагддаг. JS симуляци огт байхгүй тул UI дээр харагдах хугацаа, worker-ийн хуваарилалт бүгд бодит ажиллагааных. Нэг параметрээр дахин ажиллуулахад worker-ийн хуваарилалт бага зэрэг өөр гарч болно. Энэ нь OS scheduler-ийн жинхэнэ nondeterminism юм (9-р хэсэг). “Trace хадгалах” товчоор тухайн ажиллуулалтыг JSON болгон хадгалж, дараа нь сервергүйгээр дахин үзэж болно.</p>

<h2>7. Туршилтын арга</h2>
<h3>7.1 Орчин</h3>
{table([["Зүйл", "Утга"]] + env_info(), cls="kv")}
<h3>7.2 Өгөгдөл</h3>
<p>Тестийн өгөгдөл: <code>tests/basic.txt</code> (номын анхдагч 3 worker / queue 10-д тохирох 10 task), <code>burst.txt</code> (10 task нэгэн зэрэг), <code>fifo.txt</code> (дараалал шалгах), <code>mixed_long_short.txt</code> (урт ба богино task), <code>bad_*.txt</code> (5 төрлийн буруу файл). Санамсаргүй ачааллыг seed-ээр тогтоосон тул ижил seed ижил ачаалал үүсгэнэ.</p>
<h3>7.3 Шалгах арга</h3>
<ol>
<li><b>C талын шалгалт</b> — 5.6-д заасан 8 инвариант (<code>VERIFY: OK</code>).</li>
<li><b>Хараат бус шалгагч</b> — <code>tests/verify_trace.py</code> trace-ээс queue-ийн уртыг SUBMIT/START-аар дахин сэргээж, бүртгэсэн <code>q</code>-тэй тулгана. Мөн нэг worker дээрх интервалууд давхцахгүй, START-ийн дараалал SUBMIT-ийн дараалалтай тэнцүү (FIFO), SHUTDOWN-ы дараа SUBMIT байхгүй, worker бүр WORKER_EXIT хийсэн эсэхийг шалгана.</li>
<li><b>Хүлээгдсэн үр дүнгийн нөхцөл</b> (<code>--expect</code>) — тест бүрт хүлээн авсан/татгалзсан тоо, дээд зэрэгцээ.</li>
<li><b>ThreadSanitizer</b> — <code>make tsan</code>: 4 worker, queue 3, 40 task, retry горимд өрсөлдөөнийг ихэсгэсэн ачаалал.</li>
<li><b>Буруу оролт</b> — exit code 2 ба мессежийн агуулгыг шалгана.</li>
</ol>

<h2>8. Үр дүн</h2>
<h3>8.1 Үндсэн ба захын тест</h3>
<p>Тушаал: <code>make test</code>. Нийт <b>{npass} PASS, {nfail} FAIL</b>. Номын <code>client.c</code> жишээ: <b class="pass">{'PASS' if client_ok else 'FAIL'}</b> (5, 10 → 15; 1, 2 → 3; 100, 200 → 300; −7, 7 → 0; 40, 2 → 42). Доорх “Бодит” багана нь сүүлийн ажиллуулалтын гаралт.</p>
{table([["Тест / команд", "Нөхцөл", "Хүлээгдсэн", "Бодит", ""]] + tests)}
<h3>8.2 Буруу оролтын тест</h3>
{table([["Тест", "Программын мэдээлэл (бодит гаралт)", ""]] + errs)}
<p>ThreadSanitizer (<code>make tsan</code>): race condition илрээгүй, <code>VERIFY: OK</code>.</p>

<h3>8.3 Туршилт 1 — worker-ийн тоо ба гүйцэтгэл</h3>
<p>40 task, хугацаа 100–300 ms, бүгд t=0-д ирнэ, queue 64, seed 1 (<code>tests/experiments.sh</code>).</p>
{table(exp1_t)}
<p>Makespan worker-ийн тоонд бараг урвуу пропорциональ буурсан (2 worker → {base/float(exp1[2][3]):.2f}×, 8 worker → {base/float(exp1[4][3]):.2f}×). 16 worker-т ашиглалт {float(exp1[5][6]):.0f}% хүртэл буурсан. 40 task 16 worker-т тэгш хуваагдахгүй тул сүүлийн “давалгаа”-нд зарим worker idle үлддэг.</p>

<h3>8.4 Туршилт 2 — queue-ийн багтаамж ба татгалзал</h3>
<p>2 worker, 20 task t=0-д, тус бүр 100 ms, reject горим.</p>
{table(exp2_t)}
<p>Хүлээн авсан task-ийн тоо багтаамжтай яг тэнцүү гарсан. Client 20 task-ийг микросекундын дотор submit хийдэг бол worker <code>sem_wait</code>-аас сэрж dequeue хийхэд түүнээс урт хугацаа шаардлагатай. Тиймээс burst-ийн үед queue хоосрохоос өмнө дүүрнэ. Энэ нь номын “массив queue дүүрвэл 1 буцаана” гэсэн тодорхойлолтыг шууд харуулна.</p>

<h3>8.5 Туршилт 3 — reject ба retry бодлого</h3>
<p>2 worker, queue 3, 20 task 10 ms зайтай, 100 ms.</p>
{table(exp3_t)}
<p>Reject горимд task алдагдсан ч makespan богино байна. Retry горимд бүх task гүйцэтгэгдсэн боловч client хүлээсэн тул нийт хугацаа уртассан. Сонголт нь хэрэглээнээс хамаарна: ачаалал ихтэй вэб сервер хүсэлтээс татгалздаг бол batch боловсруулалтад retry тохиромжтой.</p>

<h3>8.6 UI дүрслэлийн бодит screenshot</h3>
{fig("01_default_run.png", "Зураг 3. Анхдагч ажиллуулалт (3 worker, queue 5, 15 task). t≈45% агшинд 3 worker бүгд running, queue-д 3 task хүлээж, 2 task татгалзсан (client мөрөн дэх ✕).")}
{fig("03_burst_reject.png", "Зураг 4. Burst + reject (2 worker, queue 3). t=30 ms: T0, T1 ажиллаж, T2 queue-д, 7 task татгалзсан. Shutdown-ы дараа W1 idle болж гарсан (хар бүс).")}
{fig("04_burst_retry.png", "Зураг 5. Ижил burst, retry горим: client дүүрсэн queue-д дахин оролдож (✕ олон), 10 task бүгд гүйцэтгэгдсэн.")}
{fig("05_fifo_step.png", "Зураг 6. 1 worker, FIFO тест — “дараагийн үйл явдал” товчоор алхамчилсан. Queue-д T3, T4, T5 ирсэн дарааллаараа хүлээж байна.")}
{fig("06_long_short.png", "Зураг 7. Урт (T0 = 1500 ms) + богино task: W0 урт task-аар эзлэгдсэн ч W1, W2 богинуудыг гүйцэтгэсээр байна.")}
{fig("07_eight_workers.png", "Зураг 8. 8 worker, queue 16, 60 task — queue-ийн урт ачааллын давалгааг дагаж өсөж буурна.")}
<div class="two">{fig("08_error_workers0.png", "Зураг 9. Worker = 0 — C программын алдааны мэдээлэл UI-д.")}{fig("09_error_file.png", "Зураг 10. Task жагсаалтын 2-р мөрөнд буруу утга.")}</div>
{fig("10_dark_mode.png", "Зураг 11. Харанхуй горим (системийн тохиргоог дагана).")}

<h2>9. Хэлэлцүүлэг</h2>
<h3>9.1 Үр дүнгийн тайлбар</h3>
<ul>
<li><b>Зөв ажиллагаа.</b> Бүх тестэд task бүр яг 1 удаа ажиллаж, нэг worker давхар ажил аваагүй, queue FIFO-оор ажиллаж, багтаамжаас хэтрээгүй. Энэ нь mutex queue-ийн өгөгдлийг хамгаалж, semaphore task-ийн тоог зөв тоолж байгааг харуулна. 500 task-ийн stress тест болон TSan нь өрсөлдөөн ихтэй нөхцөлд ч алдаа гараагүйг нотолсон.</li>
<li><b>Блоклох хүлээлт.</b> Idle worker-ууд <code>sem_wait</code> дээр унтдаг тул CPU үрэхгүй. Timeline-ийн судалтай бүс тэдгээрийн бодит хүлээлт юм.</li>
<li><b>Гүйцэтгэл.</b> Task-ууд sleep хийдэг (I/O-той адил) учраас worker-ийн тоо CPU core-оос (2) олон байсан ч хурдатгал шугаман хэвээр байсан. CPU-д ачаалалтай ажил бол core-ийн тоогоор хязгаарлагдана.</li>
<li><b>Nondeterminism.</b> Ижил параметрээр дахин ажиллуулахад аль worker аль task-ийг авах нь өөрчлөгдөж болно. Хүлээн авсан task-ийн тоо (8.1-ийн burst_reject: 3–5) ч мөн өөрчлөгдөж болно. Энэ нь OS scheduler-ийн шийдвэр бөгөөд тест ийм хэлбэлзлийг тооцож мужаар шалгадаг.</li>
</ul>
<h3>9.2 Хязгаарлалт</h3>
<ul>
<li>Task-ийн ажлыг <code>nanosleep</code>-ээр дуурайлгасан (номын зөвлөмж). Бодит CPU-д ачаалалтай ажилд хурдатгал core-ийн тоогоор хязгаарлагдана.</li>
<li>Trace бүртгэл тусдаа mutex ашигладаг тул маш богино (&lt; 1 ms) task-уудад бага зэргийн нэмэлт зардал үүсгэж, үйл явдлыг цуваа болгодог.</li>
<li>Нэг client thread submit хийдэг. Retry горимд түүний хүлээлт дараагийн task-уудын submit-ийг хойшлуулна.</li>
<li>UI-д нэг ажиллуулалтыг 2000 task, тооцоолсон ~60 секундээр хязгаарласан. CLI 10000 task хүртэл зөвшөөрнө.</li>
<li>Pool нэг процесст нэг ширхэг (номын API глобал төлөвтэй). Олон pool шаардлагатай бол handle-тэй API руу шилжих хэрэгтэй.</li>
<li>macOS-ийн <code>dispatch_semaphore</code> зам CI-д тохируулагдсан боловч бид зөвхөн Linux (Ubuntu 24.04) дээр бүрэн туршсан.</li>
</ul>

<h2>10. Дүгнэлт</h2>
<p>Номын Project 1-ийн POSIX хувилбарыг бүрэн хэрэгжүүлсэн: <code>pool_init</code> thread, mutex, semaphore үүсгэнэ; <code>pool_submit</code> массив queue-д enqueue хийж, дүүрвэл 1 буцаана; worker semaphore дээр хүлээж dequeue → execute хийнэ; <code>pool_shutdown</code> бүх task-ийг гүйцээгээд <code>pthread_join</code> хийнэ. Номын <code>client.c</code> жишээ өөрчлөлтгүй ажилласан.</p>
<p>Нотолсон үр дүн: {npass} тест амжилттай, хараат бус trace шалгагч болон ThreadSanitizer-ээр race condition, давхар гүйцэтгэл, FIFO зөрчил илрээгүй. Worker нэмэхэд гүйцэтгэл бараг шугаман сайжирсан. Queue-ийн багтаамж burst-ийн үед хүлээн авах task-ийн тоог шууд тодорхойлдог. “Worker activity” UI нь бодит trace-ээр worker бүрийн idle/running/completed төлөв, queue, татгалзлыг алхамчлан харуулж, параметрийг өөрчлөн дахин ажиллуулах боломжтой.</p>
<p>Цаашид: task-ийн priority queue, worker-ийн тоог ачааллаар динамикаар өөрчлөх, Java хувилбар (<code>synchronized/wait/notify</code>) хийж харьцуулах.</p>

<h2>11. GitHub дээрх ажиллагаа, AI ашиглалт</h2>
<div class="box">
<p><b>Repository:</b> <span class="mono">{REPO}</span> — README (Quick Start), <code>src/</code>, <code>tests/</code>, <code>examples/</code>, <code>docs/</code> бүтэцтэй. <code>.github/workflows/ci.yml</code> push бүрт build, <code>make test</code>, ThreadSanitizer-ийг автоматаар ажиллуулна. 9-р долоо хоногт <code>v1.0</code> tag/release нийтэлнэ.</p>
<p><b>Багийн ажлын урсгал</b> (бөглөнө): гишүүн бүр өөрийн branch дээр ажиллаж, Pull Request-оор нэгтгэж, нэг нь review хийсэн. Commit-ийн тоо ба гол PR-уудыг Хавсралт A-ийн “Commit/file” баганад бичнэ. GitHub-ийн Insights → Contributors дэлгэцийн зургийг энд хавсаргана.</p>
<p><b>AI ба бэлэн код:</b> Номын API нэр, <code>client.c</code>-ийн бүтэц сурах бичгээс авсан. Код, UI, тест, баримт бичгийн анхны хувилбарыг AI туслахын тусламжтай бэлтгэсэн. Баг бүх кодыг уншиж ойлгосон, ажиллуулсан, тестээр баталгаажуулсан, өөрчилсөн хэсгээ commit-оор тэмдэглэсэн. Гадны сан ашиглаагүй.</p>
</div>

<h2>Ашигласан материал</h2>
<ol>
<li>A. Silberschatz, P. B. Galvin, G. Gagne. <i>Operating System Concepts</i>, 10th ed., Wiley, 2018. Бүлэг 4.5.1 (Thread pools), 4.6.3 (Thread cancellation), 6.5–6.6 (Mutex, Semaphores), 7.1.1 (Bounded buffer), 7.3 (POSIX synchronization), Programming Project 1.</li>
<li>The Open Group. <i>POSIX.1-2017</i>: <code>pthread_create</code>, <code>pthread_join</code>, <code>pthread_mutex_lock</code>, <code>sem_init</code>, <code>sem_wait</code>, <code>sem_post</code>, <code>clock_gettime</code>.</li>
<li>Linux man-pages: <code>sem_overview(7)</code>, <code>pthreads(7)</code>, <code>nanosleep(2)</code>.</li>
<li>Clang/GCC ThreadSanitizer documentation.</li>
<li>Apple Developer Documentation: <code>dispatch_semaphore_create</code>.</li>
<li>F.CSM302 “Бие даалт 1” удирдамж, “Сэдэв ба шүүмжийн хуваарилалт”.</li>
</ol>

<h2 class="page-break">Хавсралт A. Ажлын төлөвлөгөө</h2>
{table([["Талбар", "Мэдээлэл"], ["Хуваарилалтын код", CODE], ["Төсөл", "Designing a Thread Pool (OSC Ch.7, Project 1)"], ["Repository", REPO], ["Хэл/сан/орчин", "C11 + Pthreads, Python 3 stdlib, HTML/JS; Linux (Ubuntu 24.04), gcc 13"], ["Үндсэн дүрслэл", "Worker activity (worker lane timeline + төлөвийн карт + queue)"]], cls="kv")}
{table([["Гишүүн", "Хариуцах ажил", "Commit/file"]] + [[m[0], m[2], "[commit тоо] · " + f] for m, f in zip(MEMBERS, ["src/threadpool.c, threadpool.h", "src/main.c, tests/", "ui/index.html, tools/, docs/"])])}
{table([["Тест", "Оролт/нөхцөл", "Хүлээгдсэн үр дүн"],
        ["1", "<code>./build/client</code> (номын жишээ)", "5 нийлбэр зөв хэвлэгдэнэ"],
        ["2", "<code>-f tests/basic.txt</code> (3 worker, queue 10)", "10/10 хүлээн авч дуусгана, зэрэгцээ ≤ 3"],
        ["3", "<code>-w 2 -q 3 -f tests/burst.txt</code>", "3–5 хүлээн авна, үлдсэнийг татгалзана (1 буцаана)"],
        ["4", "<code>-w 1 -f tests/fifo.txt</code>", "Ирсэн дарааллаар (FIFO)"],
        ["5", "<code>-w 0</code>, <code>-f tests/bad_*.txt</code>", "Exit 2, алдаатай мөр ба утгыг заасан мэдээлэл"]])}
"""
    return body


def manual():
    body = f"""
<section class="cover" style="height:auto;min-height:120mm;break-after:auto">
  <div class="top">F.CSM302 ҮЙЛДЛИЙН СИСТЕМ · БИЕ ДААЛТ 1 · MANUAL</div>
  <div><span class="code" style="margin-top:10mm">{CODE}</span></div>
  <h1>Thread Pool — Worker Activity<br><span style="font-size:15pt;font-weight:500">Хэрэглэгчийн ба operational заавар</span></h1>
  <table class="kv" style="margin-top:6mm">
    <tr><td>Төсөл</td><td>Designing a Thread Pool (OSC Ch.7, Programming Project 1, POSIX)</td></tr>
    <tr><td>Repository</td><td class="mono">{REPO}</td></tr>
    <tr><td>Хувилбар</td><td>v1.0</td></tr>
  </table>
</section>

<h2>Түргэн эхлэл (3 команд)</h2>
{code('''git clone <REPO_URL> && cd IV-2-9-threadpool
make && make test        # → "Нийт: 29 PASS, 0 FAIL"
make ui                  # → браузерт http://localhost:8000''')}

<h1 style="margin-top:8mm">8.1 Хэрэглэгчийн заавар</h1>

<h2>1. Программын зорилго</h2>
<p>Pthreads, mutex, semaphore-оор хэрэгжүүлсэн thread pool-ийг өөр өөр тохиргоогоор ажиллуулж, worker бүрийн <b>idle → running → completed</b> төлөв, task queue-ийн дүүргэлт, татгалзлыг хугацааны тэнхлэг дээр харуулна. UI дээрх бүх дүрслэл C программын бодит ажиллагааны бүртгэлээс (trace) зурагдана.</p>

<h2>2. Дэмжих орчин</h2>
{table([["Зүйл", "Шаардлага"],
        ["OS", "Linux (Ubuntu 20.04+, Debian, Fedora), Windows дээр WSL2. macOS-д build хийх боломжтой (Known issues-ийг үз)"],
        ["Compiler", "gcc ≥ 9 эсвэл clang ≥ 10 (C11, pthread)"],
        ["Build", "GNU make"],
        ["UI", "Python ≥ 3.8 (нэмэлт сан шаардахгүй) + орчин үеийн браузер (Chrome, Firefox, Edge, Safari)"]], cls="kv")}

<h2>3. Суулгах эсвэл нээх алхам</h2>
<ol>
<li>Repository-г татах: <code>git clone &lt;REPO_URL&gt;</code> (эсвэл ZIP татаж задлах).</li>
<li>Хавтас руу орох: <code>cd IV-2-9-threadpool</code>.</li>
<li>Хөрвүүлэх: <code>make</code> → <code>build/threadpool_sim</code>, <code>build/client</code> үүснэ.</li>
<li>UI-г эхлүүлэх: <code>make ui</code> (эсвэл <code>python3 tools/server.py --port 8000</code>).</li>
<li>Браузерт <code>http://localhost:8000</code> нээнэ. Баруун дээд буланд ногоон цэг ба “C программтай холбогдсон” гэж гарвал бэлэн.</li>
</ol>
<div class="box"><b>Сервергүй үзэх:</b> <code>ui/index.html</code>-ийг шууд нээгээд “Trace ачаалах” → <code>examples/sample_trace.json</code>. Энэ горимд “Ажиллуулах” идэвхгүй, хадгалсан trace-ийг л үзнэ.</div>

<h2>4. Оролт ба тохиргоо</h2>
<h3>4.1 UI-ийн талбарууд</h3>
{table([["Талбар", "Утга", "Тайлбар"],
        ["Worker thread", "1–64", "Pool дахь worker thread-ийн тоо"],
        ["Queue багтаамж", "1–4096", "Тойрог массив queue-ийн хэмжээ (номын анхдагч 10)"],
        ["Дүүрэх үед", "reject / retry", "reject: номын дагуу <code>pool_submit</code> 1 буцааж task хаягдана. retry: client “Retry зай” ms хүлээгээд дахин оролдоно"],
        ["Retry зай, ms", "1–10000", "Зөвхөн retry горимд"],
        ["Параметрээр → Task-ийн тоо", "1–2000", "Үүсгэх task-ийн тоо"],
        ["Хугацаа, ms (min–max)", "1–60000", "Task бүрийн ажиллах хугацаа энэ мужаас санамсаргүй"],
        ["Ирэх зай, ms (min–max)", "0–60000", "Дараалсан хоёр task-ийн хоорондох зай; 0 = бүгд зэрэг"],
        ["Seed", "≥ 0", "Ижил seed → ижил ачаалал (дахин давтах боломжтой)"],
        ["Task жагсаалт", "мөр бүр <code>arrival_ms duration_ms</code>", "Тодорхой сценари. <code>#</code>-ээс хойш тайлбар. arrival өсөх дарааллаар. “Бэлэн тест”-ээс сонгож засаж болно"]])}
<h3>4.2 Командын мөрийн сонголтууд</h3>
{code(subprocess.run(["./build/threadpool_sim", "-h"], capture_output=True, text=True, cwd=ROOT).stdout)}

<h2>5. Ажиллуулах, зогсоох, reset хийх</h2>
{table([["Үйлдэл", "UI", "Товчлуур"],
        ["Ажиллуулах", "<b>▶ Ажиллуулах</b> — C программ бодитоор ажиллана (task-уудын нийт хугацаа шиг удна), дараа нь автоматаар тоглуулна", ""],
        ["Тоглуулах / түр зогсоох", "▶ / ⏸", "Space"],
        ["Алхамчлах", "◀︎ өмнөх, ▶︎ дараагийн үйл явдал", "← / →"],
        ["Хугацаанд очих", "Гулсуур, timeline дээр дарах/чирэх, бүртгэлийн мөр дээр дарах", ""],
        ["Хурд", "0.25× … 10× (1× = бодит хугацаа)", ""],
        ["Reset", "⏮ — эхний агшинд буцна; “Анхдагч” — тохиргоог анхны утгад", ""],
        ["Хадгалах / ачаалах", "Trace хадгалах (JSON татна) / Trace ачаалах", ""],
        ["Серверийг зогсоох", "Терминалд <b>Ctrl+C</b>", ""]])}

<h2>6. Дүрслэлийн тэмдэг, өнгө, төлөв</h2>
{fig("02_timeline_default.png", "Worker activity timeline")}
{table([["Тэмдэг", "Утга"],
        ["Өнгөт bar <code>Tk</code> (worker lane)", "Worker тухайн task-ийг <b>running</b> (execute) хийж буй хугацаа. Task бүр өөрийн өнгөтэй, queue-ийн slot-д ч мөн тэр өнгөөр харагдана"],
        ["Судалтай саарал", "<b>idle</b> — worker <code>sem_wait</code> дээр ажил хүлээж байна"],
        ["Хар/бараан бүс", "Worker гарсан (<b>exited</b>) — shutdown-ы дараа"],
        ["Ягаан step chart", "Queue-ийн урт (0 … багтаамж)"],
        ["client мөр: саарал |", "<code>pool_submit</code> амжилттай (0)"],
        ["client мөр: улаан ✕", "Queue дүүрсэн — <code>pool_submit</code> 1 буцаасан (REJECT)"],
        ["Тасархай босоо зураас", "<code>pool_shutdown()</code> дуудагдсан агшин"],
        ["Хар босоо шугам", "Одоогийн агшин (playhead)"],
        ["Worker карт: ● running Tk / ○ idle / ■ exited, ✓ n", "t агшин дахь төлөв ба тухайн worker-ийн дуусгасан task-ийн тоо (completed)"],
        ["VERIFY OK / FAIL", "C программын 8 дотоод шалгалтын дүн"]])}

<h2>7. Жишээ</h2>
<h3>Жишээ 1 — Queue дүүрэх (reject)</h3>
<ol><li>“Task жагсаалт” → Бэлэн тест: <code>burst.txt</code>.</li><li>Worker 2, Queue 3, Дүүрэх үед: reject → ▶ Ажиллуулах.</li><li><b>Хүлээгдэх:</b> 3–5 task хүлээн авагдаж, үлдсэн нь client мөрөнд улаан ✕ болно; “татгалзсан” ≥ 5; makespan ≈ 600 ms.</li></ol>
{fig("03_burst_reject.png", "Жишээ 1-ийн үр дүн", "88%")}
<h3>Жишээ 2 — Retry горим</h3>
<ol><li>Жишээ 1-ийн тохиргоонд “Дүүрэх үед: retry” болгоод ажиллуулна.</li><li><b>Хүлээгдэх:</b> 10/10 хүлээн авагдана, ✕ олон (дахин оролдлого), makespan ≈ 1500 ms.</li></ol>
<h3>Жишээ 3 — Worker-ийн тооны нөлөө</h3>
<ol><li>Параметрээр: Task 40, Хугацаа 100–300, Ирэх зай 0–0, Queue 64, Seed 1.</li><li>Worker 1, 2, 4, 8-аар ээлжлэн ажиллуулж “Makespan” ба “Worker ашиглалт”-ыг харьцуулна.</li><li><b>Хүлээгдэх:</b> makespan ≈ 8.4 с → 4.2 с → 2.2 с → 1.1 с.</li></ol>
<h3>Жишээ 4 — FIFO-г алхамчилж шалгах</h3>
<ol><li>Бэлэн тест <code>fifo.txt</code>, Worker 1 → Ажиллуулах → ⏮.</li><li>→ товчоор алхамчилна. <b>Хүлээгдэх:</b> START-ууд T0, T1, T2… дарааллаар.</li></ol>

<h2>8. Түгээмэл алдаа ба шийдэл</h2>
{table([["Алдаа / шинж тэмдэг", "Шалтгаан", "Шийдэл"],
        ["“offline — зөвхөн trace файл үзэх горим”", "index.html-ийг файлаар нээсэн эсвэл сервер ажиллаагүй", "<code>make ui</code> ажиллуулаад <code>http://localhost:8000</code> нээнэ"],
        ["“build/threadpool_sim алга”", "Хөрвүүлээгүй", "<code>make</code>"],
        ["<code>Address already in use</code>", "8000 порт завгүй", "<code>python3 tools/server.py --port 8080</code>"],
        ["“Алдаа: -w буруу ('0')…”", "Утга хязгаараас гадуур", "Мессежид заасан мужид оруулна"],
        ["“&lt;task жагсаалт&gt;:2 — duration_ms буруу”", "Жагсаалтын 2-р мөрөнд тоо биш утга", "Мөр бүр яг 2 бүхэл тоо"],
        ["“arrival_ms өсөхгүй дарааллаар”", "Ирэх хугацаа эрэмбэгүй", "arrival-аар эрэмбэлнэ"],
        ["“Тооцоолсон хугацаа ~N сек”", "UI-д нэг ажиллуулалт ~60 с-ээр хязгаарлагдсан", "Task/хугацааг багасгах, worker нэмэх эсвэл CLI ашиглах"],
        ["Ижил тохиргоо өөр timeline гаргах", "OS scheduler-ийн жам ёсны nondeterminism", "Алдаа биш. “Trace хадгалах”-аар тодорхой ажиллуулалтыг хадгална"]])}

<h1 class="page-break">8.2 Operational заавар</h1>

<h2>1. Repository clone хийх</h2>
{code('''git clone <REPO_URL>
cd IV-2-9-threadpool
git checkout v1.0          # 9-р долоо хоногт нийтэлсэн хувилбар''')}

<h2>2. OS, compiler/runtime, version</h2>
{table([["Зүйл", "Туршсан хувилбар", "Хамгийн бага"]] + [[r[0], r[1], m] for r, m in zip(env_info(), ["", "x86_64 / arm64", "gcc 9 / clang 10", "glibc 2.31", "Python 3.8", "Орчин үеийн браузер"])])}

<h2>3. Dependency суулгах</h2>
{code('''# Ubuntu / Debian / WSL2
sudo apt update && sudo apt install -y build-essential python3
# Fedora
sudo dnf install -y gcc make python3
# macOS
xcode-select --install''')}
<p>Python-д нэмэлт pip сан, UI-д CDN шаардахгүй.</p>

<h2>4. Build ба Run команд</h2>
{table([["Команд", "Үйлдэл"],
        ["<code>make</code>", "<code>build/threadpool_sim</code>, <code>build/client</code> хөрвүүлнэ"],
        ["<code>make run</code>", "3 worker, queue 5, 15 task; trace → <code>build/trace.json</code>"],
        ["<code>make client</code>", "Номын client.c жишээ"],
        ["<code>make test</code>", "Бүх тест (29)"],
        ["<code>make tsan</code>", "ThreadSanitizer-тэй build + ажиллуулалт"],
        ["<code>make ui</code>", "UI сервер, http://localhost:8000"],
        ["<code>sh tests/experiments.sh</code>", "Тайлангийн туршилтын хүснэгт → <code>docs/results/*.csv</code>"],
        ["<code>python3 tools/build_docs.py</code>", "Report.pdf, Manual.pdf-ийг дахин үүсгэх (playwright шаардлагатай)"],
        ["<code>make clean</code>", "build/ устгана"]])}
<p>Exit code: <b>0</b> — амжилттай, <b>2</b> — буруу оролт, <b>3</b> — ажиллах үеийн алдаа (санах ой, thread үүсгэх), <b>4</b> — дотоод шалгалт унасан.</p>

<h2>5. Үндсэн тестийн өгөгдөл</h2>
{table([["Файл / команд", "Агуулга", "Хүлээгдсэн үр дүн"],
        ["<code>./build/client</code>", "Номын жишээ, 5 хос тоо", "<code>result = 15, 3, 300, 0, 42</code> (дараалал өөр байж болно)"],
        ["<code>-f tests/basic.txt</code>", "10 task, 0–350 ms-д ирнэ", "accepted=10, rejected=0, max_running=3, VERIFY: OK"],
        ["<code>-w 2 -q 3 -f tests/burst.txt</code>", "10 × 300 ms, t=0", "accepted 3–5, rejected 5–7"],
        ["<code>... -p retry</code>", "Дээрхтэй ижил", "accepted=10, makespan ≈ 1500 ms"],
        ["<code>-w 1 -f tests/fifo.txt</code>", "6 task", "START дараалал = T0…T5"],
        ["<code>-w 3 -f tests/mixed_long_short.txt</code>", "1 × 1500 ms + 7 × 100 ms", "accepted=8, бусад worker богинуудыг гүйцэтгэнэ"]])}
<p>Trace-ийг бие даан шалгах: <code>python3 tests/verify_trace.py build/trace.json --expect accepted=15</code>.</p>

<h2>6. Нэмэлт boundary/error test</h2>
{code('''./build/threadpool_sim -w 1 -q 1 -n 6 -d 100 -a 0          # queue 1: татгалзал гарна
./build/threadpool_sim -w 64 -q 64 -n 64 -d 50 -a 0       # дээд 64 worker
./build/threadpool_sim -w 8 -q 16 -n 500 -d 1-3 -a 0 -p retry -r 1   # 500 task stress
./build/threadpool_sim -w 0             # → Алдаа: -w буруу ('0') ..., exit 2
./build/threadpool_sim -d 500-100       # → MIN нь MAX-аас их байж болохгүй
./build/threadpool_sim -f tests/bad_unsorted.txt   # → :2 — arrival_ms өсөхгүй дарааллаар''')}

<h2>7. Хүлээгдсэн үр дүн</h2>
<p><code>make test</code>-ийн төгсгөлд <code>Нийт: 29 PASS, 0 FAIL</code> гарч, exit code 0 буцна. Ажиллуулалт бүрийн stderr-ийн төгсгөлд 8 мөр <code>[ OK ]</code> ба <code>VERIFY: OK</code> хэвлэгдэнэ. Хугацааны утгууд (wait, makespan) машин бүрт хэдэн ms-ээр зөрж болно. Хүлээн авсан/татгалзсан тоо, FIFO дараалал, зэрэгцээний дээд хэмжээ өөрчлөгдөхгүй (burst_reject-ийн 3–5 мужаас бусад).</p>
{code(read("build/test_output.txt").split("== 4.")[0].split("== 2.")[1][:1500].rstrip() + "\n...")}

<h2>8. Known issues</h2>
<ul>
<li><b>macOS:</b> unnamed POSIX semaphore (<code>sem_init</code>) дэмжигддэггүй тул <code>dispatch_semaphore</code> wrapper ашигладаг. Энэ замыг зөвхөн CI-д тохируулсан бөгөөд баг бүрэн туршаагүй.</li>
<li><b>Windows (native):</b> дэмжихгүй. WSL2 ашиглана.</li>
<li><b>Nondeterminism:</b> Worker-ийн хуваарилалт ба burst-ийн үеийн хүлээн авах тоо ажиллуулалт бүрт бага зэрэг өөр гарна (OS scheduler).</li>
<li><b>UI хязгаар:</b> Нэг ажиллуулалт ≤ 2000 task, ≤ ~60 с. Илүүг CLI-ээр ажиллуулж, trace-ийг ачаалж үзнэ (их task-тай trace зурахад браузер удааширч болно).</li>
<li><b>Retry горим:</b> Нэг client thread submit хийдэг тул retry хүлээлт дараагийн task-уудын ирэлтийг хойшлуулна.</li>
<li><b>Маш богино task (&lt; 1 ms):</b> Trace-ийн mutex нэмэлт зардал үүсгэж, хэмжилтэд нөлөөлнө.</li>
<li><b>Сервер:</b> Зөвхөн <code>127.0.0.1</code>-д сонсоно (аюулгүй байдлын үүднээс). Өөр машинаас хандахад <code>--host 0.0.0.0</code>.</li>
</ul>
"""
    return body


def write_html(name, title, body):
    os.makedirs(SRC, exist_ok=True)
    path = os.path.join(SRC, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html lang="mn"><head><meta charset="utf-8"><title>{e(title)}</title>'
                f'<style>{CSS}</style></head><body>{body}</body></html>')
    return path


def to_pdf(html_path, pdf_path, title):
    from playwright.sync_api import sync_playwright
    footer = (f'<div style="font:8px Inter,sans-serif;color:#777;width:100%;padding:0 17mm;display:flex;justify-content:space-between">'
              f'<span>{e(CODE)} · {e(title)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + html_path)
        pg.wait_for_load_state("networkidle")
        pg.pdf(path=pdf_path, format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=footer,
               margin={"top": "16mm", "bottom": "18mm", "left": "17mm", "right": "17mm"})
        b.close()


def main():
    if not os.path.exists(os.path.join(ROOT, "build/test_output.txt")):
        sys.exit("Эхлээд: make && sh tests/run_tests.sh > build/test_output.txt")
    r = write_html("report.html", "БД1 тайлан", report())
    m = write_html("manual.html", "Manual", manual())
    to_pdf(r, os.path.join(DOCS, f"{CODE}_BD1_Report.pdf"), "Designing a Thread Pool — БД1 тайлан")
    to_pdf(m, os.path.join(DOCS, f"{CODE}_Manual.pdf"), "Thread Pool — Manual")
    print("OK:", f"docs/{CODE}_BD1_Report.pdf", f"docs/{CODE}_Manual.pdf")


if __name__ == "__main__":
    main()
