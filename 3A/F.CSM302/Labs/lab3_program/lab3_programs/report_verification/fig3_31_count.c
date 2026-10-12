/* Figure 3.31 with one printf per process so the processes can be counted */
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    fork();   /* fork #1 */
    fork();   /* fork #2 */
    fork();   /* fork #3 */

    printf("pid=%d ppid=%d\n", getpid(), getppid());
    while (wait(NULL) > 0) ;
    return 0;
}
