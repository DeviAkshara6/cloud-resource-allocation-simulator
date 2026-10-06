# Cloud Resource Allocation and Scheduling Simulator

An Operating Systems CBP project that simulates cloud virtual machines, resource allocation, and CPU scheduling.

## Features

- Generate virtual machines with CPU and RAM resources
- Generate random cloud tasks
- First Fit resource allocation
- Best Fit resource allocation
- FCFS scheduling
- SJF scheduling
- Priority scheduling
- Round Robin scheduling
- Waiting time
- Turnaround time
- Completion time
- Throughput
- CPU utilization
- VM resource utilization chart
- CPU scheduling Gantt chart

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
cloud_resource_allocation_simulator/
├── app.py
├── simulator.py
├── requirements.txt
└── README.md
```

## OS concepts demonstrated

- CPU scheduling
- Process/task management
- Resource allocation
- Resource utilization
- Scheduling performance
- Waiting and turnaround time
- Throughput
- Load distribution

## Future enhancements

- Banker's Algorithm for deadlock avoidance
- Task waiting queue
- Resource release after task completion
- Algorithm comparison on identical workloads
- More detailed cloud load balancing
