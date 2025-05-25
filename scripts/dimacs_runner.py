# dimacs_runner.py
import os
import time
from solver import symmetry_solver, brute_force_solver, Formula


def load_dimacs(path: str) -> Formula:
    if not os.path.exists(path):
        raise FileNotFoundError(f"DIMACS file not found: {path}")
    formula = []
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('p') or line.startswith('c') or not line:
                    continue
                try:
                    clause = [int(x) for x in line.split() if int(x) != 0]
                    formula.append(clause)
                except ValueError:
                    print(f"Warning: Skipping invalid line: {line}")
        if not formula:
            raise ValueError("No valid clauses found in file")
        return formula
    except Exception as e:
        raise Exception(f"Error reading DIMACS file: {e}")


def run_dimacs_benchmark(filepath: str):
    formula = load_dimacs(filepath)
    n_vars = max(abs(lit) for clause in formula for lit in clause)

    print(
        f"\nRunning: {os.path.basename(filepath)} | Variables: {n_vars} | Clauses: {len(formula)}"
    )

    start = time.time()
    solved_sym, sol_sym, stats_sym = symmetry_solver(formula, n_vars)
    time_sym = round(time.time() - start, 4)

    start = time.time()
    solved_bf, sol_bf, stats_bf = brute_force_solver(formula, n_vars)
    time_bf = round(time.time() - start, 4)

    print("--- Symmetry Solver ---")
    print("Solved:", solved_sym)
    print("Evaluated:", stats_sym["evaluated"])
    print("Time:", time_sym)

    print("--- Brute Force Solver ---")
    print("Solved:", solved_bf)
    print("Evaluated:", stats_bf["evaluated"])
    print("Time:", time_bf)


def run_all_in_dir(directory: str):
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Directory not found: {directory}")
    cnf_files = [
        f for f in sorted(os.listdir(directory)) if f.endswith('.cnf')
    ]
    if not cnf_files:
        raise FileNotFoundError(f"No .cnf files found in {directory}")

    total_sym_time = 0
    total_bf_time = 0
    total_files = len(cnf_files)

    for filename in cnf_files:
        formula = load_dimacs(os.path.join(directory, filename))
        n_vars = max(abs(lit) for clause in formula for lit in clause)

        print(
            f"\nRunning: {filename} | Variables: {n_vars} | Clauses: {len(formula)}"
        )

        start = time.time()
        solved_sym, _, stats_sym = symmetry_solver(formula, n_vars)
        time_sym = time.time() - start
        total_sym_time += time_sym

        start = time.time()
        solved_bf, _, stats_bf = brute_force_solver(formula, n_vars)
        time_bf = time.time() - start
        total_bf_time += time_bf

        print("--- Symmetry Solver ---")
        print("Solved:", solved_sym)
        print("Evaluated:", stats_sym["evaluated"])
        print("Time:", round(time_sym, 4))

        print("--- Brute Force Solver ---")
        print("Solved:", solved_bf)
        print("Evaluated:", stats_bf["evaluated"])
        print("Time:", round(time_bf, 4))

    print("\n" + "=" * 50)
    print("=== Overall Statistics ===")
    print("=" * 50)
    print(f"Total files processed: {total_files}")
    print(
        f"Average Symmetry Solver time: {round(total_sym_time/total_files, 4)}s"
    )
    print(f"Average Brute Force time: {round(total_bf_time/total_files, 4)}s")
    print(f"Total time - Symmetry: {round(total_sym_time, 4)}s")
    print(f"Total time - Brute Force: {round(total_bf_time, 4)}s")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 dimacs_runner.py dimacs/")
    else:
        run_all_in_dir(sys.argv[1])
