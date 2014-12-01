from ahkab import new_ac, run
from ahkab.circuit import Circuit
from ahkab.plotting import plot_results # calls matplotlib for you
import numpy as np

cir = Circuit('Simple circuit')
cir.add_vsource('V1', 'n1', cir.gnd, dc_value=5)
cir.add_resistor('R1', 'n1', 'n2', 50)
res = run(cir)
print res
print type(res)
