//
//  main.c
//  tish - Tiny Shell
//  C implementation of forking and processing
//  foreground and background jobs
//
//  Created by Mary Martinez on 7/6/15.
//  Copyright (c) 2015 Mary. All rights reserved.
//

#include <signal.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>

#define MAX_LINE 1024
#define MAX_JOBS 8
#define DELIMS " \n"

struct job {                                            // each job has pid and command name
    pid_t pid;
    char command[MAX_LINE];
    bool bg;
};

struct job jobs[MAX_JOBS];

int add_job(struct job *jobs, pid_t pid, char *command, bool bg);
void remove_job(pid_t victim_pid);
void kill_jobs(struct job *jobs);
void init_jobs(struct job *jobs);
void print_jobs(struct job *jobs);

int internal_command(char **argv);

int main() {
    char *argv[MAX_LINE/2 + 1];
    char line[MAX_LINE];
    
    pid_t pid;
    int background;
    
    init_jobs(jobs);
    
    while (1) {
        printf("tish>> ");
        if (!fgets(line, MAX_LINE, stdin))
            break;
        
        int len = (int) strlen(line);
        char amp = line[len-2];                         // -1 for /0 and -1 for /n
        background = (amp == '&');                      // determine if background process
        
        int i;
        char *temp = argv[0] = strtok(line, DELIMS);    // parse tish command line arguments
        for (temp = strtok(NULL, DELIMS), i = 1; temp != NULL ; temp = strtok(NULL, DELIMS), i++ ) {
            argv[i] = temp;
        }
        
        int j;                                          // clear out the junk stored in remainder of argv array
        for (j=i; j < MAX_LINE/2 + 1 ; j++) {
            argv[j] = NULL;
        }
        
        if (!internal_command(argv)) {                  // if internal command the function processes commands
            pid = fork();
            if (pid == 0) {                             // CHILD PROCESS
                execvp(argv[0], argv);                  //      this is not internal command so child processes it
                
            }
                                                        // PARENT PROCESS
            if (background) {                           // background process
                add_job(jobs, pid, argv[0], true);
                
            }
            else {                                      // foreground process
                add_job(jobs, pid, argv[0], false);
                wait(&pid);                             // wait for completion
            }
        }
    }
    
    return 0;
}

int internal_command(char **argv) {
    if (!strcmp(argv[0], "bye")) {
        kill_jobs(jobs);                                // terminate all background processes
        return 1;
        
    }
    else if (!strcmp(argv[0], "jobs")) {
        print_jobs(jobs);                               // list all background jobs
        return 1;
        
    }
    else if (!strcmp(argv[0], "kill")) {
        char *temp = strtok(argv[1], DELIMS);           // parse out the pid from char arg value
        pid_t victim_pid = atoi(temp);                  // cast char to int
        remove_job(victim_pid);                         // remove from job queue
        kill(victim_pid, SIGTERM);                      // terminate process
        return 1;
        
    }
    else if (!strcmp(argv[0], "exit")) {
        exit(0);                                        // exit the program
        
    }
    
    return 0;
}

int add_job(struct job *jobs, pid_t pid, char *command, bool bg) {
    int i;
    
    for (i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid == 0) {                        // we only insert into next empty job in array
            jobs[i].pid = pid;                         // that was cleared by init method
            jobs[i].bg = bg;
            strcpy(jobs[i].command, command);
            return 1;
        }
    }
    
    return 0;
}

void remove_job(pid_t victim_pid) {
    int i;
    
    for (i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid == victim_pid) {
            jobs[i].pid = 0;
            jobs[i].command[0] = '\0';
        }
    }
}

void kill_jobs(struct job *jobs) {                    // kill all jobs in background
    int i;
    
    for (i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].bg) {
            jobs[i].pid = 0;                        // remove from job queue
            jobs[i].command[0] = '\0';
            kill(jobs[i].pid, SIGTERM);             // kill the job
        }
    }
}

void init_jobs(struct job *jobs) {                    // clear all data
    int i;
    
    for (i = 0; i < MAX_JOBS; i++) {
        jobs[i].pid = 0;
        jobs[i].command[0] = '\0';
    }
    
}

void print_jobs(struct job *jobs) {
    int i;
    char bg_process[] = "background";
    char fg_process[] = "foreground";
    
    for (i = 0; i < MAX_JOBS; i++) {
        if (jobs[i].pid != 0) {                       // we only print non empty jobs in array
            if (jobs[i].bg) {
                printf("<pid>: %d   <command>: %s   <thread>: %s\n", jobs[i].pid, jobs[i].command, bg_process);
            }
            else {
                printf("<pid>: %d   <command>: %s   <thread>: %s\n", jobs[i].pid, jobs[i].command, fg_process);
            }
        }
    }
}
