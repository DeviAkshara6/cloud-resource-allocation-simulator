import copy

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from simulator import (
    allocate_first_fit,
    allocate_best_fit,
    allocate_worst_fit,
    build_allocation_table,
    calculate_metrics,
    fcfs,
    generate_vms,
    generate_tasks,
    priority_scheduling,
    round_robin,
    sjf
)


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Cloud Resource Allocation & Scheduling Simulator",
    page_icon="☁️",
    layout="wide"
)
st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #666666;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: #f7f9fc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    .section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    '<div class="main-title">☁️ Cloud Resource Allocation & Scheduling Simulator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">OS CBP Project • Memory Allocation + CPU Scheduling Simulation</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 15px;
    ">
        ⚙️ Simulation Settings
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "Configure the cloud environment and select the OS algorithms.",
)


num_vms = st.sidebar.slider(
    "Number of VMs",
    min_value=2,
    max_value=10,
    value=5
)


num_tasks = st.sidebar.slider(
    "Number of Tasks",
    min_value=5,
    max_value=30,
    value=10
)


allocation_algorithm = st.sidebar.selectbox(
    "Memory Allocation Algorithm",
    [
        "First Fit",
        "Best Fit",
        "Worst Fit"
    ]
)


scheduling_algorithm = st.sidebar.selectbox(
    "CPU Scheduling Algorithm",
    [
        "FCFS",
        "SJF",
        "Priority",
        "Round Robin"
    ]
)


quantum = 2

if scheduling_algorithm == "Round Robin":

    quantum = st.sidebar.slider(
        "Time Quantum",
        min_value=1,
        max_value=5,
        value=2
    )


# =========================================================
# FIXED SCENARIO
# =========================================================

if "base_vms" not in st.session_state:

    st.session_state["base_vms"] = generate_vms(
        num_vms
    )


if "base_tasks" not in st.session_state:

    st.session_state["base_tasks"] = generate_tasks(
        num_tasks
    )


# If user changes number of VMs/tasks,
# create a new scenario.

if (
    len(st.session_state["base_vms"]) != num_vms
    or
    len(st.session_state["base_tasks"]) != num_tasks
):

    st.session_state["base_vms"] = generate_vms(
        num_vms
    )

    st.session_state["base_tasks"] = generate_tasks(
        num_tasks
    )


# =========================================================
# BUTTONS
# =========================================================

st.sidebar.markdown("---")

run = st.sidebar.button(
    "▶️  Run Simulation",
    use_container_width=True,
    type="primary"
)

new_scenario = st.sidebar.button(
    "🔄  Generate New Scenario",
    use_container_width=True
)


# =========================================================
# NEW SCENARIO
# =========================================================

if new_scenario:

    st.session_state["base_vms"] = generate_vms(
        num_vms
    )

    st.session_state["base_tasks"] = generate_tasks(
        num_tasks
    )

    for key in [
        "vms",
        "tasks",
        "scheduled_tasks",
        "waiting_tasks",
        "gantt",
        "metrics",
        "allocation_log",
        "allocation_algorithm",
        "scheduling_algorithm"
    ]:

        st.session_state.pop(
            key,
            None
        )

    st.rerun()


# =========================================================
# RUN SIMULATION
# =========================================================

if run:

    # IMPORTANT:
    # Use a fresh copy every time.
    # This prevents one simulation from modifying
    # the fixed scenario.

    vms = copy.deepcopy(
        st.session_state["base_vms"]
    )

    tasks = copy.deepcopy(
        st.session_state["base_tasks"]
    )


    # -----------------------------------------------------
    # MEMORY ALLOCATION
    # -----------------------------------------------------

    if allocation_algorithm == "First Fit":

        allocation_log = allocate_first_fit(
            vms,
            tasks
        )

    elif allocation_algorithm == "Best Fit":

        allocation_log = allocate_best_fit(
            vms,
            tasks
        )

    else:

        allocation_log = allocate_worst_fit(
            vms,
            tasks
        )


    # -----------------------------------------------------
    # ONLY ALLOCATED TASKS ENTER READY QUEUE
    # -----------------------------------------------------

    allocated_tasks = [
        task
        for task in tasks
        if task.vm_id != "Waiting"
    ]


    waiting_tasks = [
        task
        for task in tasks
        if task.vm_id == "Waiting"
    ]


    # -----------------------------------------------------
    # CPU SCHEDULING
    # -----------------------------------------------------

    if scheduling_algorithm == "FCFS":

        scheduled_tasks, gantt = fcfs(
            allocated_tasks
        )

    elif scheduling_algorithm == "SJF":

        scheduled_tasks, gantt = sjf(
            allocated_tasks
        )

    elif scheduling_algorithm == "Priority":

        scheduled_tasks, gantt = priority_scheduling(
            allocated_tasks
        )

    else:

        scheduled_tasks, gantt = round_robin(
            allocated_tasks,
            quantum
        )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    metrics = calculate_metrics(
        scheduled_tasks,
        vms
    )


    # -----------------------------------------------------
    # SAVE RESULTS
    # -----------------------------------------------------

    st.session_state["vms"] = vms

    st.session_state["tasks"] = tasks

    st.session_state["scheduled_tasks"] = (
        scheduled_tasks
    )

    st.session_state["waiting_tasks"] = (
        waiting_tasks
    )

    st.session_state["gantt"] = gantt

    st.session_state["metrics"] = metrics

    st.session_state["allocation_log"] = (
        allocation_log
    )

    st.session_state["allocation_algorithm"] = (
        allocation_algorithm
    )

    st.session_state["scheduling_algorithm"] = (
        scheduling_algorithm
    )


# =========================================================
# BEFORE RUNNING
# =========================================================

if "metrics" not in st.session_state:

    st.info(
        "Select the algorithms from the sidebar "
        "and click **Run Simulation**."
    )

    st.markdown(
        """
### Memory Allocation

- **First Fit** → first suitable memory block
- **Best Fit** → smallest suitable memory block
- **Worst Fit** → largest suitable memory block

### CPU Scheduling

- **FCFS**
- **SJF**
- **Priority Scheduling**
- **Round Robin**
        """
    )


# =========================================================
# RESULTS
# =========================================================

else:

    metrics = st.session_state["metrics"]

    vms = st.session_state["vms"]

    tasks = st.session_state["tasks"]

    scheduled_tasks = (
        st.session_state["scheduled_tasks"]
    )

    waiting_tasks = (
        st.session_state["waiting_tasks"]
    )

    gantt = st.session_state["gantt"]

    allocation_log = (
        st.session_state["allocation_log"]
    )

    selected_allocation = (
        st.session_state["allocation_algorithm"]
    )

    selected_scheduling = (
        st.session_state["scheduling_algorithm"]
    )


    # =====================================================
    # CONFIGURATION
    # =====================================================
    st.markdown(
    '<div class="section-title">⚙️ Current Configuration</div>',
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Memory Allocation",
            selected_allocation
        )


    with col2:

        st.metric(
            "CPU Scheduling",
            selected_scheduling
        )


    with col3:

        st.metric(
            "VMs / Tasks",
            f"{len(vms)} / {len(tasks)}"
        )


    # =====================================================
    # PERFORMANCE
    # =====================================================

    st.markdown(
    '<div class="section-title">📊 Performance Summary</div>',
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Waiting Time",
            f"{metrics['avg_waiting']:.2f}"
        )


    with col2:

        st.metric(
            "Average Turnaround Time",
            f"{metrics['avg_turnaround']:.2f}"
        )


    with col3:

        st.metric(
            "Throughput",
            f"{metrics['throughput']:.3f}"
        )


    col4, col5, col6 = st.columns(3)


    with col4:

        st.metric(
            "CPU Utilization",
            f"{metrics['cpu_utilization']:.2f}%"
        )


    with col5:

        st.metric(
            "RAM Utilization",
            f"{metrics['ram_utilization']:.2f}%"
        )


    with col6:

        st.metric(
            "Completed Tasks",
            f"{metrics['completed_tasks']} / {len(tasks)}"
        )


    # =====================================================
    # VM STATUS
    # =====================================================

    st.subheader(
        "🖥️ VM Resource Status"
    )


    vm_rows = []


    for vm in vms:

        used_cpu = (
            vm.total_cpu
            - vm.available_cpu
        )

        used_ram = (
            vm.total_ram
            - vm.available_ram
        )


        cpu_percentage = (
            used_cpu / vm.total_cpu * 100
            if vm.total_cpu
            else 0
        )


        ram_percentage = (
            used_ram / vm.total_ram * 100
            if vm.total_ram
            else 0
        )


        vm_rows.append(
            {
                "VM": vm.vm_id,
                "Total CPU": vm.total_cpu,
                "Used CPU": used_cpu,
                "Available CPU": vm.available_cpu,
                "CPU Usage (%)": round(
                    cpu_percentage,
                    2
                ),
                "Total RAM (GB)": vm.total_ram,
                "Used RAM (GB)": used_ram,
                "Available RAM (GB)": vm.available_ram,
                "RAM Usage (%)": round(
                    ram_percentage,
                    2
                ),
                "Allocated Tasks": len(vm.tasks)
            }
        )


    vm_df = pd.DataFrame(vm_rows)


    st.dataframe(
        vm_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # RAM GRAPH
    # =====================================================

    st.subheader(
        "📈 RAM Utilization"
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    ax.bar(
        vm_df["VM"],
        vm_df["RAM Usage (%)"]
    )


    ax.set_xlabel(
        "Virtual Machines"
    )

    ax.set_ylabel(
        "RAM Usage (%)"
    )

    ax.set_title(
        "Memory Utilization"
    )

    ax.set_ylim(
        0,
        100
    )


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # CPU GRAPH
    # =====================================================

    st.subheader(
        "📈 CPU Utilization"
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    ax.bar(
        vm_df["VM"],
        vm_df["CPU Usage (%)"]
    )


    ax.set_xlabel(
        "Virtual Machines"
    )

    ax.set_ylabel(
        "CPU Usage (%)"
    )

    ax.set_title(
        "CPU Resource Utilization"
    )

    ax.set_ylim(
        0,
        100
    )


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # TASK TABLE
    # =====================================================

    st.subheader(
        "📋 Task Allocation & Scheduling"
    )


    allocation_table = (
        build_allocation_table(tasks)
    )


    allocation_df = pd.DataFrame(
        allocation_table
    )


    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # WAITING TASK WARNING
    # =====================================================

    if waiting_tasks:

        st.warning(
            f"{len(waiting_tasks)} task(s) could not "
            "be allocated to a suitable memory block. "
            "Therefore, they were not entered into "
            "the CPU ready queue."
        )


    # =====================================================
    # ALLOCATION LOG
    # =====================================================

    st.subheader(
        "📝 Memory Allocation Log"
    )


    for message in allocation_log:

        if "WAITING" in message:

            st.warning(message)

        else:

            st.success(message)


    # =====================================================
    # GANTT CHART
    # =====================================================

    st.subheader(
        "📊 CPU Scheduling Gantt Chart"
    )


    if gantt:

        fig, ax = plt.subplots(
            figsize=(12, 4)
        )


        for item in gantt:

            ax.barh(
                0,
                item["duration"],
                left=item["start"],
                height=0.5
            )


            center = (
                item["start"]
                + item["duration"] / 2
            )


            ax.text(
                center,
                0,
                item["task"],
                ha="center",
                va="center"
            )


        ax.set_xlabel(
            "Time"
        )

        ax.set_yticks([])

        ax.set_title(
            f"{selected_scheduling} CPU Scheduling"
        )


        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.4
        )


        st.pyplot(fig)

        plt.close(fig)


    # =====================================================
    # SCHEDULING ORDER
    # =====================================================

    st.subheader(
        "🔄 Scheduling Order"
    )


    if scheduled_tasks:

        order = [
            task.task_id
            for task in scheduled_tasks
        ]

        st.write(
            " → ".join(order)
        )


    # =====================================================
    # EXPLANATION
    # =====================================================

    st.subheader(
        "📚 Algorithm Explanation"
    )


    st.markdown(
        """
### Memory Allocation

**First Fit**

Search memory blocks from the beginning
and allocate the first block large enough.

**Best Fit**

Search all suitable memory blocks and
allocate the smallest block that can satisfy
the memory requirement.

**Worst Fit**

Search all suitable memory blocks and
allocate the largest block available.

In this simulator:

> **VM RAM = OS memory block**

CPU availability is checked as an additional
resource constraint, but the fit decision is
based on RAM.

### CPU Scheduling

**FCFS:** Processes execute according to arrival order.

**SJF:** The available process with the shortest
burst time executes first.

**Priority:** The available process with the highest
priority executes first. Smaller priority number
means higher priority.

**Round Robin:** Each ready process receives a fixed
time quantum in circular order.
"""
    )


    # =====================================================
    # COMPLETION
    # =====================================================

    st.subheader(
        "✅ Simulation Completed"
    )


    st.write(
        "The simulator demonstrates standard OS "
        "memory allocation and CPU scheduling "
        "algorithms using cloud VMs as the "
        "simulation environment."
    )