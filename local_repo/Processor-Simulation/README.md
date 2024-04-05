# Task-Simulation Overview

This Python program simulates task scheduling in an operating system environment. It supports three scheduling algorithms: Serial Computing (SC), Timesharing (TS), and Multitasking (MT). The program reads configuration details from a file named `config.txt`.

## Setup

To run the simulation, ensure you have Python installed on your system. Then, follow these steps:

1. Clone the repository to your local machine.
2. Place your desired configuration file (`config.txt`) in the same directory as the Python script.
3. Execute the Python script by running the command below.
```
python task_simulation.py <config_filename>
```

## Configuration File Structure

The `config.txt` file serves as input for the simulation. It follows a specific structure:

1. **Total Lines**: Indicates the total number of lines in the file.
2. **Unit of Time**: Specifies the unit of time used (e.g., cycles, seconds, milliseconds, nanoseconds).
3. **Number of Tasks**: Specifies the total number of tasks.
4. **Scheduling Algorithm**: Specifies the scheduling algorithm (SC, TS, or MT).
5. **Timeslice Duration**: Specifies the quantum or timeslice duration (applicable only for TS and MT).
6. **CPU Utilization Request** (Optional): Requests CPU utilization for a given period.

After these initial lines, each subsequent line represents a task with the following attributes:
- Task name (only capital case English letters).
- Arrival time of the task.
- CPU time required by the task.
- I/O time required by the task.

## Task Execution Structure

All tasks adhere to the following execution structure:
- CPU processing occurs before I/O operations.
- Tasks have limited execution, ensuring that turnaround times remain within a manageable range.

# Program Output
The output shows the simulation results of task scheduling using the Timesharing (TS) algorithm with a timeslice of 2 seconds. The CPU utilization, within the specified time range of 0s to 12s, is calculated to be 67%.

Each row represents a task, and the columns represent different metrics:

- **Arr.**: Arrival time of the task.
- **CPU**: Time spent on the CPU.
- **I/O**: Time spent on input/output operations.
- **Compl**: Completion time of the task.
- **Tr**: Turnaround time, which is the difference between completion time and arrival time.
- **Rt**: Response time, which is the difference between completion time and the sum of CPU and I/O times.


# Example Executions
Below demonstrate an example execution for each type of processing as well as gives an in-depth explaination of its output.

## Example 1: Serial Computing (SC)
### Config.txt
```
9
s
3
sc
0
A 0 8 0
B 2 4 0
C 5 6 0
```

### Output
```
SERIAL COMPUTING        CPU utilization [0s,10s] is 100%
        Arr.    CPU     I/O     Compl   Tr      Rt
A       0       8       0       8       8       0
B       2       4       0       12      10      6
C       5       6       0       18      13      7
```

### Explanation:
- There are 3 tasks (A, B, and C).
- The SC algorithm is selected.
- Task A arrives at time 0, requires 8 units of CPU time, and has no I/O operations.
- Task B arrives at time 2, requires 4 units of CPU time, and has no I/O operations.
- Task C arrives at time 5, requires 6 units of CPU time, and has no I/O operations.
- The tasks will be executed serially, one after another, according to their arrival times.

### Gnatt Chart:
```
Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |17 |18 |
------------------------------------------------------------------------------
 A   | A | A | A | A | A | A | A | A |   |   |   |   |   |   |   |   |   |   |
 B   |   |   |   |   |   |   |   |   | B | B | B | B |   |   |   |   |   |   |
 C   |   |   |   |   |   |   |   |   |   |   |   |   | C | C | C | C | C | C |
```

## Example 2: Timesharing (TS)
### Config.txt
```
9
ms
4
ts
3
A 4 7 0
B 1 5 0
C 2 8 0
D 4 6 0
```

### Output
```
tasksim_2013.py run  --/--/--  --:--:--  4 jobs ; unit of time is 3ms
IMESHARING     CPU utilization unlisted
        Arr.    CPU     I/O     Compl   Tr      Rt
A       4       7       0       37      33      8
B       1       5       0       17      16      2
C       2       8       0       32      30      4
D       4       6       0       24      20      5
```

### Explanation:
- There are 4 tasks (A, B, C, and D).
- The TS algorithm is selected with a timeslice of 3 milliseconds.
- Task A arrives at time 0, requires 10 units of CPU time, and has no I/O operations.
- Task B arrives at time 1, requires 5 units of CPU time, and has no I/O operations.
- Task C arrives at time 2, requires 8 units of CPU time, and has no I/O operations.
- Task D arrives at time 4, requires 6 units of CPU time, and has no I/O operations.
- Tasks will be executed in a round-robin fashion with each task receiving a maximum of 3 milliseconds of CPU time before being preempted.

### Gnatt Chart:
```
Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |25 |26 |27 |28 |29 |30 |31 |32 |33 |34 |35 |36 |37 |
----------------------------------------------------------------------------------------------------------------------------------------------------------
 A   | - | - | - |   |   |   |   |   |   |   |   |   | A | A | A |   |   |   |   |   |   |   |   |   | A | A | A |   |   |   |   |   |   |   |   |   | A |
 B   |   |   |   | B | B | B |   |   |   |   |   |   |   |   |   | B | B | - |   |   |   |   |   |   |   |   |   | - | - | - |   |   |   |   |   |   |   |
 C   |   |   |   |   |   |   | C | C | C |   |   |   |   |   |   |   |   |   | C | C | C |   |   |   |   |   |   |   |   |   | C | C | - |   |   |   |   |
 D   |   |   |   |   |   |   |   |   |   | D | D | D |   |   |   |   |   |   |   |   |   | D | D | D |   |   |   |   |   |   |   |   |   | - | - | - |   |
```

## Example 3: Multitasking (MT)
### Config.txt
```
10
ns
5
mt
1
A 0 7 0
B 1 4 0
C 1 6 0
D 3 5 0
E 4 3 0
```

### Output
```
processor_simulation.py run  03/02/24  HH:MM:SS  5 jobs ; unit of time is 1ns
MULTITASKING    CPU utilization unlisted
        Arr.    CPU     I/O     Compl   Tr      Rt
A       0       7       0       23      23      0
B       1       4       0       16      15      1
C       1       6       0       25      24      2
D       3       5       0       24      21      3
E       4       3       0       19      15      4
```

### Explanation:
- There are 5 tasks (A, B, C, D, and E).
- The MT algorithm is selected with a timeslice of 1 nanosecond.
- Task A arrives at time 0, requires 7 units of CPU time, and has no I/O operations.
- Task B arrives at time 1, requires 4 units of CPU time, and has no I/O operations.
- Task C arrives at time 1, requires 6 units of CPU time, and has no I/O operations.
- Task D arrives at time 3, requires 5 units of CPU time, and has no I/O operations.
- Task E arrives at time 4, requires 3 units of CPU time, and has no I/O operations.
- Tasks will be executed concurrently with preemption, allowing each task to run for at most 1 nanosecond before being swapped out.

### Gantt Chart:
```
Time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |25 |
----------------------------------------------------------------------------------------------------------
 A   | A | A |   |   | A |   |   |   | A |   |   |   |   | A |   |   |   |   | A |   |   | A |   |   |   | 
 B   |   |   | B |   |   | B |   |   |   | B |   |   |   |   | B |   |   |   |   |   |   |   |   |   |   |
 C   |   |   |   | C |   |   | C |   |   |   |   | C |   |   |   |   | C |   |   |   | C |   |   |   | C |
 D   |   |   |   |   |   |   |   |   |   |   | D |   |   |   |   | D |   |   |   | D |   |   |   | D |   |
 E   |   |   |   |   |   |   |   | E |   |   |   |   | E |   |   |   |   | E |   |   |   |   |   |   |   |
```

