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
