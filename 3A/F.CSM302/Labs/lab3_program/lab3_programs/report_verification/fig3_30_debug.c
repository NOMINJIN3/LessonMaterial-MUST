#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <unistd.h>

int value = 5;

int main()
{
    pid_t pid = fork();
    if (pid == 0) {                       /* child */
        value += 15;
        printf("CHILD:  value = %d (address %p)\n", value, (void *)&value);
        return 0;
    } else if (pid > 0) {                 /* parent */
        wait(NULL);
        printf("PARENT: value = %d (address %p)\n", value, (void *)&value);
        return 0;
    }
}
