from enum import Enum
from PySide2.QtWidgets import QApplication, QLabel, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsPixmapItem, QGraphicsColorizeEffect
from PySide2.QtGui import QColor, QBrush, QTransform, QPixmap
import mainwindow

pieceType = Enum("Type", "King Queen Bishop Knight Rook Pawn NoType")	
pieceColor = Enum("Color", "White Black")

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

class ChessBoard(QGraphicsScene):
	cLightPieceColor = QColor("black")
	cDarkPieceColor = QColor("black")
	cLightSquareColor = QColor("white")
	cDarkSquareColor = QColor("gray")
	cDarkSquareColorFocus = QColor(100,100,170)
	cLightSquareColorFocus = QColor(100,100,255)
	cDarkSquareColorFocusDanger = QColor(170,100,100)
	cLightSquareColorFocusDanger = QColor(255,100,100)
	cDarkSquareColorSelected = QColor(100,170,100)
	cLightSquareColorSelected = QColor(100,255,100)
	cDarkPieceColorThreat = QColor(100,0,0)
	cLightPieceColorThreat = QColor(100,0,0)

	nPieceWidth = 45
	nBorderWidth = 0
	focusRow = 0
	focusCol = 0
	
	board = [[Piece(pieceType.NoType, pieceColor.White)] * 8 for i in range(8)]
	focusCell = [[False] * 8 for i in range(8)]
	threatCell = [[False] * 8 for i in range(8)]
	selectCell = [[False] * 8 for i in range(8)]
	threatPiece = [[False] * 8 for i in range(8)]
	
	def __init__(self):
		super(ChessBoard, self).__init__()
		self.removeAllMarking()

	def setItem(self, i, j, p):
		self.board[i][j] = p
		self.refreshImage(i, j)
	
	def removeItem(self, i, j):
		self.board[i][j] = Piece(pieceType.NoType, pieceColor.White)
		self.refreshImage(i,j)

	def clearBoard(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.setItem(i, j, Piece(pieceType.NoType, pieceColor.White))

	def setTileFocus(self, x, y, f=True):
		self.focusCell[x][y] = f
		self.refreshTile(x, y)
		self.refreshImage(x, y)

	def setTileThreat(self, x, y, f=True):
		self.threatCell[x][y] = f
		self.refreshTile(x, y)
		self.refreshImage(x, y)

	def setTileSelect(self, x, y, f):
		self.selectCell[x][y] = f
		self.refreshTile(x, y)
		self.refreshImage(x, y)

	def setPieceThreat(self, x, y, f):
		self.threatPiece[x][y] = f
		self.refreshImage(x, y)

	def removeAllMarking(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.focusCell[i][j] = False
				self.selectCell[i][j] = False
				self.threatPiece[i][j] = False
				self.threatCell[i][j] = False

		self.redrawEntireBoard()

	def removeAllTileDanger(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.threatCell[i][j] = False

		self.redrawEntireBoard()

	def removeAllTileFocus(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.focusCell[i][j] = False
	
		self.redrawEntireBoard()

	def removeAllTileSelection(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.selectCell[i][j] = False

		self.redrawEntireBoard()

	def removeAllPieceThreats(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.threatPiece[i][j] = False
			
		self.redrawEntireBoard()

	def mousePressEvent(self, e):
		scenePos = e.scenePos()
		if (scenePos.x() < 0 or scenePos.y() < 0 or scenePos.x() > 8 * self.nPieceWidth or scenePos.y() > 8 * self.nPieceWidth):
			focusRow = -1
			focusCol = -1
			return

		focusRow = self.rowFromPoint(scenePos.y())
		focusCol = self.colFromPoint(scenePos.x())

		if (focusRow >= 0 and focusRow < 8 and focusCol >= 0 and focusCol < 8):
			self.emit(clicked(int(focusRow), int(focusCol)))

		self.mousePressEvent(e)

	def hasTileFocus(self, x, y):
		return self.focusCell[x][y]

	def hasTileThreat(self, x, y):
		return self.threatCell[x][y]

	def hasTileSelect(self, x, y):
		return self.selectCell[x][y]

	def hasPieceThreat(self, x, y):
		return self.threatPiece[x][y]

	def drawTile(self, i, j):
		rect = QGraphicsRectItem(j * self.nPieceWidth, i * self.nPieceWidth, self.nPieceWidth, self.nPieceWidth)
		if i % 2 == j % 2:
			if self.selectCell[i][j]: # Selected cells only get the selection background color
				rect.setBrush(QBrush(self.cLightSquareColorSelected))
			elif self.focusCell[i][j]:
				if self.threatCell[i][j]:
					rect.setBrush(QBrush(self.cLightSquareColorFocusDanger))
				else:
					rect.setBrush(QBrush(self.cLightSquareColorFocus))
			else: # If the cell has no focus, it also has no danger indication
				rect.setBrush(QBrush(self.cLightSquareColor))
		else:
			if self.selectCell[i][j]: # Selectd cells only get the selection background color
				rect.setBrush(QBrush(self.cDarkSquareColorSelected))
			elif self.focusCell[i][j]:
				if self.threatCell[i][j]:
					rect.setBrush(QBrush(self.cDarkSquareColorFocusDanger))
				else:
					rect.setBrush(QBrush(self.cDarkSquareColorFocus))
			else: # If the cell has no focus, it also has no danger indication
				rect.setBrush(QBrush(self.cDarkSquareColor))

		rect.setCacheMode(QGraphicsItem.NoCache)
		self.addItem(rect)

	def refreshTile(self, i, j):
		currentItem = self.itemAt(j * self.nPieceWidth , i * self.nPieceWidth , QTransform())
		if currentItem != 0 and currentItem.data(0) == 777:
			currentItem = None

		self.drawTile(i,j)

	def refreshImage(self, i, j):
		currentItem = self.itemAt(self.xFromCol(j), self.yFromRow(i), QTransform())
		if currentItem != 0 and currentItem.data(0) == 777:
			currentItem = None

		filename = self.getPieceFilename(self.board[i][j])
		if filename == "":
			return

		y = self.nPieceWidth * i
		x = self.nPieceWidth * j
		item = QGraphicsPixmapItem(QPixmap(filename))

		colorize = QGraphicsColorizeEffect()
		if self.board[i][j].color() == pieceColor.White:
			if self.threatPiece[i][j]:
				colorize.setColor(self.cLightPieceColorThreat)
			else:
				colorize.setColor(self.cLightPieceColor)
		else:
			if self.threatPiece[i][j]:
				colorize.setColor(self.cDarkPieceColorThreat)
			else:
				colorize.setColor(self.cDarkPieceColor)

		item.setGraphicsEffect(colorize)
		item.setCacheMode(QGraphicsItem.NoCache) # needed for proper rendering
		item.setData(0, 777)

		self.addItem(item)
		item.setPos(x,y)

	def refreshBoard(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.refreshImage(i, j)

	def redrawEntireBoard(self):
		# qDeleteAll( items() )
		self.drawBoard()
		self.refreshBoard()

	def drawBoard(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.drawTile(i,j)

	def getPieceFilename(self, p):
		if p.type() == pieceType.NoType:
			return ""

		filename = "resources/"
		if p.color() == pieceColor.White:
			filename += "white"
		elif p.color() == pieceColor.Black:
			filename += "black"
	
		if p.type() == pieceType.King:
			filename += "-king"
		elif p.type() == pieceType.Queen:
			filename += "-queen"
		elif p.type() == pieceType.Bishop:
			filename += "-bishop"
		elif p.type() == pieceType.Knight:
			filename += "-knight"
		elif p.type() == pieceType.Rook:
			filename += "-rook"
		elif p.type() == pieceType.Pawn:
			filename += "-pawn"

		return filename + ".svg"

	def rowFromPoint(self, y):
		return y / self.nPieceWidth

	def colFromPoint(self, x):
		return x / self.nPieceWidth

	def xFromCol(self, c):
		return c * self.nPieceWidth + 0.5 * self.nPieceWidth

	def yFromRow(self, r):
		return r * self.nPieceWidth + 0.5 * self.nPieceWidth
