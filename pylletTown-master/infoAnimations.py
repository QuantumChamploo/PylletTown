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
				print ('something')
				
			else:
				self.curr.resetMoves()
				print (str(self.curr.totalMoves))
				self.currPlace += 1
				self.curr = self.moves[self.currPlace]

	def decrementCurrMove(self):
		self.curr.decrementMoves()
		


class scrollText():
	def __init__(self, inputText):
		self.stringList = inputText.split(' ')

		self.counter = 0
		self.length = len(self.stringList)
		self.top = ''
		self.bottom = ''
		self.level = 'top'
		self.wait = 0
		self.nextScreen = False
		self.pause = False
		


	def resetPlace(self):
		self.counter = 0
		self.top = ''
		self.bottom = ''

	def hasnextLetter(self):
		if self.counter  == self.length:
			return False
		else:
			return True

	def nextLetter(self):
		return self.stringList[self.counter]

	def increment(self):
		self.counter += 1

	def updateScroll(self):
		if self.hasnextLetter():
			if self.wait == 0:

				if self.counter == 0:
					self.level = 'top'

				elif self.counter % 6 == 0:
					if self.level == 'top':
						self.level = 'bottom'
					elif self.level == 'bottom':
						self.pause = True
						if self.nextScreen == True:
							print (self.nextScreen)

							self.level = 'top'
							self.top = ''
							self.bottom = ''
							self.nextScreen = False
							self.pause = False
					
				if self.pause == False:
					if self.level == 'top':
						self.top += self.nextLetter() + " "
					if self.level == 'bottom':
						self.bottom += self.nextLetter() + " "

					self.increment()
					self.wait += 1
				
			else:
				self.wait += 1
				if self.wait >= 1:
					self.wait = 0
