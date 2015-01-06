from __future__ import division
import math
import numpy as np

from utils import *

class Engine:
	def __init__(self, specific_impulse, fuel_flow):
		self.specific_impulse = specific_impulse
		self.fuel_flow = fuel_flow

	def thrust(self, h):
		return self.specific_impulse(h)*self.fuel_flow

class Stage:
	def __init__(self, name, cross_section, drag_coefficient, engine, num_engines, mass, fuel):
		self.name = name
		self.cross_section = cross_section
		self.drag_coefficient = drag_coefficient
		self.engine = engine
		self.num_engines = num_engines
		self.mass = mass
		self.fuel = fuel
		self.active = False
		self.attached = True

pitch_time = 20
pitch_len = 0.5
pitch_ang = 3.5
#20,0.5,2.5
pitch_time = 20
pitch_len = 0.5
pitch_ang = 2.5

xpoints = []
ypoints = []

class Rocket:
	def __init__(self, stages, position, latitude, pitch_kick):
		self.stages = stages
		self.x = position
		self.v = np.array([surface_vel(latitude),0])
		self.lat = latitude
		self.t = 0
		self.dt = 0.01
		self.vsuf = np.array([surface_vel(latitude),0])
		self.pitch = math.pi/2
		self.pitch_kick = pitch_kick

	def loop(self, n):
	  for _ in range(n):
		x1 = self.x
		h = lambda x: float(np.linalg.norm(x)-R)
		if _ % 100 == 0:
			xpoints.append(x1[0])#-_*self.vsuf[0]*self.dt)
			ypoints.append(x1[1])#-R)
		v1 = self.v
		vel = v1-self.vsuf
		if self.pitch_kick[0] < _*self.dt < self.pitch_kick[0]+self.pitch_kick[1]:
			print "[Pitch kick event]"
			self.pitch = math.pi/2-self.pitch_kick[2]*math.pi/180.
		elif _*self.dt > self.pitch_kick[0]+self.pitch_kick[1]:
			if h(x1) < 90000:
				self.pitch = math.atan2(vel[1], vel[0])
			else:
				self.pitch = math.atan2(v1[1], v1[0])
		elif _*self.dt < self.pitch_kick[0]:
			v1[0] = surface_vel(self.lat)
			self.pitch = math.pi/2

		mass = sum([stage.mass for stage in self.stages if stage.attached])
		vhat = v1/np.linalg.norm(v1)
		xhat = x1/np.linalg.norm(x1)

		def thrust(x):
			thrust = np.array([0,0])
			for stage in self.stages:
				if stage.active and stage.fuel > 0:
					df = stage.num_engines*stage.engine.fuel_flow*self.dt
					stage.fuel -= df
					stage.mass -= df

					thrust += stage.num_engines*stage.engine.thrust(h(x))*np.array([math.cos(self.pitch), math.sin(self.pitch)])
			return thrust
		v = v1
		E = np.dot(v,v)/2-G*M/np.linalg.norm(x1)
		a = -G*M/2/E
		e = np.linalg.norm(np.dot(v,v)*x1/G/M-np.dot(x1, v)*v/G/M-xhat)
		pe = a*(1-e)-R
		ap = a*(1+e)-R
		if pe > 200000:
			for stage in self.stages: stage.active = False
		if _ % 100 == 0:
			print "T: %03d Alt: %03d Vel: %03d Ang: %.1f Ap: %03d Pe: %03d Mass: %f" % (_*self.dt, 1/1000.*h(x1), np.linalg.norm(v1-self.vsuf), 180./math.pi*math.atan2(vel[1], vel[0]),ap/1000,pe/1000, mass)#, self.stages[0].fuel#, thrust(x1), map(lambda x: x.mass, self.stages)
			#for i, stage in enumerate(self.stages):
			#	print "Stage",i,"fuel",stage.fuel,"mass", stage.mass

		for i, stage in enumerate(self.stages):
			if stage.active and stage.fuel < 0:
				print "Stage cutoff!"
				stage.active = False
				stage.attached = False
				try: self.stages[i+1].active = True
				except: pass

		weight = lambda x: -xhat*float((mass*grav(x)))
		drag = lambda x, v: 0 if h(x) > 200000 else -(0.5*density(h(x))*((v-self.vsuf)**2)*self.stages[0].drag_coefficient*self.stages[0].cross_section)
		
		thru = thrust(x1)
		a = lambda x, v: (thru+weight(x)+drag(x,v))/mass
		a1 = a(x1, v1)

		x2 = self.x + 0.5*v1*self.dt
		v2 = self.v + 0.5*a1*self.dt
		a2 = a(x2, v2)

		x3 = self.x + 0.5*v2*self.dt
		v3 = self.v + 0.5*a2*self.dt
		a3 = a(x3, v3)

		x4 = self.x + v3*self.dt
		v4 = self.v + a3*self.dt
		a4 = a(x4, v4)

		self.x = self.x + (self.dt/6.0)*(v1 + 2*v2 + 2*v3 + v4)
		self.v = self.v + (self.dt/6.0)*(a1 + 2*a2 + 2*a3 + a4)