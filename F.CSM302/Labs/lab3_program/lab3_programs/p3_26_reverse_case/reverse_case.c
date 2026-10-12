/*
 * Problem 3.26 - two ordinary pipes: reverse the case of a message.
 *
 *     ./reverse_case ["message"]          (default message: "Hi There")
 *
 *   parent --(pipe 1: original message)--> child
 *   parent <-(pipe 2: case-reversed msg)-- child
 *
 * Ordinary pipes are unidirectional, so two of them are needed for two-way
 * communication.  Example:  "Hi There"  ->  "hI tHERE".
 *
 * Build: gcc -Wall -o reverse_case reverse_case.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define BUFFER_SIZE 4096
#define READ_END  0
#define WRITE_END 1

int main(int argc, char *argv[])
{
    const char *msg = (argc > 1) ? argv[1] : "Hi There";
    if (strlen(msg) >= BUFFER_SIZE) {
        fprintf(stderr, "message too long (max %d characters)\n",
                BUFFER_SIZE - 1);
        return 1;
    }

    int to_child[2];                     /* pipe 1: parent -> child */
    int to_parent[2];                    /* pipe 2: child  -> parent */
    if (pipe(to_child) == -1 || pipe(to_parent) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }

    if (pid == 0) {                                  /* ---- child ---- */
        close(to_child[WRITE_END]);                  /* unused ends */
        close(to_parent[READ_END]);

        char buf[BUFFER_SIZE];
        ssize_t n;
        /* read until the parent closes its write end (EOF) */
        while ((n = read(to_child[READ_END], buf, sizeof(buf))) > 0) {
            for (ssize_t i = 0; i < n; i++) {
                if (isupper((unsigned char)buf[i]))
                    buf[i] = (char)tolower((unsigned char)buf[i]);
                else if (islower((unsigned char)buf[i]))
                    buf[i] = (char)toupper((unsigned char)buf[i]);
            }
            if (write(to_parent[WRITE_END], buf, (size_t)n) != n) {
                perror("write (child)");
                _exit(1);
            }
        }
        close(to_child[READ_END]);
        close(to_parent[WRITE_END]);
        _exit(0);
    }

    /* ---- parent ---- */
    close(to_child[READ_END]);                       /* unused ends */
    close(to_parent[WRITE_END]);

    size_t len = strlen(msg);
    if (write(to_child[WRITE_END], msg, len) != (ssize_t)len) {
        perror("write (parent)");
        return 1;
    }
    close(to_child[WRITE_END]);                      /* tells child: EOF */

    char reply[BUFFER_SIZE];
    size_t total = 0;
    ssize_t n;
    while ((n = read(to_parent[READ_END], reply + total,
                     sizeof(reply) - 1 - total)) > 0)
        total += (size_t)n;
    reply[total] = '\0';
    close(to_parent[READ_END]);

    wait(NULL);
    printf("Sent    : %s\n", msg);
    printf("Received: %s\n", reply);
    return 0;
}
