from pint import UnitRegistry
import math
import numpy as np

#u = UnitRegistry()

g = 9.80665#*u.m/(u.s**2)
R = 6371009#*u.m
M = 5.97219e24#*u.kg
G = 6.67384e-11#*u.N/(u.kg**2)*u.m**2
grav = lambda x: G*M/np.linalg.norm(x)**2

def pressure_temperature(h):
	h = h
	if h >= 25000:
		T = -131.21+0.00299*h
		P = 2.488*((T+273.1)/216.6)**-11.388
	elif 11000 <= h < 25000:
		T = -56.46
		P = 22.65*math.e**(1.73-0.000157*h)
	elif h <= 11000:
		T = 15.04 - 0.00649*h
		P = 101.29*((T+273.1)/288.08)**5.256
	else:
		P = T = 0
	return (P, T)

def pressure(h):
	return pressure_temperature(h)[0]

def density(h):
	P, T = pressure_temperature(h)
	return P/(0.2869*(T+273.1)) 

def surface_vel(lat):
	return R*math.cos(lat*math.pi/180)*7.2921150e-5

