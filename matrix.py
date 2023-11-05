import numpy as np
from scipy.optimize import linprog

def matrix(products_list, milk, fat, product_bounds):
    ingredients = np.empty((0,2))
    profit_margins = []
    names = []
    
    for product in products_list:
        skimmed_milk_quantity, fat_quantity = [float(product[1])*float(product[3]), float(product[2])*float(product[3])]
        arr = np.array([[skimmed_milk_quantity, fat_quantity]])
        ingredients = np.append(ingredients, arr, axis=0)
        profit_margins.append(product[7])
        names.append(product[0]) 

    budget_constraint = [milk, fat]

    # The coefficients for the linear programming problem
    c = -np.array(profit_margins)  # Negate the profit margins to maximize profits
    A = ingredients.T  # Transpose the ingredient matrix to set up inequality constraints
    b = budget_constraint

    # Set bounds for each product quantity (non-negative)
    #bounds = [(0, None)] * len(profit_margins)
    bounds = product_bounds

    # Solve the linear programming problem to maximize the profit
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if result.success:
        #print("Ապրանքների առավել շահավետ համադրություն.")
        i = 0
        reqmilk = 0
        reqfat = 0
        quantitys = []
        for i, quantity in enumerate(result.x):
            if quantity > 0:
                quantitys.append([names[i], round(quantity)])
            #print(names[i], ' -', quantity, ' հատ')
            if quantity > 0:
                reqmilk = reqmilk + products_list[i][1] * products_list[i][3] * quantity
                reqfat = reqfat + products_list[i][2] * products_list[i][3] * quantity
            i = i + 1
        #print(f"Ընդհանուր շահույթ: {-result.fun:.2f} դրամ")
        profit = -result.fun
        profit = round(profit)
        #print("Մնացորդ զտած կաթ։")
        #print(milk - reqmilk)
        milkbalance = milk - reqmilk
        if milkbalance < 0.000001 and milkbalance > -0.01:
            milkbalance = 0
        #print("Մնացորդ յուղ։")
        #print(fat - reqfat)
        fatbalance = fat - reqfat
        if fatbalance < 0.0000001 and fatbalance > -0.01:
            fatbalance = 0
        
        return quantitys, profit, milkbalance, fatbalance
        
    else:
        print("Optimization failed due to lack of ingredients.")
        
        quantitys = ["00"]
        profit = 0
        milkbalance = milk
        fatbalance = fat
        # Identify which ingredients are causing the infeasibility and calculate the shortfall
        lack = []
        lacking_ingredients = []
        shortfall_info = []  # Store tuples of (ingredient_idx, shortfall)
        for ingredient_idx in range(len(b)):
            ingredient_usage = np.dot(A[ingredient_idx], product_bounds)
            shortfall = ingredient_usage - b[ingredient_idx]
            if np.any(shortfall > 0):
                lacking_ingredients.append(ingredient_idx)
                shortfall_info.append((ingredient_idx, shortfall))
    
        for ingredient_idx, shortfall_array in shortfall_info:
            if shortfall_array[0] > 0:
                shortfall_str = shortfall_array[0]
                lack.append((str(ingredient_idx + 1), shortfall_str))
                print(f"Ingredient {ingredient_idx + 1} is lacking by {shortfall_str}")
        
        # Binary search to find alternative combination of products
        alternative_ingredient_limits = b.copy()
        lower_bounds = np.zeros(len(b))
        upper_bounds = shortfall.copy()  # Start with shortfall as the upper bound
    
        for _ in range(10):  # Perform a few iterations of binary search
            mid_bounds = (lower_bounds + upper_bounds) / 2
            alternative_ingredient_limits = b + mid_bounds
        
            # Solve the linear programming problem with alternative ingredient limits
            alternative_result = linprog(c, A_ub=A, b_ub=alternative_ingredient_limits, bounds=product_bounds, method='highs')
        
            if alternative_result.success:
                print("Alternative combination of products:", alternative_result.x)
                print("Maximized profit:", -alternative_result.fun)
                break  # Found a feasible solution
            else:
               # Update bounds based on feasibility
                for i in lacking_ingredients:
                    if np.any(np.dot(A[i], product_bounds) > alternative_ingredient_limits[i]):
                        lower_bounds[i] = mid_bounds[i]
                    else:
                        upper_bounds[i] = mid_bounds[i]
        
        print("Օպտիմազացումը ձախողվեց: Ստուգեք, արդյոք սահմանափակումները հնարավոր են:")
        
        return quantitys, profit, milkbalance, fatbalance, lack