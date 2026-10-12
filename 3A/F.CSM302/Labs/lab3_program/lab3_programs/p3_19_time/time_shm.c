/*
 * Problem 3.19 - version 1: elapsed time of a command, IPC = POSIX shared memory.
 *
 *     ./time_shm <command> [args...]
 *
 * The shared-memory object is created BEFORE fork(), so parent and child both
 * have it mapped.  The child stores the starting time in it just before
 * exec(); after the child terminates the parent reads it back, takes the
 * ending time and prints the difference.
 *
 * Build: gcc -Wall -o time_shm time_shm.c -lrt
 */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>

#define SHM_NAME "/time_shm_start"

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <command> [args...]\n", argv[0]);
        return 1;
    }

    /* 1. create the shared-memory object (shm_open, ftruncate, mmap) */
    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (fd == -1) { perror("shm_open"); return 1; }

    if (ftruncate(fd, sizeof(struct timeval)) == -1) {
        perror("ftruncate");
        shm_unlink(SHM_NAME);
        return 1;
    }

    struct timeval *start = mmap(NULL, sizeof(struct timeval),
                                 PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (start == MAP_FAILED) {
        perror("mmap");
        shm_unlink(SHM_NAME);
        return 1;
    }

    /* 2. create the child */
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        shm_unlink(SHM_NAME);
        return 1;
    }

    if (pid == 0) {                         /* child */
        gettimeofday(start, NULL);          /* starting time -> shared memory */
        execvp(argv[1], &argv[1]);          /* run the command */
        perror("execvp");                   /* reached only if exec failed */
        _exit(127);
    }

    /* 3. parent: wait for the child, then take the ending time */
    int status;
    if (waitpid(pid, &status, 0) == -1) {
        perror("waitpid");
        shm_unlink(SHM_NAME);
        return 1;
    }

    struct timeval end;
    gettimeofday(&end, NULL);

    if (WIFEXITED(status) && WEXITSTATUS(status) == 127) {
        /* the child could not exec the command (convention: status 127) */
        fprintf(stderr, "could not run \"%s\"\n", argv[1]);
        munmap(start, sizeof(struct timeval));
        close(fd);
        shm_unlink(SHM_NAME);
        return 127;
    }

    double elapsed = (double)(end.tv_sec - start->tv_sec)
                   + (double)(end.tv_usec - start->tv_usec) / 1000000.0;
    printf("Elapsed time: %.5f\n", elapsed);

    /* 4. clean up */
    munmap(start, sizeof(struct timeval));
    close(fd);
    shm_unlink(SHM_NAME);
    return 0;
}
