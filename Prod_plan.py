import streamlit as st
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

def optimise_fun(production_names,distribution_names,cost_data):
    max_prod = pd.Series([180,200], index = production_names, name = "max_production")
    n_demand = pd.Series([89,95], index = distribution_names, name = "demand") 

    frac = 0.75

# loop through each p and d combination to create a decision variable
    m = gp.Model('Production planning')
    x={}
    for p in production_names:
        for d in distribution_names:
            x[p,d]=m.addVar(name=p+"_to_"+d)
    st.dataframe(x)


# Provide each set for the indices 
    m = gp.Model('Production planning')
    x=m.addVars(production_names,distribution_names,name="prod_ship")

# The index of the tranporation costs have each combination of prodiction and distribution location
    m = gp.Model('Production planning')
    x=m.addVars(cost_data.index,name="prod_ship")
    
    meet_demand=m.addConstrs((gp.quicksum(x[p,d] for p in production_names) >= n_demand[d] for d in distribution_names),name="meet_demand")
    m.update()



    can_produce = m.addConstrs((gp.quicksum(x[p,d] for d in distribution_names)<= max_prod[p] for p in production_names),
                           name="can produce")
    must_produce = m.addConstrs((gp.quicksum(x[p,d] for d in distribution_names)>= frac*max_prod[p] for p in production_names),
                           name="must produce")



    m.setObjective(gp.quicksum(cost_data[p,d]*x[p,d] for p in production_names for d in distribution_names),GRB.MINIMIZE)

    m.write('widget_shipment.lp')
    m.optimize()

    x_values = pd.Series(m.getAttr('X', x), name = "shipment", index = cost_data.index)
    sol = pd.concat([cost_data, x_values], axis=1)
    return sol[sol.shipment > 0]


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
                cost_value = st.number_input(f"Enter cost for {prod_name} x {dist_name}:", min_value=0.0, key=key, format="%.2f")
                cost_data.loc[prod_name, dist_name] = cost_value

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.write("Cost Data:", cost_data)
    # cost_data.reset_index().pivot(index='production', columns='distribution', values='cost')
    output=optimise_fun(production_names,distribution_names,cost_data)
    output.reset_index().pivot(index='production', columns='distribution', values='cost')    

if __name__ == "__main__":
    main()







# production = ['Baltimore','Cleveland','Little Rock','Birmingham','Charleston']
# distribution = ['Columbia','Indianapolis','Lexington','Nashville','Richmond','St. Louis']

# # Define a gurobipy model for the decision problem
# m = gp.Model('widgets')

# path = 'https://raw.githubusercontent.com/Gurobi/modeling-examples/master/optimization101/Modeling_Session_1/'
# transp_cost = pd.read_csv(path + 'cost.csv', index_col=[0,1], squeeze=True)
# # transp_cost = pd.read_csv('cost.csv', index_col=[0,1], squeeze=True)
# # Pivot to view the costs a bit easier
# transp_cost.reset_index().pivot(index='production', columns='distribution', values='cost')


# max_prod = pd.Series([180,200,140,80,180], index = production, name = "max_production")
# n_demand = pd.Series([89,95,121,101,116,181], index = distribution, name = "demand") 
# max_prod.to_frame()
# #n_demand.to_frame()

# frac = 0.75

# # loop through each p and d combination to create a decision variable
# m = gp.Model('widgets')
# x={}
# for p in production:
#   for d in distribution:
#     x[p,d]=m.addVar(name=p+"_to_"+d)

# m.update()
# x


# # Provide each set for the indices 
# m = gp.Model('widgets')
# x=m.addVars(production,distribution,name="prod_ship")
# m.update()
# x

# # The index of the tranporation costs have each combination of prodiction and distribution location
# m = gp.Model('widgets')
# x=m.addVars(transp_cost.index,name="prod_ship")
# m.update()
# x

# meet_demand=m.addConstrs((gp.quicksum(x[p,d] for p in production) >= n_demand[d] for d in distribution),
#                           name="meet_demand")
# m.update()
# x


# can_produce = m.addConstrs((gp.quicksum(x[p,d] for d in distribution)<= max_prod[p] for p in production),
#                            name="can produce")
# must_produce = m.addConstrs((gp.quicksum(x[p,d] for d in distribution)>= frac*max_prod[p] for p in production),
#                            name="must produce")
# m.update()
# can_produce


# m.setObjective(gp.quicksum(transp_cost[p,d]*x[p,d] for p in production for d in distribution),GRB.MINIMIZE)

# m.write('widget_shipment.lp')
# m.optimize()

# x_values = pd.Series(m.getAttr('X', x), name = "shipment", index = transp_cost.index)
# sol = pd.concat([transp_cost, x_values], axis=1)
# #sol 
# sol[sol.shipment > 0]