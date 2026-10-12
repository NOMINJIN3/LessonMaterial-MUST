#ifndef PID_MANAGER_H
#define PID_MANAGER_H

#define MIN_PID 300
#define MAX_PID 5000

/* Creates and initializes the data structure that represents the pids.
 * Returns -1 if unsuccessful, 1 if successful. */
int allocate_map(void);

/* Allocates and returns a pid.
 * Returns -1 if unable to allocate a pid (all pids are in use). */
int allocate_pid(void);

/* Releases a pid so that it can be handed out again. */
void release_pid(int pid);

#endif
