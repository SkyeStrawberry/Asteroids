from Util.constants import Colour, Point, Vector
import math
import pygame

class Projectile():
	length: int
	speed: float
	velocity: Vector
	center: Point
	oldCenter: Point
	start: Point
	oldStart: Point
	end: Point
	oldEnd: Point
	angle: float
	angleDeg: float
	colour: Colour
	rect: pygame.rect.Rect

	def __init__(self, pygame, display: pygame.Surface, x: int | float, y: int | float, angle: int | float, parent):
		self.length  = 10
		self.speed: float   = 40 + (parent.speed or 0)
		self.center = Point(x, y)
		self.start = Point(x - ( math.sin(angle) * self.length )/2 , y + ( math.cos(angle) * self.length )/2 )
		self.end = Point(x + ( math.sin(angle) * self.length )/2 , y - ( math.cos(angle) * self.length )/2 )
		self.oldCenter = self.center
		self.oldStart = self.start
		self.oldEnd  = self.end
		self.angle = angle
		self.angleDeg = math.degrees(angle)
		self.parent = parent
		self.colour = parent.colour
		self.draw(pygame, display)
		self.setVelocity()

	def draw(self, pygame, display: pygame.Surface):
		self.rect = pygame.draw.line(display, self.colour, (self.start[0], self.start[1]), (self.end[0], self.end[1]), 2)
		pygame.display.update()
		return self
		
	def update(self, pygame, display: pygame.Surface):
		pygame.draw.line(display, "black", (self.oldStart[0], self.oldStart[1]), (self.oldEnd[0], self.oldEnd[1]), 3)
		self.draw(pygame, display)
		return self

	def move(self, pygame, display: pygame.Surface, deltax=0, deltay=0):
		if deltax == 0 and deltay == 0:
			deltax = self.velocity[0]
			deltay = self.velocity[1]
		self.oldCenter = self.center
		self.oldStart  = self.start
		self.oldEnd    =  self.end
		self.center = Point(self.center[0] + deltax, self.center[1] - deltay)
		self.start  = Point(self.start[0]  + deltax, self.start[1]  - deltay) 
		self.end    = Point(self.end[0]    + deltax, self.end[1]    - deltay) 
		self.update(pygame, display)
		return self

	def setVelocity(self):
		deltax = (self.speed * math.sin(self.angle))/2
		deltay = (self.speed * math.cos(self.angle))/2
		self.velocity = Vector(deltax , deltay)
		return self

	def destroy(self, pygame, display: pygame.Surface):
		pygame.draw.line(display, "black", self.start, self.end, 3)
		pygame.display.update()
		return self
		
	def outofBounds(self, pygame) -> bool:
		screen = pygame.display.get_window_size()
		if (screen[0]+self.length < self.end[0] or self.end[0] < -self.length) or (screen[1]+self.length < self.end[1] or self.end[1] < -self.length):
			if (screen[0]+self.length < self.start[0] or self.start[0] < -self.length) or (screen[1]+self.length < self.start[1] or self.start[1] < -self.length):
				if (screen[0]+self.length < self.center[0] or self.center[0] < -self.length) or (screen[1]+self.length < self.center[1] or self.center[1] < -self.length):
					return True
		return False
			