/*
 * Problem 3.22 - Collatz conjecture, sequence passed through POSIX shared memory.
 *
 *     ./collatz_shm <positive integer>
 *
 * Parent:  a. establish the shared-memory object (shm_open, ftruncate, mmap)
 *          b. create the child and wait for it to terminate
 *          c. output the contents of shared memory
 *          d. remove the shared-memory object (shm_unlink)
 * Child:   computes the Collatz sequence and stores it in shared memory.
 *
 * Parent and child are synchronized only by wait(): the parent does not
 * touch the data until the child has exited.
 *
 * Build: gcc -Wall -o collatz_shm collatz_shm.c -lrt
 */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

#define SHM_NAME  "/collatz_shm"
#define MAX_TERMS 100000                       /* capacity of the sequence */

struct shared_data {                           /* layout of the shared memory */
    size_t count;                              /* how many terms were stored */
    unsigned long long seq[MAX_TERMS];         /* the sequence itself */
};

int main(int argc, char *argv[])
{
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

    /* a. establish the shared-memory object */
    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (fd == -1) { perror("shm_open"); return 1; }

    if (ftruncate(fd, sizeof(struct shared_data)) == -1) {
        perror("ftruncate");
        shm_unlink(SHM_NAME);
        return 1;
    }

    struct shared_data *shm = mmap(NULL, sizeof(struct shared_data),
                                   PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shm == MAP_FAILED) {
        perror("mmap");
        shm_unlink(SHM_NAME);
        return 1;
    }
    shm->count = 0;

    /* b. create the child and wait for it */
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        shm_unlink(SHM_NAME);
        return 1;
    }

    if (pid == 0) {                             /* child: write to shared memory */
        unsigned long long n = (unsigned long long)v;
        shm->seq[shm->count++] = n;
        while (n != 1) {
            if (n % 2 == 0) {
                n = n / 2;
            } else {
                if (n > (ULLONG_MAX - 1) / 3) {
                    fprintf(stderr, "error: overflow while computing 3n+1\n");
                    exit(2);
                }
                n = 3 * n + 1;
            }
            if (shm->count >= MAX_TERMS) {
                fprintf(stderr, "error: sequence longer than %d terms\n",
                        MAX_TERMS);
                exit(3);
            }
            shm->seq[shm->count++] = n;
        }
        exit(0);
    }

    int status;
    wait(&status);

    int rc = 0;
    if (WIFEXITED(status) && WEXITSTATUS(status) == 0) {
        /* c. output the contents of shared memory */
        for (size_t i = 0; i < shm->count; i++)
            printf(i == 0 ? "%llu" : ", %llu", shm->seq[i]);
        printf("\n");
    } else {
        fprintf(stderr, "child failed, nothing to print\n");
        rc = 1;
    }

    /* d. remove the shared-memory object */
    munmap(shm, sizeof(struct shared_data));
    close(fd);
    shm_unlink(SHM_NAME);
    return rc;
}
