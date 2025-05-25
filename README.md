# SymmetrySAT

**SymmetrySAT** is a symmetry-aware SAT solver designed to reduce search space through structured configuration pruning and backflow recovery. Built for logic verification, constraint solving, and hybrid neuro-symbolic applications, it provides a unique approach to accelerating and simplifying SAT-based workflows.

---

## 🔍 What It Does

- Uses **symmetry class pruning** to skip redundant logic configurations
- Applies **backflow repair** to recover skipped solutions when necessary
- Compares performance directly against brute-force solving
- Supports **DIMACS CNF format** (standard in SAT benchmarks)
- Benchmarks and logs solver stats for analysis and visualization

---

## ⚙️ Features

- CLI-based solver (`dimacs_runner.py`)
- Scalable to ~20-variable problems in raw Python
- Optimized for structured logic (e.g., mirrored or repeated subcircuits)
- Helpful for constraint-heavy systems, digital logic verification, and symbolic AI

---

## 📂 Folder Structure

symSAT/
├── data/ # SAT problem files (.cnf)
├── results/ # Optional: benchmark results
├── scripts/
│ └── dimacs_runner.py # CLI runner for symmetry vs brute-force comparison
├── src/
│ └── symSAT/
│ └── solver.py # Core symmetry SAT algorithm
├── README.md
├── MIT License


---

## 🧪 Example Run


cd scripts/
python3 dimacs_runner.py ../data/uf20-01.cnf
