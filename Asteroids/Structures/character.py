from Util.constants import Point, Vector, Colour
from .projectile import Projectile
from math import sin, cos, radians, sqrt
import pygame

import time
#9.899999999999878 thrust 10, fc 0.01

class Character():
	center: Point
	velocity: Vector
	sideLen: int
	speed: float
	acceleration: float
	angularAcc: float
	angle: float
	angleDeg: float
	shotTimer: float
	lastShot: float
	shots: int
	hits: int
	score: int
	oldScore: int
	colour: Colour
	rect: pygame.rect.Rect
	vertices: list[Point]
	oldVertices: list[Point]
	oldCenter: Point

	def __init__(self, pygame, display: pygame.Surface , x: int, y: int, colour: Colour = Colour(255, 255, 255) , thrustF: int = 10, draw: bool = False):
		self.center = Point(x, y)
		self.velocity = Vector(0, 0)
		self.sideLen = 25
		self.speed = 0
		self.acceleration = 0
		self.angularAcc = 0
		self.angle = 0
		self.angleDeg = 0
		self.shotTimer = 0.4
		self.lastShot = 0
		self.shots = 0
		self.hits = 0
		self.score = 0
		self.oldScore = 0
		self.colour = colour
		self.vertices = [
			Point( x, y - ( 2*self.sideLen*sqrt(3) ) /6 ),  
			Point( x - ( self.sideLen/2 ), y + ( self.sideLen * sqrt(3) ) /6 ),
			Point( x + ( self.sideLen/2 ), y + ( self.sideLen * sqrt(3) ) /6 ),
		]
		self.oldVertices : list[Point] = self.vertices
		self.oldCenter   : Point = self.center
		
		if draw:
			self.draw(pygame, display)
	
	def draw(self, pygame, display: pygame.Surface):
		vertices = self.vertices.copy(); vertices.insert(2, self.center) #Creates a shallow copy and inserts the center to oldVertices
		self.rect = pygame.draw.polygon(display, self.colour, vertices, 2) #Draws 
		pygame.display.update()	 

		return self


	def update(self, pygame, display: pygame.Surface):
		oldVertices = self.oldVertices.copy(); oldVertices.insert(2, self.oldCenter)  #Creates a shallow copy and inserts the center to oldVertices
		pygame.draw.polygon(display, Colour(0,0,0), oldVertices, 3) #Draws over old polygon
		self.draw(pygame, display)
		pygame.display.update()
		return self

	def move(self, pygame, display: pygame.Surface, deltax: int | float, deltay: int | float):
		self.oldVertices = self.vertices
		self.oldCenter = self.center
		self.vertices = [ #Changes the coordinates of each vertex by deltax and deltay
			Point(self.vertices[0].x + deltax, self.vertices[0].y - deltay),
			Point(self.vertices[1].x + deltax, self.vertices[1].y - deltay),
			Point(self.vertices[2].x + deltax, self.vertices[2].y - deltay),
		]
		self.center = Point(self.center[0] + deltax, self.center[1] - deltay) #Changes the coordinates of the center by deltax and deltay
		self.update(pygame, display)
		return self
	
	def rotate(self, pygame, display: pygame.Surface):
		#Calculates the new coordinates of each vertex using 
		#x' = ( x - xᵣ)cos(θ) - (y - yᵣ)sin(θ) + xᵣ
		#y' = ( x - xᵣ)sin(θ) + (y - yᵣ)cos(θ) + yᵣ , where:
		#(xᵣ, yᵣ) is the point of rotation, and
		#(x', y') is the new set of cordinates for the vertex, and
		# θ is the change in angle 
		daRadians = radians(self.angularAcc)
		self.angle += daRadians
		self.angleDeg += self.angularAcc
		self.oldVertices = self.vertices
		self.oldCenter = self.center
		vertices = []
		for vertex in self.vertices:		
			vertexX = (vertex.x-self.center.x)*cos(daRadians) - (vertex.y-self.center.y)*sin(daRadians)+self.center.x #x' = ( x - xᵣ)cos(θ) - (y - yᵣ)sin(θ) + xᵣ
			vertexY = (vertex.x-self.center.x)*sin(daRadians) + (vertex.y-self.center.y)*cos(daRadians)+self.center.y #y' = ( x - xᵣ)sin(θ) + (y - yᵣ)cos(θ) + yᵣ
			vertices.append(Point(vertexX, vertexY)) #(x', y')
		self.vertices = vertices
		self.update(pygame, display)
		return self

	def movef(self, pygame, display: pygame.Surface):
		#Changes the vector velocity of the spaceship in the direction it is facing using
		#Δx = (F sin θ)/2
		#Δy = (F cos θ)/2
		#where F is the magnitude of the vector added to the current velocity
		#and θ is the angle of the spaceship
		deltax = (self.acceleration * sin(self.angle))/2 #Δx = (F sin θ)/2
		deltay = (self.acceleration * cos(self.angle))/2 #Δy = (F cos θ)/2
		self.velocity = Vector(self.velocity.dx + deltax ,self.velocity.dy + deltay)
		self.speed = sqrt((self.velocity.dx**2) + (self.velocity.dy**2)) #Speed of the character using pythagoras
		self.move(pygame, display, self.velocity.dx, self.velocity.dy)
		return self
	
	def friction(self, coefrict = 0.01): #Subtracts a percentage of the velocity from itself; thanks mafew
		frictionResx = self.velocity.dx - (self.velocity.dx * coefrict)
		frictionResy = self.velocity.dy - (self.velocity.dy * coefrict)
		self.velocity = Vector(frictionResx, frictionResy)
		return self

	def shoot(self, pygame, display: pygame.Surface):
		if self.shotTimer <= (time.time() - self.lastShot): #Stops the player from shooting faster than the shot timer
			self.lastShot = time.time()
			self.shots += 1
			return Projectile(pygame, display, self.vertices[0].x, self.vertices[0].y, self.angle, self)

	def outofBounds(self, pygame) -> bool:
		dimensions = pygame.display.get_window_size()
		if dimensions[0] + (2*self.sideLen*sqrt(3)) /6 < self.center.x:
			print("out right")
		if self.center.x < -((2*self.sideLen*sqrt(3)) /6):
			print("out left")
		if dimensions[1] + (2*self.sideLen*sqrt(3)) /6 < self.center.y:
			print("out bottom")
		if self.center.y < -((2*self.sideLen*sqrt(3)) /6):
			print("out top")
		return True

	def displayScore(self, pygame, display, x, y, colour):
		textSurface = pygame.font.Font("Util/font.ttf", 20).render(f"Score: {self.score}", True, colour)
		textSize = textSurface.get_size()
		bounds = textSurface.get_bounding_rect(0)
		bounds.center = (x + textSize[0]/2, y + textSize[1]/2)
		pygame.draw.rect(display, Colour(0, 0,0), bounds, 0)
		display.blit(textSurface, (x, y))
		pygame.display.update()