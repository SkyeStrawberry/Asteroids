from Structures.character import Character
from Gamemodes.standardSinglePlayer import StandardSinglePlayer

class GameHandler():
	def __init__(self, pygame, display, gameOptions):
		self.gameOptions = gameOptions
		self.displayDimensions = pygame.display.get_window_size()
		
		self.player = None
		
		self.clock = pygame.time.Clock()
		
		self.players = []
		self.projectiles = []
		self.asteroids = []

		
		self.game     = None
		self.gameMode = None
		
		self.closed = False
		
		self.initialise(pygame, display)

	def initialise(self, pygame, display):
		
		for player in self.gameOptions["players"]: 
			spawn = player["spawn"]
			self.players.append(Character(pygame, display, spawn[0], spawn[1], colour=player["colour"], draw=True))

		if self.gameOptions["gameMode"] == "standard":
			if len(self.players) == 1:
				self.game = StandardSinglePlayer
				self.gameMode = "Asteroids (Single Player)"

				self.player = self.players[0]

				pygame.display.set_caption(self.gameMode)
				self.game = StandardSinglePlayer(pygame, display, self.gameOptions, self.player)
			elif 1 < len(self.players) <= 3:
				self.game 
				self.gameMode = f"Asteroids ({len(self.players)} Players)"

		self.game.run(pygame, display) #type:ignore
		return self