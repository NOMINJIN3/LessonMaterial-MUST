/*
 * Test / demo driver for the pid manager of Problem 3.20.
 * Build: gcc -Wall -o pid_test pid_test.c pid_manager.c
 */
#include <stdio.h>
#include "pid_manager.h"

int main(void)
{
    int total = MAX_PID - MIN_PID + 1;
    int ok = 1;

    /* allocate_pid() before allocate_map() must fail */
    printf("allocate_pid() before allocate_map(): %d (expected -1)\n",
           allocate_pid());

    printf("allocate_map() = %d (expected 1)\n", allocate_map());

    /* hand out a few pids */
    int a = allocate_pid(), b = allocate_pid(), c = allocate_pid();
    printf("allocated pids: %d %d %d (expected %d %d %d)\n",
           a, b, c, MIN_PID, MIN_PID + 1, MIN_PID + 2);

    /* release the middle one; the manager may hand it out again */
    release_pid(b);
    printf("released %d, next allocate_pid() = %d (expected %d)\n",
           b, allocate_pid(), b);

    /* exhaust all pids */
    int count = 3;                              /* a, b(again), c are in use */
    int last = -1, p;
    while ((p = allocate_pid()) != -1) { count++; last = p; }
    printf("allocated %d pids in total, last = %d (expected %d, last %d)\n",
           count, last, total, MAX_PID);
    if (count != total || last != MAX_PID) ok = 0;

    printf("allocate_pid() when all in use: %d (expected -1)\n", allocate_pid());

    /* releasing makes pids available again (lowest free pid first) */
    release_pid(MAX_PID);
    release_pid(MIN_PID + 10);
    int r1 = allocate_pid();
    int r2 = allocate_pid();
    int r3 = allocate_pid();
    printf("released %d and %d, then allocated: %d %d %d (expected %d %d -1)\n",
           MAX_PID, MIN_PID + 10, r1, r2, r3, MIN_PID + 10, MAX_PID);
    if (r1 != MIN_PID + 10 || r2 != MAX_PID || r3 != -1) ok = 0;

    /* out-of-range release must be ignored */
    release_pid(MIN_PID - 1);
    release_pid(MAX_PID + 1);
    printf("out-of-range release ignored: allocate_pid() = %d (expected -1)\n",
           allocate_pid());

    printf("%s\n", ok ? "ALL CHECKS PASSED" : "SOME CHECKS FAILED");
    return ok ? 0 : 1;
}
