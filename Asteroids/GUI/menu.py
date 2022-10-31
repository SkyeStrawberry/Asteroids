from GUI.button import Button
from Util.constants import Point, Colour
from Structures.gameHandler import GameHandler
import pygame

class MainMenu():
	def __init__(self, pygame, display):
		self.font = pygame.font.Font("Util/font.ttf", 30)
		self.clock = pygame.time.Clock()
		self.center = (0,0)
		self.closed = False
		self.buttons = []
		self.initialise(pygame, display)
		self.menuLoop(pygame, display)

	def hideAll(self, display):
		display.fill(Colour(0,0,0))

	def runStand(self, pygame, display):
		self.hideAll(display)
		clock = pygame.time.Clock()
		gameOptions = {
			"clock": clock,
			"gameMode": "standard",
			"players": [
			{
				"spawn": (display.get_width()/2, display.get_height()/2),
				"colour": "white",
				"name": "p1"
				},
			]
		}
		GameHandler(pygame, display, gameOptions)

	def initialise(self, pygame, display):
		self.addButton(pygame, display, 550, 500, "Single Player")
		return self

	def generateText(self, pygame, display, text, x, y, colour):
		textSurface = self.font.render(text, True, colour)
		textSize = textSurface.get_size()
		bounds = textSurface.get_bounding_rect(0)
		bounds.center = (x, y)
		
		pygame.draw.rect(display, colour, bounds, 1)
		x = x - textSize[0]/2
		y = y - textSize[1]/2
		display.blit(textSurface, (x, y))
		pygame.draw.line(display, colour, (x,y), (x+1, y+1))
		pygame.display.update()

	def addButton(self, pygame, display: pygame.Surface, x: int | float, y: int | float, text: str):
		newButton = Button(pygame,  display, self, Point(x, y), text, 20, {
			"text": Colour(255, 255, 255),
			"hover": Colour(110, 110, 110),
		})
		self.buttons.append(newButton)
		return self

	def menuLoop(self, pygame, display):
		pygame.display.set_caption("Asteroids")
		while not self.closed:
			display.fill(Colour(0,0,0))
			pygame.event.get()
			
			mousePos = pygame.mouse.get_pos()
			for button in self.buttons:
				button.isHovered(Point(mousePos[0], mousePos[1]))
				button.renderText(pygame, display)
				if pygame.mouse.get_pressed()[0] and button.isHover:
					button.click(pygame, display)
			self.clock.tick(144)