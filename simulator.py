import random


class VM:
    def __init__(self, vm_id, cpu, ram):
        self.vm_id = vm_id

        self.total_cpu = cpu
        self.available_cpu = cpu

        self.total_ram = ram
        self.available_ram = ram

        self.tasks = []

    def can_allocate(self, task):
        return (
            self.available_cpu >= task.cpu_required
            and self.available_ram >= task.ram_required
        )

    def allocate(self, task):
        self.available_cpu -= task.cpu_required
        self.available_ram -= task.ram_required

        self.tasks.append(task.task_id)
        task.vm_id = self.vm_id


class Task:
    def __init__(
        self,
        task_id,
        cpu_required,
        ram_required,
        burst_time,
        arrival_time,
        priority
    ):
        self.task_id = task_id

        self.cpu_required = cpu_required
        self.ram_required = ram_required

        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority

        self.vm_id = "Waiting"

        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None


# ---------------------------------------------------------
# GENERATE VMs
# ---------------------------------------------------------

def generate_vms(n):

    return [
        VM(
            f"VM{i}",
            random.choice([2, 4, 6, 8]),
            random.choice([4, 8, 16])
        )
        for i in range(1, n + 1)
    ]


# ---------------------------------------------------------
# GENERATE TASKS
# ---------------------------------------------------------

def generate_tasks(n):

    return [
        Task(
            f"T{i}",
            random.choice([1, 2, 3, 4]),
            random.choice([1, 2, 4, 8]),
            random.randint(2, 10),
            random.randint(0, 5),
            random.randint(1, 5)
        )
        for i in range(1, n + 1)
    ]


# ---------------------------------------------------------
# TASK ALLOCATION ORDER
# ---------------------------------------------------------

def allocation_order(tasks):

    return sorted(
        tasks,
        key=lambda t: (t.arrival_time, t.task_id)
    )


# =========================================================
# MEMORY ALLOCATION ALGORITHMS
# =========================================================

# ---------------------------------------------------------
# FIRST FIT
# ---------------------------------------------------------

def allocate_first_fit(vms, tasks):

    messages = []

    for task in allocation_order(tasks):

        for vm in vms:

            if vm.can_allocate(task):

                vm.allocate(task)

                messages.append(
                    f"{task.task_id} → {vm.vm_id} "
                    f"(First Fit)"
                )

                break

        else:

            messages.append(
                f"{task.task_id} → WAITING "
                f"(insufficient memory/resources)"
            )

    return messages


# ---------------------------------------------------------
# BEST FIT
# ---------------------------------------------------------

def allocate_best_fit(vms, tasks):

    messages = []

    for task in allocation_order(tasks):

        suitable_vms = [
            vm
            for vm in vms
            if vm.can_allocate(task)
        ]

        if suitable_vms:

            # BEST FIT:
            # Choose the smallest available RAM
            # that can accommodate the task.

            selected_vm = min(
                suitable_vms,
                key=lambda vm: (
                    vm.available_ram,
                    vm.available_cpu,
                    vm.vm_id
                )
            )

            selected_vm.allocate(task)

            messages.append(
                f"{task.task_id} → {selected_vm.vm_id} "
                f"(Best Fit)"
            )

        else:

            messages.append(
                f"{task.task_id} → WAITING "
                f"(insufficient memory/resources)"
            )

    return messages


# ---------------------------------------------------------
# WORST FIT
# ---------------------------------------------------------

def allocate_worst_fit(vms, tasks):

    messages = []

    for task in allocation_order(tasks):

        suitable_vms = [
            vm
            for vm in vms
            if vm.can_allocate(task)
        ]

        if suitable_vms:

            # WORST FIT:
            # Choose the largest available RAM
            # that can accommodate the task.

            selected_vm = max(
                suitable_vms,
                key=lambda vm: (
                    vm.available_ram,
                    vm.available_cpu
                )
            )

            selected_vm.allocate(task)

            messages.append(
                f"{task.task_id} → {selected_vm.vm_id} "
                f"(Worst Fit)"
            )

        else:

            messages.append(
                f"{task.task_id} → WAITING "
                f"(insufficient memory/resources)"
            )

    return messages


# =========================================================
# CPU SCHEDULING
# =========================================================

# ---------------------------------------------------------
# NON-PREEMPTIVE SCHEDULING
# ---------------------------------------------------------

def non_preemptive(tasks, selection_key):

    remaining_tasks = list(tasks)

    completed_tasks = []

    gantt = []

    current_time = 0

    while remaining_tasks:

        available_tasks = [
            task
            for task in remaining_tasks
            if task.arrival_time <= current_time
        ]

        # CPU is idle until next process arrives

        if not available_tasks:

            next_arrival = min(
                task.arrival_time
                for task in remaining_tasks
            )

            if current_time < next_arrival:

                gantt.append(
                    {
                        "task": "IDLE",
                        "start": current_time,
                        "duration": (
                            next_arrival - current_time
                        )
                    }
                )

                current_time = next_arrival

            continue

        # Select process according to algorithm

        task = min(
            available_tasks,
            key=selection_key
        )

        remaining_tasks.remove(task)

        start_time = current_time

        # Waiting Time

        task.waiting_time = (
            start_time - task.arrival_time
        )

        # Execute process

        current_time += task.burst_time

        # Completion Time

        task.completion_time = current_time

        # Turnaround Time

        task.turnaround_time = (
            task.completion_time
            - task.arrival_time
        )

        completed_tasks.append(task)

        gantt.append(
            {
                "task": task.task_id,
                "start": start_time,
                "duration": task.burst_time
            }
        )

    return completed_tasks, gantt


# ---------------------------------------------------------
# FCFS
# ---------------------------------------------------------

def fcfs(tasks):

    return non_preemptive(
        tasks,
        lambda task: (
            task.arrival_time,
            task.task_id
        )
    )


# ---------------------------------------------------------
# SJF
# ---------------------------------------------------------

def sjf(tasks):

    return non_preemptive(
        tasks,
        lambda task: (
            task.burst_time,
            task.arrival_time,
            task.task_id
        )
    )


# ---------------------------------------------------------
# PRIORITY
# ---------------------------------------------------------

def priority_scheduling(tasks):

    return non_preemptive(
        tasks,
        lambda task: (
            task.priority,
            task.arrival_time,
            task.task_id
        )
    )


# ---------------------------------------------------------
# ROUND ROBIN
# ---------------------------------------------------------

def round_robin(tasks, quantum=2):

    tasks = sorted(
        tasks,
        key=lambda task: (
            task.arrival_time,
            task.task_id
        )
    )

    remaining_time = {
        task.task_id: task.burst_time
        for task in tasks
    }

    ready_queue = []

    completed_tasks = []

    gantt = []

    current_time = 0

    index = 0

    while len(completed_tasks) < len(tasks):

        # Add newly arrived processes

        while (
            index < len(tasks)
            and tasks[index].arrival_time <= current_time
        ):

            ready_queue.append(tasks[index])

            index += 1

        # CPU idle

        if not ready_queue:

            if index < len(tasks):

                next_arrival = tasks[index].arrival_time

                if current_time < next_arrival:

                    gantt.append(
                        {
                            "task": "IDLE",
                            "start": current_time,
                            "duration": (
                                next_arrival - current_time
                            )
                        }
                    )

                    current_time = next_arrival

            continue

        # Get first process from queue

        task = ready_queue.pop(0)

        start_time = current_time

        execution_time = min(
            quantum,
            remaining_time[task.task_id]
        )

        # Execute

        current_time += execution_time

        remaining_time[task.task_id] -= execution_time

        gantt.append(
            {
                "task": task.task_id,
                "start": start_time,
                "duration": execution_time
            }
        )

        # Add newly arrived processes

        while (
            index < len(tasks)
            and tasks[index].arrival_time <= current_time
        ):

            ready_queue.append(tasks[index])

            index += 1

        # Process still has remaining burst time

        if remaining_time[task.task_id] > 0:

            ready_queue.append(task)

        else:

            # Process completed

            task.completion_time = current_time

            task.turnaround_time = (
                task.completion_time
                - task.arrival_time
            )

            task.waiting_time = (
                task.turnaround_time
                - task.burst_time
            )

            completed_tasks.append(task)

    return completed_tasks, gantt


# =========================================================
# PERFORMANCE METRICS
# =========================================================

def calculate_metrics(tasks, vms):

    if not tasks:

        return {
            "avg_waiting": 0,
            "avg_turnaround": 0,
            "throughput": 0,
            "cpu_utilization": 0,
            "ram_utilization": 0,
            "completed_tasks": 0
        }

    total_waiting = sum(
        task.waiting_time
        for task in tasks
    )

    total_turnaround = sum(
        task.turnaround_time
        for task in tasks
    )

    total_burst = sum(
        task.burst_time
        for task in tasks
    )

    end_time = max(
        task.completion_time
        for task in tasks
    )

    # Total RAM in all VMs

    total_ram = sum(
        vm.total_ram
        for vm in vms
    )

    # RAM currently allocated

    used_ram = sum(
        vm.total_ram - vm.available_ram
        for vm in vms
    )

    avg_waiting = (
        total_waiting / len(tasks)
    )

    avg_turnaround = (
        total_turnaround / len(tasks)
    )

    throughput = (
        len(tasks) / end_time
        if end_time > 0
        else 0
    )

    # CPU utilization for the simulated CPU

    cpu_utilization = min(
        100,
        (total_burst / end_time) * 100
    ) if end_time > 0 else 0

    ram_utilization = (
        (used_ram / total_ram) * 100
        if total_ram > 0
        else 0
    )

    return {
        "avg_waiting": avg_waiting,
        "avg_turnaround": avg_turnaround,
        "throughput": throughput,
        "cpu_utilization": cpu_utilization,
        "ram_utilization": ram_utilization,
        "completed_tasks": len(tasks)
    }


# =========================================================
# TASK TABLE
# =========================================================

def build_allocation_table(tasks):

    rows = []

    for task in sorted(
        tasks,
        key=lambda t: (
            t.arrival_time,
            t.task_id
        )
    ):

        if task.completion_time is not None:

            status = "Completed"

            completion = task.completion_time
            waiting = round(
                task.waiting_time,
                2
            )

            turnaround = round(
                task.turnaround_time,
                2
            )

        else:

            status = "Waiting for Memory"

            completion = "-"
            waiting = "-"
            turnaround = "-"

        rows.append(
            {
                "Task": task.task_id,
                "VM": task.vm_id,
                "CPU Required": task.cpu_required,
                "RAM Required (GB)": task.ram_required,
                "Burst Time": task.burst_time,
                "Arrival Time": task.arrival_time,
                "Priority": task.priority,
                "Completion Time": completion,
                "Waiting Time": waiting,
                "Turnaround Time": turnaround,
                "Status": status
            }
        )

    return rows