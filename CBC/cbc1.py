import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(bounds=(0,10))
model.y = pyo.Var(bounds=(0,10))
x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= -x+2*y<=8)
model.C2 = pyo.Constraint(expr= 2*x+y<=14)
model.C3 = pyo.Constraint(expr= 2*x-y<=10)

model.obj = pyo.Objective(expr= x+y, sense=pyo.maximize)

# Use CBC solver instead of GLPK
opt = SolverFactory('cplex')
opt.solve(model)

model.pprint()

x_value = pyo.value(x)
y_value = pyo.value(y)

print('\n---------------------------------------------------------------------')
print('x=', x_value)
print('y=', y_value)





# from pyomo.environ import *

# import pyutilib.subprocess.GlobalData
# pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

# model = ConcreteModel()

# model.x = Var([1,2], domain=NonNegativeReals)

# model.OBJ = Objective(expr = 2*model.x[1] + 3*model.x[2])

# model.Constraint1 = Constraint(expr = 3*model.x[1] + 4*model.x[2] >= 1)

# opt = SolverFactory('cbc')
# opt.solve(model)