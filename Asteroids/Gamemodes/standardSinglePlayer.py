from Structures.asteroid import Asteroid
from Structures.character import Character
from Structures.projectile import Projectile
from Util.constants import *
from math import radians
import time

class StandardSinglePlayer():
	def __init__(self, pygame, display, gameOptions, player: Character):
		self.gameOptions = gameOptions
		self.displayDimensions = pygame.display.get_window_size()
		self.player: Character = player
		self.clock = gameOptions["clock"]
		self.projectiles: list[Projectile] = []
		self.asteroids: list[Asteroid]   = []
		self.gameMode = "Single Player (Standard)"
		self.asteroidDelay = 2
		self.asteroidStart = time.time()
		self.closed = False
		
		return None
	def run(self, pygame, display):
		
		while not self.closed:
			for event in pygame.event.get(game_over.type):
				self.closed = True
				break
			for event in pygame.event.get(pygame.KEYDOWN):
				if event.key == pygame.K_ESCAPE:
					pygame.event.post(game_pause)
				if event.key == pygame.K_SPACE:
					projectile = self.player.shoot(pygame, display)
					if projectile:
						self.projectiles.append(projectile)
				if event.key == pygame.K_UP:
					self.player.acceleration += 0.2
				if event.key == pygame.K_LEFT:
					self.player.angularAcc -= 3
				if event.key == pygame.K_RIGHT:
					self.player.angularAcc += 3

			for event in pygame.event.get(pygame.KEYUP):
				if event.key == pygame.K_UP:
					self.player.acceleration -= 0.2
				if event.key == pygame.K_LEFT:
					self.player.angularAcc += 3
				if event.key == pygame.K_RIGHT:
					self.player.angularAcc -= 3
			
			for asteroid in self.asteroids:
				asteroid.move(pygame, display)
				if asteroid.outofBounds():
					self.asteroids.remove(asteroid)
					continue
				if asteroid.rect.contains(self.player.rect):
					asteroid.destroy(pygame, display)
					self.asteroids.remove(asteroid)
					break
			
			for projectile in self.projectiles:
				collision = projectile.rect.collidelist(self.asteroids)  # type: ignore
				if 0 <= collision:
					self.player.score += int(10000/((self.asteroids[collision].radius/3)**2))
					self.asteroids[collision].destroy(pygame, display)
					self.asteroids.remove(self.asteroids[collision])
					projectile.destroy(pygame, display)
					self.projectiles.remove(projectile)
					continue
				if projectile.outofBounds(pygame):
					self.projectiles.remove(projectile)
					continue
				projectile.move(pygame, display)
		
			if self.asteroidDelay <= (time.time()-self.asteroidStart):
				self.asteroidStart = time.time()
				self.asteroids.append(Asteroid(pygame, display, {
					"radius": 90,
					"speed": 20,
					"velocity": (0, 0),
					"sizeLvl": 1,
					"center": (0, 0),
					"angle": 0,
					"spawn": True,
				}, self))	 
			self.player.movef(pygame, display).rotate(pygame, display).friction().displayScore(pygame, display, 0, 0, Colour(255, 255, 255))
			self.clock.tick(60)
		return self
	
	def spawnAsteroid(self, pygame, display: pygame.Surface, asteroids: dict):
		for asteroid in asteroids:
			self.asteroids.append(Asteroid(pygame, display, {
				"radius": asteroid["radius"],
				"speed": 20,
				"velocity": asteroid["velocity"],
				"sizeLvl": 1,
				"center": asteroid["center"],
				"angle": radians(asteroid["angle"]),
				"spawn": False,
			}, self))
			
		return self
