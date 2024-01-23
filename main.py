import streamlit as st
import pandas as pd
import numpy as np
from pulp import *

# Load some example data.
DATA_URL = \
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
data = st.cache(pd.read_csv)(DATA_URL, nrows=1000)

# Select some rows using st.multiselect. This will break down when you have >1000 rows.
st.write('### Full Dataset', data)
selected_indices = st.multiselect('Select rows:', data.index)
selected_rows = data.loc[selected_indices]
st.write('### Selected Rows', selected_rows)

decision_variables = []
for rownum, row in selected_rows.iterrows():
    variable = str('x' + str(rownum))
    variable = LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer')
    decision_variables.append(variable)


print ("Total_number_of_decision_variables: " + str(len(decision_variables)))
print(decision_variables)
st.write(decision_variables)

# define the problem
prob = LpProblem('test',LpMinimize)

total_cost = ""
for rownum, row in selected_rows.iterrows():
    for i, schedule in enumerate(decision_variables):
        if rownum == i:
            formula = row['Lat']*schedule
            total_cost += formula

    prob += total_cost

print ("Optimization function: " + str(total_cost))

st.write("**total cost :**")
st.title(total_cost)