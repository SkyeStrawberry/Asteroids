import pygame
from typing import NamedTuple

Point  = NamedTuple('Point', [('x', int | float), ('y', int | float)])
Vector = NamedTuple("Vector", [("dx", int | float), ("dy", int | float)])
Colour = NamedTuple("Colour", [("red", int), ("green", int), ("blue", int)])

menu_show   = pygame.event.Event(pygame.event.custom_type())
menu_hide   = pygame.event.Event(pygame.event.custom_type())
game_start  = pygame.event.Event(pygame.event.custom_type())
game_pause  = pygame.event.Event(pygame.event.custom_type())
game_resume = pygame.event.Event(pygame.event.custom_type())
game_over   = pygame.event.Event(pygame.event.custom_type())
game_won    = pygame.event.Event(pygame.event.custom_type())