import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from algorithm import topological_sort

st.set_page_config(page_title="Job Scheduling Using Graph", page_icon="🗂️", layout="wide")

st.title("🗂️ Job Scheduling Using Graph")
st.write("Add jobs and dependencies, visualize the graph, and calculate a valid execution order using topological sorting.")

if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "dependencies" not in st.session_state:
    st.session_state.dependencies = []

def load_sample():
    st.session_state.jobs = [
        "Requirements", "Frontend", "Backend", "Integration", "Deployment"
    ]
    st.session_state.dependencies = [
        ("Requirements", "Frontend"),
        ("Requirements", "Backend"),
        ("Frontend", "Integration"),
        ("Backend", "Integration"),
        ("Integration", "Deployment"),
    ]

def clear_all():
    st.session_state.jobs = []
    st.session_state.dependencies = []

left, right = st.columns([1, 1])

with left:
    st.subheader("1. Manage Jobs")
    with st.form("add_job_form", clear_on_submit=True):
        new_job = st.text_input("Job name", placeholder="e.g. Testing")
        add_job_clicked = st.form_submit_button("Add Job")
    if add_job_clicked:
        name = new_job.strip()
        if not name:
            st.warning("Please enter a job name.")
        elif name in st.session_state.jobs:
            st.warning("This job already exists.")
        else:
            st.session_state.jobs.append(name)
            st.success(f"Added job: {name}")

    if st.session_state.jobs:
        remove_job = st.selectbox("Choose a job to remove", ["— Select —"] + st.session_state.jobs)
        if st.button("Remove Selected Job") and remove_job != "— Select —":
            st.session_state.jobs.remove(remove_job)
            st.session_state.dependencies = [
                (a, b) for a, b in st.session_state.dependencies
                if a != remove_job and b != remove_job
            ]
            st.rerun()
    else:
        st.caption("No jobs added yet.")

with right:
    st.subheader("2. Add Dependencies")
    if len(st.session_state.jobs) >= 2:
        with st.form("dependency_form", clear_on_submit=True):
            prerequisite = st.selectbox("Prerequisite (must happen first)", st.session_state.jobs)
            dependent = st.selectbox("Job that follows", st.session_state.jobs, index=1 if len(st.session_state.jobs) > 1 else 0)
            add_dep_clicked = st.form_submit_button("Add Dependency")
        if add_dep_clicked:
            if prerequisite == dependent:
                st.error("A job cannot depend on itself.")
            elif (prerequisite, dependent) in st.session_state.dependencies:
                st.warning("This dependency already exists.")
            else:
                st.session_state.dependencies.append((prerequisite, dependent))
                st.success(f"Added dependency: {prerequisite} → {dependent}")
    else:
        st.caption("Add at least two jobs to create a dependency.")

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Load Sample Project", use_container_width=True):
        load_sample()
        st.rerun()
with col_b:
    if st.button("Clear All", use_container_width=True):
        clear_all()
        st.rerun()

st.divider()
st.subheader("3. Jobs and Dependencies")
if st.session_state.jobs:
    st.write("**Jobs:** " + ", ".join(st.session_state.jobs))
else:
    st.info("Add a job or click 'Load Sample Project' to get started.")

if st.session_state.dependencies:
    st.write("**Dependencies:**")
    for before, after in st.session_state.dependencies:
        st.write(f"- {before} → {after}")
else:
    st.caption("No dependencies have been added.")

st.subheader("4. Graph Diagram")
if st.session_state.jobs:
    graph = nx.DiGraph()
    graph.add_nodes_from(st.session_state.jobs)
    graph.add_edges_from(st.session_state.dependencies)

    fig, ax = plt.subplots(figsize=(10, 5))
    pos = nx.spring_layout(graph, seed=7)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=2600)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=9)
    nx.draw_networkx_edges(
        graph, pos, ax=ax, arrows=True, arrowstyle="-|>",
        arrowsize=20, connectionstyle="arc3,rad=0.06",
        node_size=2600
    )
    ax.set_axis_off()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.caption("The graph diagram will appear here after you add jobs.")

st.subheader("5. Scheduling Result")
if st.button("Schedule Jobs", type="primary"):
    try:
        schedule = topological_sort(st.session_state.jobs, st.session_state.dependencies)
    except ValueError as error:
        st.error(str(error))
    else:
        if not st.session_state.jobs:
            st.info("No jobs to schedule.")
        elif schedule is None:
            st.error("Cycle detected! No valid schedule is possible.")
        else:
            st.success("Valid Job Execution Order")
            for index, job in enumerate(schedule, start=1):
                st.write(f"{index}. {job}")

st.caption("Built with Python, Streamlit, NetworkX, and topological sorting.")
