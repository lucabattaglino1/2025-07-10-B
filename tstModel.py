# tstModel.py
from model.model import Model

mdl = Model()
mdl.buildGraph('2016-01-01', '2018-12-28', 'Electric Bikes')
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")
