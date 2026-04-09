import subprocess
import os
import glob
import tempfile

# Chemin vers ton downward
FD_PATH = "/home/joan/downward/fast-downward.py" 

def solve_pddl(domain_path, problem_path):
    """ Exécute Fast-Downward et retourne une liste d'actions """
    
    if not os.path.exists(problem_path) or os.path.getsize(problem_path) == 0:
        return []

    abs_domain_path = os.path.abspath(domain_path)
    abs_problem_path = os.path.abspath(problem_path)

    # Commande compatible avec cette version de Fast-Downward
    cmd = ["python3", FD_PATH, abs_domain_path, abs_problem_path, "--search", "astar(blind())"]

    with tempfile.TemporaryDirectory(prefix="fd_run_") as temp_dir:
        try:
            subprocess.run(cmd, check=True, capture_output=True, cwd=temp_dir, text=True)
        except subprocess.CalledProcessError:
            return []

        # Lecture du résultat (sas_plan ou sas_plan.N)
        actions = []
        plan_files = sorted(glob.glob(os.path.join(temp_dir, "sas_plan*")))
        if plan_files:
            with open(plan_files[-1], "r") as f:
                for line in f:
                    if line.startswith(";"):
                        continue

                    clean = line.strip().replace("(", "").replace(")", "").split()
                    if clean:
                        actions.append(clean)

        return actions
