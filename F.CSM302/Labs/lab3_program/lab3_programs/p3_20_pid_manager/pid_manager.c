/*
 * Problem 3.20 - pid manager.
 *
 * The availability of the pids MIN_PID..MAX_PID is kept in a bitmap (as Linux
 * does): bit i = 0  -> pid MIN_PID + i is available
 *          bit i = 1  -> pid MIN_PID + i is in use
 *
 * allocate_pid() returns the lowest available pid (first fit).
 */
#include <stdio.h>
#include <stdlib.h>
#include "pid_manager.h"

#define NUM_PIDS   (MAX_PID - MIN_PID + 1)     /* 4701 pids */
#define MAP_BYTES  ((NUM_PIDS + 7) / 8)

static unsigned char *pid_map = NULL;          /* the bitmap */

static int  bit_is_set(int i) { return (pid_map[i / 8] >> (i % 8)) & 1; }
static void set_bit(int i)    { pid_map[i / 8] |=  (unsigned char)(1u << (i % 8)); }
static void clear_bit(int i)  { pid_map[i / 8] &= (unsigned char)~(1u << (i % 8)); }

int allocate_map(void)
{
    free(pid_map);                             /* allow re-initialization */
    pid_map = calloc(MAP_BYTES, 1);            /* all bits 0 = all available */
    if (pid_map == NULL)
        return -1;
    return 1;
}

int allocate_pid(void)
{
    if (pid_map == NULL)                       /* allocate_map() not called */
        return -1;

    for (int i = 0; i < NUM_PIDS; i++) {
        if (!bit_is_set(i)) {
            set_bit(i);
            return MIN_PID + i;
        }
    }
    return -1;                                 /* every pid is in use */
}

void release_pid(int pid)
{
    if (pid_map == NULL || pid < MIN_PID || pid > MAX_PID)
        return;                                /* not a pid of this manager */
    clear_bit(pid - MIN_PID);
}
