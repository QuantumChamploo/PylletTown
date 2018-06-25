import pygame 


class spriteMove():
	def __init__(self, paces, direction):
		self.totalMoves = paces*16 + 1
		self.movesLeft = paces*16 + 1
		self.direction = direction

	def resetMoves(self):
		self.movesLeft = self.totalMoves

	def hasMoves(self):
		if self.movesLeft == 0:
			return False
		else:
			return True
	def decrementMoves(self):
		self.movesLeft -= 1