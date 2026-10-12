/*
 * Problem 3.27 - file copy through an ordinary pipe.
 *
 *     ./filecopy input.txt copy.txt
 *
 * The parent reads the source file and writes its contents into the pipe;
 * the child reads the pipe and writes everything to the destination file.
 *
 * Build: gcc -Wall -o filecopy filecopy.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define BUFFER_SIZE 4096
#define READ_END  0
#define WRITE_END 1

/* write all n bytes, handling partial writes; returns 0 on success */
static int write_all(int fd, const char *buf, ssize_t n)
{
    while (n > 0) {
        ssize_t w = write(fd, buf, (size_t)n);
        if (w < 0) return -1;
        buf += w;
        n   -= w;
    }
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 3) {
        fprintf(stderr, "usage: %s <source file> <destination file>\n", argv[0]);
        return 1;
    }

    signal(SIGPIPE, SIG_IGN);            /* get EPIPE instead of being killed */

    /* open the source first, so that a bad name is reported before forking */
    int src = open(argv[1], O_RDONLY);
    if (src == -1) { perror(argv[1]); return 1; }

    int fd[2];
    if (pipe(fd) == -1) { perror("pipe"); return 1; }

    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }

    if (pid == 0) {                                  /* ---- child ---- */
        close(fd[WRITE_END]);                        /* unused end */
        close(src);

        int dst = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (dst == -1) { perror(argv[2]); _exit(1); }

        char buf[BUFFER_SIZE];
        ssize_t n;
        while ((n = read(fd[READ_END], buf, sizeof(buf))) > 0) {
            if (write_all(dst, buf, n) == -1) {
                perror("write (child)");
                _exit(1);
            }
        }
        if (n < 0) { perror("read (child)"); _exit(1); }

        close(dst);
        close(fd[READ_END]);
        _exit(0);
    }

    /* ---- parent ---- */
    close(fd[READ_END]);                             /* unused end */

    char buf[BUFFER_SIZE];
    ssize_t n;
    long long total = 0;
    int rc = 0;
    while ((n = read(src, buf, sizeof(buf))) > 0) {
        if (write_all(fd[WRITE_END], buf, n) == -1) {
            perror("write (parent)");
            rc = 1;
            break;
        }
        total += n;
    }
    if (n < 0) { perror("read (parent)"); rc = 1; }

    close(src);
    close(fd[WRITE_END]);                            /* child sees EOF */

    int status;
    wait(&status);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) rc = 1;

    if (rc == 0)
        printf("Copied %lld bytes: %s -> %s\n", total, argv[1], argv[2]);
    return rc;
}
