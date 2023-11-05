import numpy as np
from scipy.optimize import linprog

# Define the ingredient matrix
# Each row represents a product, and each column represents an ingredient
ingredients = np.array([
    [0.224, 0.0048], # Թան 0.32լ
    [0.045,0.0009], # Թթվասեր 0.09կգ 18%
    [0.09, 0.018], # Թթվասեր 0.18կգ
    [0.175, 0.0035], # Թթվասեր 0.35կգ
    [0.475, 0.0095], # Կաթ մանրէազերծված 2.5% 0,95 լ
    [0.375, 0.0075], # Կաթ մանրէազերծված 3.2% 0,75 լ
    [0.65, 0.0018], # Կաթնաշոռ 0.10կգ 9.0%
    [1.296, 0.00324], # Կաթնաշոռ 0.18կգ 0․5%
    [1.17, 0.00324], # Կաթնաշոռ 0.18կգ 9%
    [0.225, 0.0045], # Մածուն 0.45լ 1.5%
    [0.225, 0.0045], # Մածուն 0.45կգ 2.5%
    [0.425, 0.0085], # Մածուն 0.85կգ 2.5%
    [0.7, 0.005], # Մածուն քամած 0.2կգ
    [0.075, 0.0015], # Ռեժան "Սյունիք" 60%, 150գ
    [2.75, 0.0125], # Ցխաթան "Սյունիք" 7%, 500գ
    [4.95, 0.0225] # Ցխաթան "Սյունիք" 7%, 900գ
])

print(ingredients)

# Define the profit margins for each product
# The profit margins are in the same order as the ingredients array.
profit_margins = [
    82.6308, 
    136.076, 
    264.152, 
    472.95, 
    315.93, 
    481.55, 
    171.91, 
    221.578, 
    304.138, 
    152.06, 
    183.23, 
    310.82, 
    217.25, 
    590.07, 
    907.045, 
    1778.705
]

# Define the budget constraint (maximum total ingredient quantity available)
budget_constraint = [3939, 147]

# The coefficients for the linear programming problem
c = -np.array(profit_margins)  # Negate the profit margins to maximize profits
A = ingredients.T  # Transpose the ingredient matrix to set up inequality constraints
b = budget_constraint

# Set bounds for each product quantity (non-negative)
bounds = [(0, None)] * len(profit_margins)

# Solve the linear programming problem to maximize the profit
result = linprog(c, A_ub=A, b_ub=b, bounds=bounds)

if result.success:
    print("Most profitable combination of products:")
    for i, quantity in enumerate(result.x):
        print(f"Product {i+1}: {quantity} units")
    print(f"Total profit: {-result.fun:.2f}")
else:
    print("Optimization failed. Check if constraints are feasible.")