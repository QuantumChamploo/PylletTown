class menuScroller():

										# implemented as list that shows six items at a time
	def __init__(self,inventory, actions, name):
		self.name = name
		self.inventory = inventory
		self.actions = actions
		self.length = len(inventory)
		self.counter = 0
		self.first = inventory[0]
		self.last = inventory[self.length-1]
		self.top = inventory[self.counter]
		self.bottom = inventory[5]
		self.itemsBelow = self.length - 1 - self.counter
		self.boxedItem = self.inventory[self.counter]
		#self.partialInventory = self.inventory[self.inventory.index(self.top):self.inventory.index(self.bottom)]

	def resetCounter(self):
		self.counter = 0

	def nextItem(self, item):
		hldItem = self.inventory[self.inventory.index(item)+1]
		return hldItem

	def lastItem(self, item):
		hldItem = self.inventory[self.inventory.index(item)-1]
		return hldItem

	def findIndex(self, element):
		hldIndex = [self.inventory[0] for item in self.inventory].index(element)
		return hldIndex


	# old implementation
	# def scrollDown(self):
	# 	if self.inventory[self.counter] == self.bottom:
	# 		hld = 2
	# 		#we dond do anything here
	# 	else:
	# 		if self.length - 1 - self.counter > 5: 
	# 			self.counter += 1 
	# 			self.top = self.inventory[self.counter]
	# 			self.boxedItem = self.inventory[self.counter]
	# 			self.bottom = self.inventory[5 + self.counter]
	# 		else:
	# 			self.counter += 1 
				
	# 			self.boxedItem = self.inventory[self.counter]	


	# # old implementation
	# def scrollUp(self):
	# 	if self.counter == 0:

	# 		# we do nothing here
	# 		hld3 = 2
	# 	else:
	# 		if self.top == self.first:
	# 			self.counter -= 1
	# 			self.boxedItem = self.inventory[self.counter]
	# 		else:
	# 			self.counter -= 1
	# 			self.top = self.inventory[self.FindIndex(self.top) - 1]
	# 			self.boxedItem = self.inventory[self.counter]
	# 			self.bottom = self.inventory[self.counter]


	def scrollUP(self):
		if self.counter == 0 and self.top == self.first:
			hldint = 0

		elif self.counter == 0:
			self.top = self.lastItem(self.top)
			self.bottom = self.lastItem(self.bottom)
		else:
			self.counter -= 1

	def scrollDOWN(self):
		if self.counter == 5 and self.bottom == self.last:
			hldint = 1

		elif self.counter == 5:
			self.top = self.nextItem(self.top)
			self.bottom = self.nextItem(self.bottom)
		else:
			self.counter += 1



								
	def printMenu(self):
		print ('the items in the inventory are: ')
		for items in self.inventory[0][self.findIndex(self.top):self.findIndex(self.bottom)+1]:
			print (str(items))
		print ('The bottom of the inventory is ' + str(self.bottom))
		print ('The top of the inventory is ' + str(self.top))		
		print ("And the counter is at " + str(self.counter))