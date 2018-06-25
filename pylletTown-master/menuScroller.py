class menuScroller():
	def __init__(self,inventory):

		self.inventory = inventory
		self.length = len(inventory)
		self.counter = 0
		self.first = inventory[0]
		self.last = inventory[self.length-1]
		self.top = inventory[self.counter]
		self.bottom = inventory[5]
		self.itemsBelow = self.length - 1 - self.counter
		self.boxedItem = self.inventory[self.counter]

	def resetCounter(self):
		self.counter = 0
	def scrollDown(self):
		if self.inventory[self.counter] == self.bottom:
			hld = 2
			#we dond do anything here
		else:
			if self.length - 1 - self.counter > 5: 
				self.counter += 1 
				self.top = self.inventory[self.counter]
				self.boxedItem = self.inventory[self.counter]
				self.bottom = self.inventory[5 + self.counter]
			else:
				self.counter += 1 
				
				self.boxedItem = self.inventory[self.counter]	

	def scrollUp(self):
		if self.counter == 0:
			# we do nothing here
			hld3 = 2
		else:
			if self.top == self.first:
				self.counter -= 1
				self.boxedItem = self.inventory[self.counter]
			else:
				self.counter -= 1
				self.top = self.inventory[self.inventory.index(self.top) - 1]
				self.boxedItem = self.inventory[self.counter]
				self.bottom = self.inventory[self.counter]
								
	def printMenu(self):
		print ('the items in the inventory are: ')
		for items in self.inventory[self.inventory.index(self.top):self.inventory.index(self.bottom)+1]:
			print (str(items))
		print ('The bottom of the inventory is ' + str(self.bottom))
		print ('The top of the inventory is ' + str(self.top))		
		print ("And the counter is at " + str(self.counter))