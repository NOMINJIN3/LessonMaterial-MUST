/*
 * Problem 3.21 - Collatz conjecture with fork().
 *
 *     ./collatz_fork <positive integer>
 *
 * The child process generates and prints the Collatz sequence
 *     n = n/2 (n even),  n = 3n+1 (n odd)     until n == 1.
 * The parent calls wait() so that it finishes only after the child.
 * The child prints the sequence itself because parent and child have their
 * own copies of the data (see Practice Exercise 3.1).
 *
 * Build: gcc -Wall -o collatz_fork collatz_fork.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    /* ---- error checking: exactly one argument, a positive integer ---- */
    if (argc != 2) {
        fprintf(stderr, "usage: %s <positive integer>\n", argv[0]);
        return 1;
    }

    char *endp;
    errno = 0;
    long long v = strtoll(argv[1], &endp, 10);
    if (endp == argv[1] || *endp != '\0' || errno == ERANGE || v <= 0) {
        fprintf(stderr, "error: \"%s\" is not a positive integer\n", argv[1]);
        return 1;
    }
    unsigned long long n = (unsigned long long)v;

    pid_t pid = fork();
    if (pid < 0) {                                  /* error occurred */
        perror("fork");
        return 1;
    }

    if (pid == 0) {                                 /* child process */
        printf("%llu", n);
        while (n != 1) {
            if (n % 2 == 0) {
                n = n / 2;
            } else {
                if (n > (ULLONG_MAX - 1) / 3) {     /* 3n+1 would overflow */
                    fprintf(stderr, "\nerror: overflow while computing 3n+1\n");
                    exit(2);
                }
                n = 3 * n + 1;
            }
            printf(", %llu", n);
        }
        printf("\n");
        exit(0);
    }

    /* parent process: wait for the child to complete */
    int status;
    wait(&status);
    if (WIFEXITED(status))
        return WEXITSTATUS(status);
    return 1;
}
