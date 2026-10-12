#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_LINE   80
#define HIST_SIZE  10
#define PROMPT     "COMMAND->"

/* Глобал өгөгдөл: дохио боловсруулагч параметр авдаггүй тул глобал байх ёстой */
static char history[HIST_SIZE][MAX_LINE + 1];
static int  hist_count = 0;
static volatile sig_atomic_t fg_running = 0;

/* Дохионд аюулгүй хэвлэх функцууд (printf биш write) */
static void write_str(const char *s)
{
    write(STDOUT_FILENO, s, strlen(s));
}

static void write_int(int n)
{
    char buf[16];
    int i = sizeof(buf);
    buf[--i] = '\0';
    if (n == 0) buf[--i] = '0';
    while (n > 0) {
        buf[--i] = '0' + (n % 10);
        n /= 10;
    }
    write_str(&buf[i]);
}

/* Сүүлийн 10 командыг хэвлэнэ */
static void print_history(void)
{
    int start = hist_count > HIST_SIZE ? hist_count - HIST_SIZE : 0;

    if (hist_count == 0) {
        write_str("No commands in history.\n");
        return;
    }
    for (int i = start; i < hist_count; i++) {
        write_str("  ");
        write_int(i + 1);
        write_str("  ");
        write_str(history[i % HIST_SIZE]);
        write_str("\n");
    }
}

/* Ctrl-C (SIGINT) боловсруулагч */
void handle_SIGINT(int sig)
{
    (void)sig;
    write_str("\n");
    if (fg_running)
        return;
    print_history();
    write_str(PROMPT);
}

/* Түүхэнд нэмэх */
static void add_history(const char *cmd)
{
    strncpy(history[hist_count % HIST_SIZE], cmd, MAX_LINE);
    history[hist_count % HIST_SIZE][MAX_LINE] = '\0';
    hist_count++;
}

/* prefix-ээр эхэлсэн хамгийн сүүлийн командыг хайна */
static const char *find_history(const char *prefix)
{
    int oldest = hist_count > HIST_SIZE ? hist_count - HIST_SIZE : 0;
    size_t len = strlen(prefix);

    for (int i = hist_count - 1; i >= oldest; i--) {
        if (strncmp(history[i % HIST_SIZE], prefix, len) == 0)
            return history[i % HIST_SIZE];
    }
    return NULL;
}

/* setup(): мөр уншиж, r/r x шалгаж, токенуудад хуваана.
   1 буцаавал ажиллуулах команд бэлэн, 0 бол ажиллуулах юм алга. */
int setup(char inputBuffer[], char *args[], int *background)
{
    char line[MAX_LINE + 1];
    ssize_t length = 0;
    int ct = 0;
    char c;
    int too_long = 0;

    while (1) {
        ssize_t n = read(STDIN_FILENO, &c, 1);
        if (n < 0) {
            if (errno == EINTR) continue;
            perror("read");
            exit(1);
        }
        if (n == 0) {                 /* Ctrl-D */
            if (length == 0) {
                write_str("\n");
                exit(0);
            }
            break;
        }
        if (c == '\n') break;
        if (length < MAX_LINE) line[length++] = c;
        else too_long = 1;
    }
    line[length] = '\0';

    if (too_long) {
        fprintf(stderr, "Error: command longer than %d characters\n", MAX_LINE);
        return 0;
    }

    char *cmd = line;
    while (*cmd == ' ' || *cmd == '\t') cmd++;
    if (*cmd == '\0')
        return 0;

    /* r болон r x командууд */
    if (cmd[0] == 'r' && (cmd[1] == '\0' || cmd[1] == ' ' || cmd[1] == '\t')) {
        char *prefix = cmd + 1;
        while (*prefix == ' ' || *prefix == '\t') prefix++;

        const char *found = find_history(prefix);
        if (found == NULL) {
            if (*prefix == '\0')
                fprintf(stderr, "Error: no commands in history\n");
            else
                fprintf(stderr, "Error: no command in history starts with '%s'\n",
                        prefix);
            return 0;
        }
        strcpy(inputBuffer, found);
        printf("%s\n", inputBuffer);
        fflush(stdout);
    } else {
        strcpy(inputBuffer, cmd);
    }

    add_history(inputBuffer);

    /* Токенуудад хуваах */
    char *p = inputBuffer;
    while (*p != '\0') {
        while (*p == ' ' || *p == '\t') *p++ = '\0';
        if (*p == '\0') break;

        char *start = p;
        while (*p != '\0' && *p != ' ' && *p != '\t') p++;

        if (p - start == 1 && *start == '&') {
            *background = 1;
        } else {
            if (*(p - 1) == '&') {
                *background = 1;
                *(p - 1) = '\0';
            }
            if (ct < MAX_LINE / 2)
                args[ct++] = start;
        }
    }
    args[ct] = NULL;

    return ct > 0;
}

int main(void)
{
    char inputBuffer[MAX_LINE + 1];
    int  background;
    char *args[MAX_LINE / 2 + 1];

    /* SIGINT боловсруулагчийг тохируулах */
    struct sigaction handler;
    memset(&handler, 0, sizeof(handler));
    handler.sa_handler = handle_SIGINT;
    sigemptyset(&handler.sa_mask);
    handler.sa_flags = SA_RESTART;
    sigaction(SIGINT, &handler, NULL);

    while (1) {
        background = 0;

        while (waitpid(-1, NULL, WNOHANG) > 0)
            ;

        write_str(PROMPT);

        if (!setup(inputBuffer, args, &background))
            continue;

        if (strcmp(args[0], "exit") == 0)
            exit(0);

        pid_t pid = fork();                 /* (1) хүү процесс үүсгэх */

        if (pid < 0) {
            perror("fork");
        } else if (pid == 0) {
            signal(SIGINT, SIG_DFL);
            execvp(args[0], args);          /* (2) командыг ажиллуулах */
            fprintf(stderr, "%s: command not found\n", args[0]);
            _exit(1);
        } else {
            if (background == 0) {          /* (3) & байхгүй бол хүлээх */
                fg_running = 1;
                waitpid(pid, NULL, 0);
                fg_running = 0;
            } else {
                printf("[background pid %d]\n", (int)pid);
                fflush(stdout);
            }
        }
    }
    return 0;
}
