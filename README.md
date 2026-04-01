# Welcome to Artificial Bee Colony (ABC) Optimizer 🐝

Welcome to the **ArtificialBeeColony** repository. This is a Python implementation of the Artificial Bee Colony (ABC) optimization algorithm. Designed as a **bio-inspired** meta-heuristic, it simulates the intelligent foraging behavior of a honey bee swarm to solve complex, constrained non-linear optimization problems and find global minimums or maximums efficiently.

---

## 📚 About The Project

| Feature                | Details |
| ---------------------- | ------- |
| 🎯 **Purpose** | A robust, **bio-inspired** meta-heuristic platform to optimize complex mathematical functions subject to multiple equality and inequality constraints. |
| ⚙️ **Architecture** | Object-Oriented Python design encapsulating the algorithm's state within the `ABC` class. |
| 🧮 **Data Management** | High-performance matrix operations, random sampling, and array manipulations powered by `NumPy`. |
| 🔄 **Core Operations** | Employed bee exploration, onlooker bee probabilistic selection (Waggle Dance), scout bee random search, and Deb's feasibility rules for constraint handling. |

---

## 🚀 Tech Stack

### Language & Libraries

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

- **Python:** The core scripting language handling the logical flow and object-oriented structure.
- **NumPy:** Utilized extensively for generating initial multidimensional populations, vectorized boundary corrections, and calculating fitness values rapidly across large swarms.

---

## 🔧 Highlighted Features

| Feature | Description |
|--------|------------|
| **Employed Bee Phase** | Searches for new food sources (solutions) in the neighborhood of their current positions and evaluates their nectar amount (fitness). |
| **Onlooker Bee Phase** | Simulates the "Waggle Dance." Bees probabilistically select food sources based on the fitness information shared by employed bees. |
| **Scout Bee Phase** | Prevents the algorithm from getting stuck in local optima. If a food source is not improved after a certain `limit`, it is abandoned and replaced with a randomly generated new source. |
| **Deb's Feasibility Rules** | Advanced constraint handling using a Sum of Constraint Violation (SVR) approach. It dynamically compares solutions prioritizing feasibility over raw fitness when constraints are violated. |
| **Dynamic Boundaries** | Automatic handling and correction of upper and lower limits for variables to ensure the search space remains valid. |

---

## 📐 Default Optimization Problem

By default, the script is configured to solve a specific constrained non-linear problem with 4 variables and an $\epsilon$ tolerance for equality constraints.

The objective function evaluated is:

f(x) = 3x₁ + 0.000001x₁³ + 2x₂ + (0.000002/3)x₂³

Subject to the constraints:

- g₁(x) = -x₄ + x₃ - 0.55 ≤ 0  
- g₂(x) = -x₃ + x₄ - 0.55 ≤ 0  
- h₃(x) = 1000 sin(-x₃ - 0.25) + 1000 sin(-x₄ - 0.25) + 894.8 - x₁ = 0  
- h₄(x) = 1000 sin(x₃ - 0.25) + 1000 sin(x₃ - x₄ - 0.25) + 894.8 - x₂ = 0  
- h₅(x) = 1000 sin(x₄ - 0.25) + 1000 sin(x₄ - x₃ - 0.25) + 1294.8 = 0  

*(You can modify the `fobjective` method inside the `ABC` class to optimize your own custom functions).*

---

## 🛠️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/MexboxLuis/ArtificialBeeColony.git
cd ArtificialBeeColony
```

### 2. Install Dependencies

```bash
pip install numpy
```

### 3. Run the Script

```bash
python ArtificialBeeColony.py
```

### 4. Adjusting Parameters

```python
MCN = 5000          # Maximum Cycle Number (Iterations)
nvar = 4            # Number of variables
SN = 30             # Swarm Size (Number of food sources)
epsilon = 0.001     # Tolerance for equality constraints

Ub = np.array([1200, 1200, 0.55, 0.55]) # Upper bounds
Lb = np.array([0, 0, -0.55, -0.55])     # Lower bounds
```
