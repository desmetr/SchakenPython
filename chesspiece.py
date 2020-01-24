from enums import *
from tkinter import *
import itertools

class ChessPiece():
	pColor = None
	def __init__(self, c):
		self.pColor = c
		self.image = None
		self.selected = False

	def setImage(self):
		pass

	def piece(self):
		return Piece(pieceType.NoType, self.color())

	def color(self):
		return self.pColor

	def possibleMoves(self, r, c, firstMoveBlack, firstMoveWhite):
		pass

class NoType(ChessPiece):
	def __init__(self, c):
		super(NoType, self).__init__(c)

	def piece(self):
		return Piece(pieceType.NoType, self.color())
	
	def __str__(self):
		return "NoType"

	def setImage(self):
		pass

	def possibleMoves(self, r, c, firstMoveBlack, firstMoveWhite):
		return []

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		return []

	def takeableMoves(self, r, c, board):
		return []

class Pawn(ChessPiece):
	def __init__(self, c):
		super(Pawn, self).__init__(c)
		self.firstMove = True
		self.setImage()

	def piece(self):
		return Piece(pieceType.Pawn, self.color())
	
	def __str__(self):
		return self.color().name + " Pawn"

	def __repr__(self):
		return self.color().name + " Pawn"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-pawn.png")

	def canPromote(self, r, c):
		if self.color() == pieceColor.Black:
			return r == 7
		else:
			return r == 0

	def enPassantLeft(self, r, c, board):
		if self.color() == pieceColor.Black:
			if r < 7 and c > 0:
				return isinstance(board[r][c - 1], Pawn) and board[r][c - 1].color() == pieceColor.White and \
					   isinstance(board[r + 1][c - 1], NoType) and isinstance(board[r + 1][c], NoType)
		else:
			if r > 0 and c > 0:
				return isinstance(board[r][c - 1], Pawn) and board[r][c - 1].color() == pieceColor.Black and \
					   isinstance(board[r - 1][c - 1], NoType) and isinstance(board[r - 1][c], NoType)

	def enPassantRight(self, r, c, board):
		if self.color() == pieceColor.Black:
			if r < 7 and c < 7:
				return isinstance(board[r][c + 1], Pawn) and board[r][c + 1].color() == pieceColor.White and \
				   isinstance(board[r + 1][c + 1], NoType) and isinstance(board[r + 1][c], NoType)
		else:
			if r > 0 and c < 7:
				return isinstance(board[r][c + 1], Pawn) and board[r][c + 1].color() == pieceColor.Black and \
					   isinstance(board[r - 1][c + 1], NoType) and isinstance(board[r - 1][c], NoType)


	def possibleMoves(self, r, c):
		possibleMoves = []
		if self.color() == pieceColor.Black:
			if r + 1 < 8: possibleMoves.append((r + 1, c))
			if self.firstMove:
				if r + 2 < 8: possibleMoves.append((r + 2, c))
		else:
			if r - 1 >= 0: possibleMoves.append((r - 1, c))
			if self.firstMove:
				if r - 2 >= 0: possibleMoves.append((r - 2, c))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))
		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		path = []; newPositions = []; legalMovesAndNotBlocked = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMoves(curPos[0],curPos[1])
		for newPos in newPositions:
			ni, nj = newPos
			if self.color() == pieceColor.Black:
				for i in range(curPos[0] + 1, ni + 1):
					if (i, nj) != curPos:
						path.append((i, nj))
			else:
				for i in range(curPos[0], ni - 1, -1):
					if (i, nj) != curPos:
						path.append((i, nj))
			
		for i, move in enumerate(path):
			r, c = move
			if isinstance(board[r][c], NoType):
				legalMovesAndNotBlocked.append(move)

		return list(set(legalMovesAndNotBlocked))

	def takeableMoves(self, curPos, newPos, board):
		takeableMovesTemp = []; takeableMoves = []

		if self.color() == pieceColor.Black:
			if curPos[0] + 1 < 8:
				if curPos[1] - 1 >= 0: takeableMovesTemp.append((curPos[0] + 1, curPos[1] - 1))
				if curPos[1] + 1 < 8: takeableMovesTemp.append((curPos[0] + 1, curPos[1] + 1))
		else:
			if curPos[0] - 1 >= 0:
				if curPos[1] - 1 >= 0: takeableMovesTemp.append((curPos[0] - 1, curPos[1] - 1))
				if curPos[1] + 1 < 8: takeableMovesTemp.append((curPos[0] - 1, curPos[1] + 1))

		for move in takeableMovesTemp:
			r, c = move
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[curPos[0]][curPos[1]].color():
					takeableMoves.append((r,c))

		return list(set(takeableMoves))

class Rook(ChessPiece):
	def __init__(self, c):
		super(Rook, self).__init__(c)
		self.setImage()
		
	def piece(self):
		return Piece(pieceType.Rook, self.color())

	def __str__(self):
		return self.color().name + " Rook"

	def __repr__(self):
		return self.color().name + " Rook"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-rook.png")

	def possibleMoves(self, r, c):
		return self.possibleMovesUp(r,c) + \
			   self.possibleMovesDown(r,c) + \
			   self.possibleMovesLeft(r,c) + \
			   self.possibleMovesRight(r,c)

	def possibleMovesUp(self, r, c):
		possibleRowsToGoUp = r

		possibleMoves = [(i, c) for i in range(possibleRowsToGoUp + 1) if not (i, c) == (r, c)]
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesDown(self, r, c):
		possibleRowsToGoDown = 7 - r

		possibleMoves = [(i, c) for i in range(r, r + possibleRowsToGoDown + 1) if not (i, c) == (r, c)]
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesLeft(self, r, c):
		possibleColumnsToGoLeft = c

		possibleMoves = [(r, i) for i in range(possibleColumnsToGoLeft, -1, -1) if not (r, i) == (r, c)]
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRight(self, r, c):
		possibleColumnsToGoRight = 7 - c

		possibleMoves = [(r, i) for i in range(c, c + possibleColumnsToGoRight + 1) if not (r, i) == (r, c)]
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		return self.legalMovesAndNotBlockedInPathUp(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathDown(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathLeft(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathRight(curPos, newPos, board)

	def legalMovesAndNotBlockedInPathUp(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesUp(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
			columnIndices = [move[1]	for i in range(curPos[0] - 1, move[0], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathDown(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesDown(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(curPos[0] +  1, move[0])]
			columnIndices = [move[1] for i in range(curPos[0] +  1, move[0])]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathLeft(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeft(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [curPos[0] for j in range(curPos[1] - 1, move[1], -1)]
			columnIndices = [j for j in range(curPos[1] - 1, move[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathRight(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRight(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [curPos[0] for j in range(curPos[1] + 1, move[1])]
			columnIndices = [j for j in range(curPos[1] + 1, move[1])]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		return self.takeableMovesUp(curPos, newPos, board) + \
			   self.takeableMovesDown(curPos, newPos, board) + \
			   self.takeableMovesLeft(curPos, newPos, board) + \
			   self.takeableMovesRight(curPos, newPos, board)

	def takeableMovesUp(self, curPos, newPos, board):
		newPositions = []; takeableMovesUp = []; takeableMovesUpTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesUp(curPos[0],curPos[1])

		for newPos in newPositions:
			if not isinstance(board[newPos[0]][newPos[1]], NoType) and board[newPos[0]][newPos[1]].color() != self.color():
				takeableMovesUpTemp.append(newPos)

		for move in takeableMovesUpTemp:
			if move in self.possibleMovesUp(curPos[0], curPos[1]):
				rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
				columnIndices = [move[1] for i in range(curPos[0] - 1, move[0], -1)]
				zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

				if len(zipped) > 0:
					movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
					if all(move for move in movesOccupied):
						takeableMovesUp.append(move)
				else:
					if not isinstance(board[move[0]][move[1]], NoType):
						takeableMovesUp.append(move)
				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesUp))

	def takeableMovesDown(self, curPos, newPos, board):
		newPositions = []; takeableMovesDown = []; takeableMovesDownTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesDown(curPos[0],curPos[1])

		for newPos in newPositions:
			if not isinstance(board[newPos[0]][newPos[1]], NoType) and board[newPos[0]][newPos[1]].color() != self.color():
				takeableMovesDownTemp.append(newPos)

		for move in takeableMovesDownTemp:
			if move in self.possibleMovesDown(curPos[0],curPos[1]):
				rowIndices = [i for i in range(curPos[0] + 1, move[0])]
				columnIndices = [move[1] for i in range(curPos[0] + 1, move[0])]
				zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

				if len(zipped) > 0:
					movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
					if all(move for move in movesOccupied):
						takeableMovesDown.append(move)
				else:
					if not isinstance(board[move[0]][move[1]], NoType):
						takeableMovesDown.append(move)	
				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesDown))

	def takeableMovesLeft(self, curPos, newPos, board):
		newPositions = []; takeableMovesLeft = []; takeableMovesLeftTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeft(curPos[0],curPos[1])

		for newPos in newPositions:
			if not isinstance(board[newPos[0]][newPos[1]], NoType) and board[newPos[0]][newPos[1]].color() != self.color():
				takeableMovesLeftTemp.append(newPos)

		for move in takeableMovesLeftTemp:
			if move in self.possibleMovesLeft(curPos[0],curPos[1]):
				rowIndices = [move[0] for i in range(curPos[1] - 1, move[1], -1)]
				columnIndices = [i for i in range(curPos[1] - 1, move[1], -1)]
				zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

				if len(zipped) > 0:
					movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
					if all(move for move in movesOccupied):
						takeableMovesLeft.append(move)
				else:
					if not isinstance(board[move[0]][move[1]], NoType):
						takeableMovesLeft.append(move)	

				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeft))

	def takeableMovesRight(self, curPos, newPos, board):
		newPositions = []; takeableMovesRight = []; takeableMovesRightTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRight(curPos[0],curPos[1])

		for newPos in newPositions:
			if not isinstance(board[newPos[0]][newPos[1]], NoType) and board[newPos[0]][newPos[1]].color() != self.color():
				takeableMovesRightTemp.append(newPos)

		for move in takeableMovesRightTemp:
			if move in self.possibleMovesRight(curPos[0],curPos[1]):
				rowIndices = [move[0] for i in range(curPos[1] + 1, move[1])]
				columnIndices = [i for i in range(curPos[1] + 1, move[1])]
				zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

				if len(zipped) > 0:
					movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
					if all(move for move in movesOccupied):
						takeableMovesRight.append(move)
				else:
					if not isinstance(board[move[0]][move[1]], NoType):
						takeableMovesRight.append(move)	

				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesRight))

class Knight(ChessPiece):
	def __init__(self, c):
		super(Knight, self).__init__(c)
		self.setImage()

	def piece(self):
		return Piece(pieceType.Knight, self.color())

	def __str__(self):
		return self.color().name + " Knight"

	def __repr__(self):
		return self.color().name + " Knight"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-knight.png")

	def possibleMoves(self, r, c):
		possibleMoves = []

		if 0 <= r - 2 <= 7 and 0 <= c - 1 <= 7: possibleMoves.append((r - 2, c - 1)) 
		if 0 <= r - 2 <= 7 and 0 <= c + 1 <= 7: possibleMoves.append((r - 2, c + 1))
		if 0 <= r - 1 <= 7 and 0 <= c + 2 <= 7: possibleMoves.append((r - 1, c + 2))
		if 0 <= r + 1 <= 7 and 0 <= c + 2 <= 7: possibleMoves.append((r + 1, c + 2))
		if 0 <= r + 2 <= 7 and 0 <= c + 1 <= 7: possibleMoves.append((r + 2, c + 1))
		if 0 <= r + 2 <= 7 and 0 <= c - 1 <= 7: possibleMoves.append((r + 2, c - 1))
		if 0 <= r - 1 <= 7 and 0 <= c - 2 <= 7: possibleMoves.append((r - 1, c - 2))
		if 0 <= r + 1 <= 7 and 0 <= c - 2 <= 7: possibleMoves.append((r + 1, c - 2))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return possibleMoves

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		possibleMoves = self.possibleMoves(curPos[0],curPos[1])
		legalMoves = [move for move in possibleMoves if isinstance(board[move[0]][move[1]], NoType)]

		return legalMoves

	def takeableMoves(self, curPos, newPos, board):
		takeableMoves = []
		possibleMoves = self.possibleMoves(curPos[0],curPos[1])
		for move in possibleMoves:
			if not isinstance(board[move[0]][move[1]], NoType):
				if board[move[0]][move[1]].color() != board[curPos[0]][curPos[1]].color():
					takeableMoves.append(move)

		return list(set(takeableMoves))

class Bishop(ChessPiece):
	def __init__(self, c):
		super(Bishop, self).__init__(c)
		self.setImage()

	def piece(self):
		return Piece(pieceType.Bishop, self.color())

	def __str__(self):
		return self.color().name + " Bishop"

	def __repr__(self):
		return self.color().name + " Bishop"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-bishop.png")

	def possibleMoves(self, r, c):
		return self.possibleMovesLeftUp(r,c) + \
			   self.possibleMovesRightUp(r,c) + \
			   self.possibleMovesLeftDown(r,c) + \
			   self.possibleMovesRightDown(r,c) 

	def possibleMovesLeftUp(self, r, c):
		possibleMoves = []; rowsDone = []; columnsDone = []
		possibleRowsToGoUp = r
		possibleColumnsToGoLeft = c
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				if possibleRowsToGoUp - possibleColumnsToGoLeft <= i < possibleRowsToGoUp and \
					j < possibleColumnsToGoLeft and i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRightUp(self, r, c):
		possibleMoves = []; rowsDone = []; columnsDone = []
		possibleRowsToGoUp = r
		possibleColumnsToGoRight = 7 - c
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(c, 8):
				if possibleRowsToGoUp - possibleColumnsToGoRight <= i < possibleRowsToGoUp and \
					c < j <= c + possibleColumnsToGoRight and i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesLeftDown(self, r, c):
		possibleMoves = []; rowsDone = []; columnsDone = []
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		for i in range(r, 8):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				if r < i <= r + possibleRowsToGoDown and j < possibleColumnsToGoLeft and \
					i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRightDown(self, r, c):
		possibleMoves = []; rowsDone = []; columnsDone = []
		for i in range(r, 8):
			for j in range(c, 8):
				if i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		return self.legalMovesAndNotBlockedInPathLeftUp(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathRightUp(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathLeftDown(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathRightDown(curPos, newPos, board)

	def legalMovesAndNotBlockedInPathLeftUp(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeftUp(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
			columnIndices = [j for j in range(curPos[1] - 1, move[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(path))

	def legalMovesAndNotBlockedInPathRightUp(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRightUp(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
			columnIndices = [j for j in range(move[1], curPos[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, reversed(columnIndices))]
			zipped.append(move)
			
			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
			
			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))
			
			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathLeftDown(self, curPos, newPos, board):
		path = []; rowIndices = []; columnIndices = []; newPositions = []; movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeftDown(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(move[0] - 1, curPos[0], -1)]
			columnIndices = [j for j in range(curPos[1] - 1, move[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, reversed(columnIndices))]
			zipped.append(move)

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathRightDown(self, curPos, newPos, board):
		path = []; movesOccupied = []; rowIndices = []; columnIndices = []; newPositions = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRightDown(curPos[0],curPos[1])
		for move in newPositions:
			rowIndices = [i for i in range(move[0], curPos[0], -1)]
			columnIndices = [j for j in range(move[1], curPos[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

			movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		return self.takeableMovesLeftUp(curPos, newPos, board) + \
			   self.takeableMovesRightUp(curPos, newPos, board) + \
			   self.takeableMovesLeftDown(curPos, newPos, board) + \
			   self.takeableMovesRightDown(curPos, newPos, board)

	def takeableMovesLeftUp(self, curPos, newPos, board):
		takeableMovesLeftUp = []; takeableMovesLeftUpTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		possibleMovesLeftUp = self.possibleMovesLeftUp(curPos[0],curPos[1])
		for move in possibleMovesLeftUp:
			if not isinstance(board[move[0]][move[1]], NoType) and self.color() != board[move[0]][move[1]].color():
				takeableMovesLeftUpTemp.append(move)

		for move in takeableMovesLeftUpTemp:
			rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
			columnIndices = [j for j in range(curPos[1] - 1, move[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

			if len(zipped) > 0:
				movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
				if all(move for move in movesOccupied):
					takeableMovesLeftUp.append(move)
			elif not isinstance(board[move[0]][move[1]], NoType):
				takeableMovesLeftUp.append(move)

			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeftUp))

	def takeableMovesRightUp(self, curPos, newPos, board):
		takeableMovesRightUp = []; takeableMovesRightUpTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		possibleMovesRightUp = self.possibleMovesRightUp(curPos[0],curPos[1])
		for move in possibleMovesRightUp:
			if not isinstance(board[move[0]][move[1]], NoType) and self.color() != board[move[0]][move[1]].color():
				takeableMovesRightUpTemp.append(move)

		for move in takeableMovesRightUpTemp:
			rowIndices = [i for i in range(curPos[0] - 1, move[0], -1)]
			columnIndices = [j for j in range(curPos[1] + 1, move[1])]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

			if len(zipped) > 0:
				movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
				if all(move for move in movesOccupied):
					takeableMovesRightUp.append(move)
			elif not isinstance(board[move[0]][move[1]], NoType):
				takeableMovesRightUp.append(move)

			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesRightUp))

	def takeableMovesLeftDown(self, curPos, newPos, board):
		takeableMovesLeftDown = []; takeableMovesLeftDownTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		possibleMovesLeftDown = self.possibleMovesLeftDown(curPos[0],curPos[1])
		for move in possibleMovesLeftDown:
			if not isinstance(board[move[0]][move[1]], NoType) and self.color() != board[move[0]][move[1]].color():
				takeableMovesLeftDownTemp.append(move)
		
		for move in takeableMovesLeftDownTemp:
			rowIndices = [i for i in range(move[0] - 1, curPos[0] - 1, -1)]
			columnIndices = [j for j in range(curPos[1] - 1, move[1], -1)]
			zipped = [(i,j) for i,j in zip(rowIndices, reversed(columnIndices))]
			
			if len(zipped) > 0:
				movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
				if all(move for move in movesOccupied):
					takeableMovesLeftDown.append(move)
			elif not isinstance(board[move[0]][move[1]], NoType):
				takeableMovesLeftDown.append(move)

			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeftDown))
	
	def takeableMovesRightDown(self, curPos, newPos, board):
		takeableMovesRightDown = []; takeableMovesRightDownTemp = []; rowIndices = []; columnIndices = []; movesOccupied = []

		possibleMovesRightDown = self.possibleMovesRightDown(curPos[0],curPos[1])
		for move in possibleMovesRightDown:
			if not isinstance(board[move[0]][move[1]], NoType) and self.color() != board[move[0]][move[1]].color():
				takeableMovesRightDownTemp.append(move)
		
		for move in takeableMovesRightDownTemp:
			rowIndices = [i	for i in range(curPos[0] + 1, move[0])]
			columnIndices = [j for j in range(curPos[1] + 1, move[1])]
			zipped = [(i,j) for i,j in zip(rowIndices, columnIndices)]

			if len(zipped) > 0:
				movesOccupied = [isinstance(board[zipMove[0]][zipMove[1]], NoType) for zipMove in zipped]
				if all(move for move in movesOccupied):
					takeableMovesRightDown.append(move)
			elif not isinstance(board[move[0]][move[1]], NoType):
				takeableMovesRightDown.append(move)

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(takeableMovesRightDown))

class Queen(ChessPiece):
	def __init__(self, c):
		super(Queen, self).__init__(c)
		self.setImage()

	def piece(self):
		return Piece(pieceType.Queen, self.color())

	def __str__(self):
		return self.color().name + " Queen"

	def __repr__(self):
		return self.color().name + " Queen"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-queen.png")

	def possibleMoves(self, r, c):
		possibleMoves = []

		possibleMoves.append(Rook(self.color()).possibleMoves(r,c))
		possibleMoves.append(Bishop(self.color()).possibleMoves(r,c))
		possibleMoves = list(itertools.chain(*possibleMoves))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))
		
		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		path = []
		path.append(Rook(self.color()).legalMovesAndNotBlockedInPath(curPos, newPos, board))
		path.append(Bishop(self.color()).legalMovesAndNotBlockedInPath(curPos, newPos, board))
		path = list(itertools.chain(*path))
		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		path = []
		path.append(Rook(self.color()).takeableMoves(curPos, newPos, board))
		path.append(Bishop(self.color()).takeableMoves(curPos, newPos, board))
		path = list(itertools.chain(*path))
		return list(set(path))

class King(ChessPiece):
	def __init__(self, c):
		super(King, self).__init__(c)
		self.setImage()

	def piece(self):
		return Piece(pieceType.King, self.color())

	def __str__(self):
		return self.color().name + " King"

	def __repr__(self):
		return self.color().name + " King"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-king.png")

	def possibleMoves(self, r, c):
		possibleMoves = []

		if 0 <= r - 1 <= 7 and 0 <= c - 1 <= 7: possibleMoves.append((r - 1, c - 1)) 
		if 0 <= r - 1 <= 7 and 0 <= c <= 7: 	possibleMoves.append((r - 1, c))
		if 0 <= r - 1 <= 7 and 0 <= c + 1 <= 7: possibleMoves.append((r - 1, c + 1))
		if 0 <= r <= 7 and 0 <= c + 1 <= 7: 	possibleMoves.append((r, c - 1))
		if 0 <= r <= 7 and 0 <= c + 1 <= 7: 	possibleMoves.append((r, c + 1))
		if 0 <= r + 1 <= 7 and 0 <= c - 1 <= 7: possibleMoves.append((r + 1, c - 1))
		if 0 <= r + 1 <= 7 and 0 <= c <= 7: 	possibleMoves.append((r + 1, c))
		if 0 <= r + 1 <= 7 and 0 <= c + 1 <= 7: possibleMoves.append((r + 1, c + 1))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))
		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		temp = self.possibleMoves(curPos[0], curPos[1])
		path = []
		for move in temp:
			r, c = move
			if isinstance(board[r][c], NoType):
				path.append(move)

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		takeableMoves = []
		temp = self.possibleMoves(curPos[0], curPos[1])

		for move in temp:
			r, c = move
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[curPos[0]][curPos[1]].color():
					takeableMoves.append((r,c))

		return list(set(takeableMoves))