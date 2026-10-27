import tkinter as tk
from tkinter import messagebox, simpledialog
from algorithm import topological_sort


class JobSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Implementation of Job Scheduling Using Graph")
        self.root.geometry("750x550")

        self.jobs = []
        self.dependencies = []

        tk.Label(
            root,
            text="Job Scheduling Using Graph",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        buttons = tk.Frame(root)
        buttons.pack(pady=8)

        tk.Button(
            buttons, text="Add Job", width=14,
            command=self.add_job
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons, text="Remove Job", width=14,
            command=self.remove_job
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            buttons, text="Add Dependency", width=14,
            command=self.add_dependency
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            buttons, text="Schedule Jobs", width=14,
            command=self.schedule_jobs
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            buttons, text="Load Sample", width=14,
            command=self.load_sample
        ).grid(row=1, column=0, padx=5, pady=8)

        tk.Button(
            buttons, text="Clear All", width=14,
            command=self.clear_all
        ).grid(row=1, column=1, padx=5, pady=8)

        tk.Label(
            root, text="Jobs and Dependencies",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.job_list = tk.Listbox(root, width=85, height=8)
        self.job_list.pack(padx=15, pady=5)

        tk.Label(
            root, text="Scheduling Result",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.result = tk.Text(root, width=85, height=8)
        self.result.pack(padx=15, pady=5)

    def refresh_jobs(self):
        self.job_list.delete(0, tk.END)

        for job in self.jobs:
            self.job_list.insert(tk.END, f"Job: {job}")

        for before, after in self.dependencies:
            self.job_list.insert(
                tk.END, f"Dependency: {before} -> {after}"
            )

    def add_job(self):
        job = simpledialog.askstring("Add Job", "Enter job name:")

        if job:
            job = job.strip()

            if not job:
                return

            if job in self.jobs:
                messagebox.showwarning(
                    "Duplicate Job", "This job already exists."
                )
                return

            self.jobs.append(job)
            self.refresh_jobs()

    def remove_job(self):
        selection = self.job_list.curselection()

        if not selection:
            messagebox.showinfo(
                "Select Job", "Select a job from the list first."
            )
            return

        selected_text = self.job_list.get(selection[0])

        if not selected_text.startswith("Job: "):
            messagebox.showinfo(
                "Select Job", "Please select a job, not a dependency."
            )
            return

        job = selected_text[5:]
        self.jobs.remove(job)
        self.dependencies = [
            (a, b) for a, b in self.dependencies
            if a != job and b != job
        ]
        self.refresh_jobs()

    def add_dependency(self):
        if len(self.jobs) < 2:
            messagebox.showinfo(
                "Add Jobs", "Add at least two jobs first."
            )
            return

        before = simpledialog.askstring(
            "Dependency", "Enter prerequisite job name:"
        )
        if not before:
            return

        after = simpledialog.askstring(
            "Dependency", "Enter dependent job name:"
        )
        if not after:
            return

        before = before.strip()
        after = after.strip()

        if before not in self.jobs or after not in self.jobs:
            messagebox.showerror(
                "Invalid Job", "Both jobs must exist in the job list."
            )
            return

        if before == after:
            messagebox.showerror(
                "Invalid Dependency", "A job cannot depend on itself."
            )
            return

        if (before, after) in self.dependencies:
            messagebox.showwarning(
                "Duplicate", "This dependency already exists."
            )
            return

        self.dependencies.append((before, after))
        self.refresh_jobs()

    def schedule_jobs(self):
        self.result.delete("1.0", tk.END)

        try:
            schedule = topological_sort(
                self.jobs, self.dependencies
            )
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        if schedule is None:
            self.result.insert(
                tk.END,
                "Cycle detected! No valid schedule is possible."
            )
        elif not schedule:
            self.result.insert(tk.END, "No jobs to schedule.")
        else:
            self.result.insert(
                tk.END,
                "Valid Job Execution Order:\n\n"
                + "\n".join(
                    f"{i + 1}. {job}"
                    for i, job in enumerate(schedule)
                )
            )

    def load_sample(self):
        self.jobs = [
            "Requirements",
            "Frontend",
            "Backend",
            "Integration",
            "Deployment"
        ]

        self.dependencies = [
            ("Requirements", "Frontend"),
            ("Requirements", "Backend"),
            ("Frontend", "Integration"),
            ("Backend", "Integration"),
            ("Integration", "Deployment")
        ]

        self.refresh_jobs()
        self.result.delete("1.0", tk.END)

    def clear_all(self):
        self.jobs.clear()
        self.dependencies.clear()
        self.refresh_jobs()
        self.result.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = JobSchedulingApp(root)
    root.mainloop()