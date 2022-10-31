from Util.constants import Point, Colour
#from GUI.menu import MainMenu
import pygame

class Button():
	center: Point
	text: str
	textColour: Colour
	textSurface: pygame.surface.Surface
	hoverColour: Colour
	hoverRect: pygame.rect.Rect
	isHover: bool
	show: bool
	#parent: MainMenu
	font: pygame.font.Font
	fontSize: int
	
	def __init__(self, pygame, display, parent, center: Point, text: str, size:int, colours: dict) -> None:
		self.center = center
		self.text = text
		self.textColour = colours['text']
		self.hoverColour = colours['hover']
		self.parent = parent
		self.fontSize = size
		self.show = False
		self.isHover = False
		self.font = pygame.font.Font("Util/font.ttf", self.fontSize)

		self.renderText(pygame, display)
	
	def click(self, pygame, display):
		self.parent.runStand(pygame, display)

	def renderText(self, pygame, display):
		self.textSurface = self.font.render(self.text, True, self.textColour)
		self.hoverRect = self.textSurface.get_bounding_rect(0).inflate(10, 15)
		self.hoverRect.center = (int(self.center.x), int(self.center.y))
		
		textSize = self.textSurface.get_size()
		display.blit(self.textSurface, (self.center.x-textSize[0]/2, self.center.y-textSize[1]/2))
		if self.isHover:
			pygame.draw.rect(display, self.hoverColour, self.hoverRect, 1)
		pygame.display.update()
		
		return self
	
	def isHovered(self, mouse: Point):
		if not self.hoverRect.collidepoint(mouse.x, mouse.y): 
			self.isHover = False
			return self
		self.isHover = True	
		return self
		