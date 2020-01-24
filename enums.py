from enum import Enum
import mainwindow

pieceType = Enum("Type", "King Queen Bishop Knight Rook Pawn NoType")	
pieceColor = Enum("Color", "White Black NoColor")

class Piece:
	pType = pieceType.NoType
	pColor = pieceColor.White

	def __init__(self):
		self.pType = pieceType.NoType
		self.pColor = pieceColor.White		

	def __init__(self, t, c):
		self.pType = t
		self.pColor = c

	def __str__(self):
		return self.pType.name

	def setType(self, t):
		self.pType = t

	def setColor(self, c):
		self.pColor = c

	def type(self):
		return self.pType

	def color(self):
		return self.pColor