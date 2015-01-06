from __future__ import division
import math
import numpy as np

from utils import *
from sim import *
from spacex import *

# That's a Falcon 9!

Stage1 = Stage( "Falcon 9 First Stage",
				math.pi*(3.66/2)**2,
				0.3,
				Merlin1D,
				9,
				18000+385000,
				385000 )
Stage1.active = True
Stage2 = Stage( "Falcon 9 Second Stage",
				math.pi*(3.66/2)**2,
				0.3,
				Merlin1DVac,
				1,
				4900+90000,
				90000 )
Payload = Stage("Payload",
				math.pi*(3.66/2)**2,
				0.3,
				None,
				0,
				13500,
				0 )

Falcon9 = Rocket([Stage1, Stage2, Payload], np.array([0,R]), 28.5, (20, 0.5, 2.5))
try:
	Falcon9.loop(1000000)
except KeyboardInterrupt:
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	p = ax.plot(xpoints, ypoints, 'b')
	ax.set_xlabel('x-points')
	ax.set_ylabel('y-points')
	ax.set_title('Simple XY point plot')
	plt.show()
