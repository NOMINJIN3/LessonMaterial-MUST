/* Figure 3.33 as printed in the book (+ <sys/wait.h>); the path of the program is taken from argv[1]
   ONLY in this demo so that a failing execlp() can be shown (default: /bin/ls, as in the book). */
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
pid_t pid;
const char *path = (argc > 1) ? argv[1] : "/bin/ls";

   /* fork a child process */
   pid = fork();

   if (pid < 0) { /* error occurred */
      fprintf(stderr, "Fork Failed");
      return 1;
   }
   else if (pid == 0) { /* child process */
      execlp(path,"ls",NULL);
      printf("LINE J\n");
   }
   else { /* parent process */
     /* parent will wait for the child to complete */
     wait(NULL);
     printf("Child Complete\n");
   }

   return 0;
}
