

class Position:
	def __init__(self,x,y):
		self.isEpmty = True
		self.position = [float(x),float(y)]

#centerOfHorizontal = 210 / 2
#centerOfVertical = 297 / 2
#widthOfCardsRow = cardwidth * cardCountOnHorizontal + spaceBetweenOnHorizontal * (cardCountOnHorizontal - 1)
#heightOfCardsCol = cardwidth * cardCountOnHorizontal + spaceBetweenOnHorizontal * (cardCountOnHorizontal - 1)

class SinglePage:
	#default Single pdff page	
	def __init__(self,cardWidth = 57,cardHeight = 89,cardCountOnHorizontal = 3,cardCountOnVertical = 3,spaceBetweenOnHorizontal = 5,spaceBetweenOnVertical = 5,shiftBack = 0):
		self.countOfFreePositions = 0
		centerOfHorizontal = 210 / 2
		centerOfVertical = 297 / 2
		widthOfCardsRow = cardWidth * cardCountOnHorizontal + (spaceBetweenOnHorizontal * (cardCountOnHorizontal - 1))
		heightOfCardsCol = cardHeight * cardCountOnVertical + (spaceBetweenOnVertical * (cardCountOnVertical - 1))
		#default count of cards with grid 3x3
		
		leftBorder = centerOfHorizontal - widthOfCardsRow/2
		upBorder = centerOfVertical - heightOfCardsCol/2 - shiftBack

		if cardCountOnVertical == -3 and cardCountOnHorizontal == -33:
			self.positions = [
								Position(0,0),Position(float(cardWidth),0),Position(float(cardWidth)*2,0),
								Position(0,float(cardHeight)),Position(float(cardWidth),float(cardHeight)),Position(float(cardWidth)*2,float(cardHeight)),
								Position(0,float(cardHeight)*2),Position(float(cardWidth),float(cardHeight)*2),Position(float(cardWidth)*2,float(cardHeight)*2)
							 ]
		else:
			#must restore only x
			self.positions = []
			nextColCardIndex = int(0)
			for y in range(int(cardCountOnVertical)):
				for x in range(int(cardCountOnHorizontal)):

					if y == 0 and x == 0:
						self.positions.append(Position(leftBorder,upBorder))
					else:
						self.positions.append(Position(leftBorder + x* (cardWidth + int(spaceBetweenOnHorizontal)),upBorder + y *(cardHeight+ int(spaceBetweenOnVertical))))
					nextColCardIndex+=1
				nextColCardIndex = 0
	def isPageFull(self):
		for pos in self.positions:
			if pos.isEpmty == True:
				self.countOfFreePositions += 1
		if self.countOfFreePositions	== 0:
			return True
		else:
			self.countOfFreePositions = 0
			return False

	def getLastFreePos(self):
		for pos in self.positions:
			if pos.isEpmty == True:
				pos.isEpmty = False
				return pos.position
