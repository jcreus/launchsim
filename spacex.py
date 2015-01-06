# Common code for SpaceX rocket engines

from utils import *
from sim import *

# Falcon 9 simulation

p0 = pressure(0)

def get_isp(h):
	if h < 80000:
		return 282*g + (1/p0)*(p0-pressure(h))*(320*g-282*g)
	else:
		return 320*g

Merlin1D = Engine(get_isp, 236)
Merlin1DVac = Engine(lambda _: 340*g, 236)