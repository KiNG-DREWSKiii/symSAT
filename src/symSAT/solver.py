# solver.py
import itertools
import math
from typing import List, Tuple, Dict, Set

Clause = List[int]
Formula = List[Clause]
Assignment = List[int]  # 1 = True, 0 = False

def evaluate_clause(clause: Clause, assignment: Assignment) -> bool:
    return any((assignment[abs(lit) - 1] == (1 if lit > 0 else 0)) for lit in clause)

def evaluate_formula(formula: Formula, assignment: Assignment) -> bool:
    return all(evaluate_clause(clause, assignment) for clause in formula)

def generate_symmetry_class(n: int, k: int) -> List[Assignment]:
    configs = []
    indices = list(range(n))
    for majority_value in [1, 0]:
        minority_value = 1 - majority_value
        for flip_indices in itertools.combinations(indices, k):
            assignment = [majority_value] * n
            for idx in flip_indices:
                assignment[idx] = minority_value
            configs.append(assignment)
    return configs

def jump_size(n: int, k: int) -> int:
    return math.ceil(math.log2(n - k + 1))

def clause_activation_profile(formula: Formula, assignments: List[Assignment]) -> Set[int]:
    active_clauses = set()
    for i, clause in enumerate(formula):
        satisfied_count = sum(evaluate_clause(clause, a) for a in assignments)
        if satisfied_count > len(assignments) // 2:
            active_clauses.add(i)
    return active_clauses

def get_hamming_neighbors(config: Assignment) -> List[Assignment]:
    neighbors = []
    for i in range(len(config)):
        neighbor = config[:]
        neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def backflow(formula: Formula, solution: Assignment, visited: Set[Tuple[int]], max_layers: int = 4) -> Tuple[bool, Assignment]:
    current_layer = [solution]
    previous_cap = clause_activation_profile(formula, current_layer)
    for _ in range(max_layers):
        next_layer = []
        for config in current_layer:
            for neighbor in get_hamming_neighbors(config):
                key = tuple(neighbor)
                if key in visited:
                    continue
                visited.add(key)
                if evaluate_formula(formula, neighbor):
                    return True, neighbor
                next_layer.append(neighbor)
        if not next_layer:
            break
        new_cap = clause_activation_profile(formula, next_layer)
        if new_cap == previous_cap:
            break
        previous_cap = new_cap
        current_layer = next_layer
    return False, []

def symmetry_solver(formula: Formula, n: int, max_sink: int = 3) -> Tuple[bool, Assignment, Dict]:
    visited = set()
    stats = {"evaluated": 0, "symmetry_levels": [], "jumps": 0, "backflows": 0}
    k = 1
    sink_count = 0
    while k <= n:
        stats["symmetry_levels"].append(k)
        configs = generate_symmetry_class(n, k)
        for config in configs:
            config_key = tuple(config)
            if config_key in visited:
                continue
            visited.add(config_key)
            stats["evaluated"] += 1
            if evaluate_formula(formula, config):
                stats["backflows"] += 1
                back_solved, recovered = backflow(formula, config, visited)
                return True, recovered if back_solved else config, stats
        sink_count += 1
        if sink_count >= max_sink:
            j = jump_size(n, k)
            k += j
            stats["jumps"] += 1
            sink_count = 0
        else:
            k += 1
    return False, [], stats

def brute_force_solver(formula: Formula, n: int) -> Tuple[bool, Assignment, Dict]:
    stats = {"evaluated": 0}
    for bits in itertools.product([0, 1], repeat=n):
        stats["evaluated"] += 1
        if evaluate_formula(formula, list(bits)):
            return True, list(bits), stats
    return False, [], stats
