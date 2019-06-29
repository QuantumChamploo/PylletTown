class cutScene():
	def __init__(self, moves):

		self.moves = moves
		
		
		self.first = moves[0]
		self.last = moves[len(moves)-1]
		self.curr = self.first
		self.currPlace = 0


	def hasNextMove(self):
		if self.curr == self.last and not self.curr.hasMoves():
			return False
		else:
			return True


	def verifyCurrentMove(self):
		if not self.curr.hasMoves():
			if self.curr == self.last: 
				hld = 3				
			else:
				self.curr.resetMoves()
				print (str(self.curr.totalMoves))
				self.currPlace += 1
				self.curr = self.moves[self.currPlace]

	def decrementCurrMove(self):
		self.curr.decrementMoves()