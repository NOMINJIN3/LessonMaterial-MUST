/*
 * Problem 3.18 - a child process that becomes a zombie.
 *
 * The child exits immediately, but the parent never calls wait() and just
 * sleeps.  Until the parent calls wait() (or itself terminates) the child's
 * entry stays in the process table with state Z (zombie).  The parent sleeps
 * ZOMBIE_SECONDS >= 10 s, so the zombie exists for at least 10 seconds.
 *
 * How to check:
 *     ./zombie &            run in the background
 *     ps -l                 child has "Z" in the S column; its PPID = parent PID
 *     kill -9 <parent pid>  (optional) remove the zombie before the 15 s pass
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

#define ZOMBIE_SECONDS 15

int main(void)
{
    pid_t pid = fork();

    if (pid < 0) {                      /* error occurred */
        perror("fork");
        return 1;
    }

    if (pid == 0) {                     /* child: terminate at once */
        printf("CHILD  : pid=%d exits now -> it will be a zombie\n",
               (int)getpid());
        exit(0);
    }

    /* parent: deliberately NO wait() here */
    printf("PARENT : pid=%d, child pid=%d\n", (int)getpid(), (int)pid);
    printf("PARENT : sleeping %d s without wait(); run 'ps -l' now\n",
           ZOMBIE_SECONDS);
    fflush(stdout);

    sleep(ZOMBIE_SECONDS);

    printf("PARENT : exiting; init/systemd will reap the zombie\n");
    return 0;
}
