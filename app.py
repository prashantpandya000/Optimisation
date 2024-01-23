import streamlit as st
from pulp import *

# Function to define and solve the production planning problem
def optimize_production_planning(target_profit, resource_constraint, demand_product1, demand_product2):
    # Define the problem
    prob = LpProblem("ProductionPlanning", LpMaximize)

    # Decision variables
    x1 = LpVariable("Product1_units", lowBound=0, cat='Integer')
    x2 = LpVariable("Product2_units", lowBound=0, cat='Integer')

    # Objective function (maximize profit)
    prob += 40 * x1 + 30 * x2, "Total_Profit"

    # Resource constraint
    prob += 2 * x1 + 3 * x2 <= resource_constraint, "Resource_Constraint"

    # Demand constraints
    prob += x1 >= demand_product1, "Demand_Product1"
    prob += x2 >= demand_product2, "Demand_Product2"

    # Solve the problem
    prob.solve()

    # Display results
    st.write("Status:", LpStatus[prob.status])
    st.write("Optimal Production Plan:")
    st.write(f"Produce {value(x1)} units of Product 1 (Meeting demand: {demand_product1} units)")
    st.write(f"Produce {value(x2)} units of Product 2 (Meeting demand: {demand_product2} units)")
    st.write("Total Profit: $", value(prob.objective))

# Streamlit app
def main():
    st.title("Production Planning with PuLP and Streamlit")

    # User inputs
    target_profit = st.number_input("Enter the target profit:", value=0, step=10)
    resource_constraint = st.number_input("Enter the resource constraint:", value=0, step=10)
    demand_product1 = st.number_input("Enter the demand for Product 1:", value=0, step=10)
    demand_product2 = st.number_input("Enter the demand for Product 2:", value=0, step=10)

    # Button to run optimization
    if st.button("Optimize"):
        # Call the optimization function
        optimize_production_planning(target_profit, resource_constraint, demand_product1, demand_product2)

if __name__ == "__main__":
    main()


