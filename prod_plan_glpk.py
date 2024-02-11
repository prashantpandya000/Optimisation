import streamlit as st
import pandas as pd
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory




def optimise_fun(production_names,distribution_names,cost_data):
    max_prod = pd.Series([180,200], index = production_names, name = "max_production")
    n_demand = pd.Series([89,95], index = distribution_names, name = "demand") 
    st.text(f'Max Production:\n {max_prod}')
    st.text(f'Demand:\n {n_demand}')

    frac = 0.75
    m = ConcreteModel()
    m.x = Var(production_names, distribution_names, domain=NonNegativeReals)

    # Define objective function
    m.objective = Objective(
        expr=sum(cost_data.loc[p, d] * m.x[p, d] for p in production_names for d in distribution_names),
        sense=minimize
    )

    # Define constraints
    m.meet_demand = ConstraintList()
    for d in distribution_names:
        m.meet_demand.add(
            sum(m.x[p, d] for p in production_names) >= n_demand[d]
        )

    m.can_produce = ConstraintList()
    for p in production_names:
        m.can_produce.add(
            sum(m.x[p, d] for d in distribution_names) <= max_prod[p]
        )

    m.must_produce = ConstraintList()
    for p in production_names:
        m.must_produce.add(
            sum(m.x[p, d] for d in distribution_names) >= frac * max_prod[p]
        )

    # Solve the optimization problem
    solver = SolverFactory('glpk')
    solver.solve(m)

    # Extract solution
    x_values = pd.DataFrame([[value(m.x[p, d]) for d in distribution_names] for p in production_names],
                            index=production_names,
                            columns=distribution_names)
    sol = pd.concat([cost_data, x_values], axis=1)
    return sol[sol.gt(0).any(axis=1)]
    




def main():
    st.title("Production planning")

    # Get number of production items and distribution points
    num_productions = st.number_input("Enter the number of production items:", min_value=1, step=1)
    num_distributions = st.number_input("Enter the number of distribution points:", min_value=1, step=1)

    # Collect production and distribution names
    production_names = [st.text_input(f"Enter name for Production Item {i}:") for i in range(1, num_productions + 1)]
    distribution_names = [st.text_input(f"Enter name for Distribution Point {j}:") for j in range(1, num_distributions + 1)]

    # Create an empty DataFrame
    cost_data = pd.DataFrame(index=production_names, columns=distribution_names)

    # Display the form for editing cost data
    with st.form(key='edit_form'):
        for prod_name in production_names:
            for dist_name in distribution_names:
                key = f"{prod_name}_{dist_name}"
                cost_value = st.number_input(f"Enter cost for {prod_name} x {dist_name}:", min_value=0.0, key=key, format="%.1f")
                cost_data.loc[prod_name, dist_name] = cost_value

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.write("Cost Data:", cost_data)
    # cost_data.reset_index().pivot(index='production', columns='distribution', values='cost')
    output=optimise_fun(production_names,distribution_names,cost_data)
    st.text(f'Optimal Production Plan:\n {output}')

if __name__ == "__main__":
    main()