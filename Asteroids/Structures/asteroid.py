from Gamemodes.typings.standardSinglePlayer import StandardSinglePlayer
from Util.constants import Point, Vector, Colour
from math import sin, cos, acos, radians, degrees, sqrt
from random import randint, choice
import pygame

class Asteroid():
	radius: int
	diameter: int
	speed: float
	velocity: Vector
	sizeLvl: int
	center: Point
	oldCenter: Point
	vertices: list[Point]
	oldVertices: list[Point]
	angle: float
	angleDeg: float
	rotation: float
	rect: pygame.rect.Rect
	parent: StandardSinglePlayer

	def __init__(self, pygame, display, data, parent):	
		self.t = (0,0)
		self.radius   = int(round(data["radius"]))
		self.diameter = self.radius*2

		self.speed = data["speed"]
		self.velocity = data["velocity"]
		self.sizeLvl = data["sizeLvl"]

		self.center = data["center"]
		self.oldCenter = self.center
		self.vertices = []
		self.oldVertices = []
		
		self.angle    = data["angle"]
		self.angleDeg = degrees(data["angle"])
		self.rotation = radians(choice([0.1, -0.1]))
		self.parent = parent
		
		if data["spawn"]:
			self.chooseSpawn()
			
		self.createVertices()
		self.setVelocity()
		self.draw(pygame, display)

	def chooseSpawn(self):
		x = randint(-self.diameter, self.parent.displayDimensions[0]+ self.diameter)
		y = randint(-self.diameter, self.parent.displayDimensions[1]+ self.diameter)
		side = randint(-2, 2)
		if side == -2:
			x = randint(-self.diameter, self.parent.displayDimensions[0] + self.diameter)
			y = -self.diameter
		elif side == -1:
			x = -self.diameter
			y = randint(-self.diameter, self.parent.displayDimensions[1] + self.diameter)
		elif side == 1:
			x = self.parent.displayDimensions[0] + self.diameter
			y = randint(-self.diameter, self.parent.displayDimensions[1] + self.diameter)
		else:
			x = randint(-self.diameter, self.parent.displayDimensions[0] + self.diameter)
			y = self.parent.displayDimensions[1] + self.diameter
		
		self.center = Point(x, y)
		self.t = (x,y)
		return self

	def createVertices(self):
		for i in range(0,8):
			vertex = (self.center[0], self.center[1]+randint((round(self.radius/choice([2,2,2,4,4]))), self.radius))
			x = ( (vertex[0]-self.center[0]) * cos(radians(45*i)) - (vertex[1]-self.center[1]) * sin(radians(45*i)) ) + self.center[0]
			y = ( (vertex[0]-self.center[0]) * sin(radians(45*i)) - (vertex[1]-self.center[1]) * cos(radians(45*i)) ) + self.center[1]
			self.vertices.append(Point(x, y))
			self.oldVertices.append(Point(x, y))
		return self

	def setVelocity(self):
		if self.velocity == (0,0):		
			x = randint(self.radius, self.parent.displayDimensions[0]-self.radius)
			y = randint(self.radius, self.parent.displayDimensions[1]-self.radius)
			dy = (y-self.center[1])
			dx = (x-self.center[0])
			d = sqrt(dx**2 + dy**2)
			theta = degrees(acos(dy/d))
			if dx < 0: theta = 360-theta
			self.angleDeg = theta
			self.angle = radians(theta)
		deltax = ((self.speed * sin(self.angle))/2)/(self.radius/9)
		deltay = ((self.speed * cos(self.angle))/2)/(self.radius/9)
		self.velocity = Vector(deltax, deltay)
		return self
		
	def draw(self, pygame, display, colour="white"):
		self.rect = pygame.draw.polygon(display, colour, self.vertices, 2)
		pygame.display.update()
		return self

	def update(self, pygame, display, colour="white"):
		pygame.draw.polygon(display, Colour(0,0,0), self.oldVertices, 3)
		pygame.display.update()
		self.draw(pygame, display, colour)
		return self

	def move(self, pygame, display):
		self.oldVertices = self.vertices.copy()
		self.oldCenter = self.center
		for index, vertex in enumerate(self.vertices):
			self.vertices[index] = Point(vertex.x + self.velocity.dx, vertex.y + self.velocity.dy)
		self.center = Point(self.center.x + self.velocity.dx, self.center.y + self.velocity.dy)
		self.rotate(pygame, display)
		return self
	
	def rotate(self, pygame, display):
		for index, vertex in enumerate(self.vertices):
			x = (vertex.x-self.center.x)*cos(self.rotation) - (vertex.y-self.center.y)*sin(self.rotation)+self.center.x
			y = (vertex.x-self.center.x)*sin(self.rotation)+(vertex.y-self.center.y)*cos(self.rotation)+self.center.y
			self.vertices[index] = Point(x, y)
		self.update(pygame, display)
		return self

	def destroy(self, pygame, display):
		angledif = randint(70, 90)
		self.parent.spawnAsteroid(pygame, display, [
			{
				"radius": self.radius/2,
				"angle": self.angleDeg-angledif,
				"center": self.center,
				"velocity": self.velocity,
			}, 
			{
				"radius": self.radius/2,
				"angle": self.angleDeg+angledif,
				"center": self.center,
				"velocity": self.velocity
			}
		])
		pygame.draw.polygon(display, Colour(0,0,0), self.vertices, 3)
		return None

	def outofBounds(self):
		rtrn = False
		for vertex in self.vertices:
			if (self.parent.displayDimensions[0]+2*self.diameter < vertex.x or vertex.x < -2*self.diameter) or (self.parent.displayDimensions[1]+2*self.diameter < vertex.y or vertex.y < -2*self.diameter):
				rtrn = True
			else: 
				return False
		return rtrn