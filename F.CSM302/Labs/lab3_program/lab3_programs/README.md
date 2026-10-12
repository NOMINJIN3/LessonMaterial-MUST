# Лаб 3 — Бүлэг 3 «Процесс»: Programming Problems 3.18 – 3.27

Ном: Silberschatz, Galvin, Gagne — *Operating System Concepts*, 10th edition, Chapter 3.

## Шаардлага

Linux / UNIX (Ubuntu г.м.), `gcc`, `make`, JDK (`javac`, `java`). Windows дээр WSL (Ubuntu) ашиглана. macOS дээр Makefile `-lrt`-г зөвхөн Linux дээр ашигладаг (macOS дээр шалгаагүй); `test_all.sh` нь Linux-ийн `ps` синтакс ашигладаг.

```
sudo apt install build-essential default-jdk
```

## Хөрвүүлэх, шалгах

```
make             # бүх C болон Java програмыг хөрвүүлнэ
./test_all.sh    # бүх бодлогын автомат шалгалт (~20 секунд)
./demo.sh        # 1 минутаас богино бичлэгт зориулсан үзүүлэн (SCENE_TIME=6 сек/хэсэг, нийт ≈ 46 сек)
make clean       # хөрвүүлсэн файлуудыг устгана
```

## Бичлэг хийх (≤ 1 минут, өөрийн дуу хоолойгоор)

1. `make` (эсвэл `make java JAVAC=...`) хийж, бүх програмыг **бичлэгээс өмнө** хөрвүүл.
2. Терминалын үсгийг томруулж, дэлгэц болон микрофоны бичлэгээ асаа.
3. `./demo.sh` ажиллуул — 10 бодлогыг 7 хэсэгт дараалан үзүүлнэ. Хэсэг бүр 6 секунд тул тайлбараа тэр хугацаанд хэл.
4. Тайлбарын жишээ текст: `VIDEO_SCRIPT_mn.md`. Өөрийн үгээр хэлбэл илүү зүгээр.

## Бодлого бүр

| № | Бодлого | Файл | Ажиллуулах | Ажиллах зарчим |
|---|---------|------|------------|----------------|
| 3.18 | Zombie процесс | `p3_18_zombie/zombie.c` | `./p3_18_zombie/zombie &` дараа нь `ps -l` | Хүүхэд шууд `exit()` хийнэ, эцэг `wait()` дуудахгүй 15 секунд унтана → хүүхэд `Z` төлөвтэй үлдэнэ. `kill -9 <эцгийн pid>`-ээр устгаж болно. |
| 3.19 | `time` — командын ажилласан хугацаа | `p3_19_time/time_shm.c`, `time_pipe.c` | `./p3_19_time/time_shm ls`, `./p3_19_time/time_pipe ls` | Хүүхэд `exec()`-ийн өмнө `gettimeofday()`-ээр эхлэх цагийг **shared memory** (эхний хувилбар) эсвэл **pipe** (хоёр дахь хувилбар)-ээр эцэгт дамжуулна. Эцэг `wait()`-ийн дараа дуусах цагийг авч зөрүүг хэвлэнэ. |
| 3.20 | PID менежер | `p3_20_pid_manager/pid_manager.c`, `.h`, `pid_test.c` | `./p3_20_pid_manager/pid_test` | 300…5000 хүртэлх PID-ийн боломжтой/завгүй байдлыг **bitmap**-ээр хадгална. `allocate_map()`, `allocate_pid()`, `release_pid()`. |
| 3.21 | Collatz — `fork()` | `p3_21_collatz_fork/collatz_fork.c` | `./p3_21_collatz_fork/collatz_fork 35` | Хүүхэд процесс дарааллыг тооцож хэвлэнэ, эцэг `wait()` хийнэ. Аргументыг эерэг бүхэл тоо эсэхээр шалгана. |
| 3.22 | Collatz — shared memory | `p3_22_collatz_shm/collatz_shm.c` | `./p3_22_collatz_shm/collatz_shm 35` | Эцэг `shm_open`, `ftruncate`, `mmap` хийнэ → хүүхэд дарааллыг shared memory-д бичнэ → эцэг `wait()`-ийн дараа уншиж хэвлээд `shm_unlink` хийнэ. |
| 3.23 | Quote-of-the-day сервер (порт 6017) | `p3_23_quote_server/QuoteServer.java`, `DateClient.java` | `java QuoteServer` ба өөр терминалд `java DateClient 127.0.0.1 6017` | Date сервер (Figure 3.27)-ийг өөрчилсөн: өдрийн дугаараар нэг ASCII үг (<512 тэмдэгт) сонгож илгээнэ. |
| 3.24 | Haiku сервер (порт 5575) | `p3_24_haiku_server/HaikuServer.java`, `DateClient.java` | `java HaikuServer` ба `java DateClient 127.0.0.1 5575` | Холбогдсон клиент бүрт 5-7-5 үет бүхий санамсаргүй нэг haiku илгээнэ. |
| 3.25 | Echo сервер (порт 6007) | `p3_25_echo_server/EchoServer.java`, `EchoClient.java` | `java EchoServer` ба `echo "Hello there!" \| java EchoClient` | `accept()` → `InputStream.read()` → буфер → `OutputStream.write()` давталт. `read()` нь `-1` буцаахад (клиент холболтоо хаахад) давталт дуусна. |
| 3.26 | Том/жижиг үсэг солих (2 pipe) | `p3_26_reverse_case/reverse_case.c` | `./p3_26_reverse_case/reverse_case "Hi There"` | Нэг pipe эцэг→хүүхэд, нөгөө pipe хүүхэд→эцэг. Хүүхэд үсэг бүрийн том/жижгийг сольж буцаана: `Hi There` → `hI tHERE`. |
| 3.27 | `filecopy` (pipe) | `p3_27_filecopy/filecopy.c` | `./p3_27_filecopy/filecopy input.txt copy.txt` | Эцэг эх файлыг уншиж pipe-д бичнэ; хүүхэд pipe-ээс уншиж зорилтот файлд бичнэ. |

## Санамж

* `3.23` – `3.25`-ын серверүүд клиентүүдийг нэг нэгээр нь дараалан үйлчилнэ (thread ашиглаагүй). Бүлэг 4-т thread-ээр сайжруулж болно.
* Серверүүд хэзээ ч өөрөө зогсохгүй — `Ctrl+C`-ээр зогсооно. Порт завгүй бол порт дугаарыг эхний аргументаар өгч болно (`java QuoteServer 7017`).
* Хөрвүүлэлт `-Wall -Wextra` нээлттэй байхад анхааруулгагүй.
* Энэ лабд Programming *Problems* (3.18–3.27) орсон; Programming *Projects* (UNIX Shell, Linux Kernel Module) ороогүй.

## `report_verification/` — тайлангийн «Баталгаажуулалт»

Энэ хавтас нь **тайлангийн** (Practice Exercises 3.1–3.17) баталгаажуулалтын хэсгүүдэд ашигласан жижиг програм, скриптүүд бөгөөд 3.18–3.27 бодлогод хамаарахгүй. Бүгдийг нэг дор давтаж ажиллуулахдаа (Linux): `./report_verification/run_verification.sh` (3.10-ийн зомби жишээ ажиллахын тулд эхлээд `make`). `ps_tree.py` нь `ps -ael`-ийн гаралтаас процессын мод байгуулдаг тул 3.9-ийн модыг **өөрийн компьютер дээрээ** гаргахад ашиглаж болно — дэлгэрэнгүйг `report_verification/README.txt`-ээс үз.
