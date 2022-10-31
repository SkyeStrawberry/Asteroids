from Structures.gameHandler import GameHandler
from GUI.menu import MainMenu
from GUI.button import Button
from Util.constants import Point, Colour
import pygame

pygame.init()

dispWidth  = 1100
dispHeight = 800

display = pygame.display.set_mode((dispWidth, dispHeight))
display.get_height()
display.get_width()
clock = pygame.time.Clock()

gameOptions = {
	"clock": clock,
	"gameMode": "standard",
	"players": [
		{
			"spawn": (dispWidth/2, dispHeight/2),
			"colour": "white",
			"name": "p1"
		},
	]
}

menu = MainMenu(pygame, display)
#button = Button(pygame, display, menu, Point(dispWidth/2, dispHeight/2), "Lorem ipsum", 80, {
#	"text": Colour(255, 255, 255),
#	"hover": Colour(110, 110, 110),
#})
#menu.buttons.append(button)
#menu.menuLoop(pygame, display)
#menu.generateText(pygame, display, "test", disp W idth/2, dispHeight/2, "white")
#game = GameHandler(pygame, display, gameOptions)