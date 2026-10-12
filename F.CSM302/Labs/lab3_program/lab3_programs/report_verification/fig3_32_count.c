/* Figure 3.32 (for loop with fork) + one printf per process so the processes can be counted */
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    int i;

    for (i = 0; i < 4; i++)
        fork();

    printf("pid=%d ppid=%d\n", getpid(), getppid());
    while (wait(NULL) > 0) ;
    return 0;
}
