/*
 * Problem 3.19 - version 2: elapsed time of a command, IPC = ordinary pipe.
 *
 *     ./time_pipe <command> [args...]
 *
 * The child writes the starting time (the struct timeval itself, not a
 * pointer to it - a pointer would be meaningless in the parent's address
 * space) into the pipe just before exec().  After the child terminates the
 * parent reads the starting time from the pipe, takes the ending time and
 * prints the difference.
 *
 * Build: gcc -Wall -o time_pipe time_pipe.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>

#define READ_END  0
#define WRITE_END 1

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <command> [args...]\n", argv[0]);
        return 1;
    }

    int fd[2];
    if (pipe(fd) == -1) { perror("pipe"); return 1; }

    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }

    if (pid == 0) {                                 /* child */
        close(fd[READ_END]);                        /* unused end */

        struct timeval start;
        gettimeofday(&start, NULL);                 /* starting time */
        if (write(fd[WRITE_END], &start, sizeof(start)) != sizeof(start)) {
            perror("write");
            _exit(1);
        }
        close(fd[WRITE_END]);

        execvp(argv[1], &argv[1]);                  /* run the command */
        perror("execvp");                           /* reached only on error */
        _exit(127);
    }

    /* parent */
    close(fd[WRITE_END]);                           /* unused end */

    int status;
    if (waitpid(pid, &status, 0) == -1) { perror("waitpid"); return 1; }

    struct timeval end, start;
    gettimeofday(&end, NULL);                       /* ending time */

    if (WIFEXITED(status) && WEXITSTATUS(status) == 127) {
        /* the child could not exec the command (convention: status 127) */
        fprintf(stderr, "could not run \"%s\"\n", argv[1]);
        return 127;
    }

    if (read(fd[READ_END], &start, sizeof(start)) != sizeof(start)) {
        fprintf(stderr, "could not read the starting time from the pipe\n");
        return 1;
    }
    close(fd[READ_END]);

    double elapsed = (double)(end.tv_sec - start.tv_sec)
                   + (double)(end.tv_usec - start.tv_usec) / 1000000.0;
    printf("Elapsed time: %.5f\n", elapsed);
    return 0;
}
