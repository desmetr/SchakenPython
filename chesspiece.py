from chessboard import pieceColor, pieceType, Piece
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

	def legalMovesAndNotBlockedInPath(self, curPos, newPos):
		return []

	def takeableMoves(self, r, c):
		return []

class Pawn(ChessPiece):
	def __init__(self, c):
		super(Pawn, self).__init__(c)
		self.firstMove = True

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
		ci, cj = curPos
		path = []
		newPositions = []
		legalMovesAndNotBlocked = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMoves(ci,cj)
		for newPos in newPositions:
			ni, nj = newPos
			if self.color() == pieceColor.Black:
				for i in range(ci + 1, ni + 1):
					if (i, nj) != curPos:
						path.append((i, nj))
			else:
				for i in range(ci, ni - 1, -1):
					if (i, nj) != curPos:
						path.append((i, nj))
			
		for i, move in enumerate(path):
			r, c = move
			if isinstance(board[r][c], NoType):
				legalMovesAndNotBlocked.append(move)

		return list(set(legalMovesAndNotBlocked))

	def takeableMoves(self, curPos, newPos, board):
		temp = []
		takeableMoves = []
		ci, cj = curPos
		if self.color() == pieceColor.Black:
			if ci + 1 < 8:
				if cj - 1 >= 0: temp.append((ci + 1, cj - 1))
				if cj + 1 < 8: temp.append((ci + 1, cj + 1))
		else:
			if ci - 1 >= 0:
				if cj - 1 >= 0: temp.append((ci - 1, cj - 1))
				if cj + 1 < 8: temp.append((ci - 1, cj + 1))

		for move in temp:
			r, c = move
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))

		return list(set(takeableMoves))

class Rook(ChessPiece):
	def __init__(self, c):
		super(Rook, self).__init__(c)

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
		possibleMoves = []
		possibleRowsToGoUp = r
		# Rows to go up
		for i in range(possibleRowsToGoUp + 1):
			if not (i, c) == (r, c):
				possibleMoves.append((i, c))
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesDown(self, r, c):
		possibleMoves = []
		possibleRowsToGoDown = 7 - r
		# Rows to go down
		for i in range(r, r + possibleRowsToGoDown + 1):
			if not (i, c) == (r, c):
				possibleMoves.append((i, c))
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesLeft(self, r, c):
		possibleMoves = []
		possibleColumnsToGoLeft = c
		# Columns to go left
		for i in range(possibleColumnsToGoLeft, -1, -1):
			if not (r, i) == (r, c):
				possibleMoves.append((r, i))
		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRight(self, r, c):
		possibleMoves = []
		possibleColumnsToGoRight = 7 - c
		# Columns to go right
		for i in range(c, c + possibleColumnsToGoRight + 1):
			if not (r, i) == (r, c):
				possibleMoves.append((r, i))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def legalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		return self.legalMovesAndNotBlockedInPathUp(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathDown(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathLeft(curPos, newPos, board) + \
			   self.legalMovesAndNotBlockedInPathRight(curPos, newPos, board)

	def legalMovesAndNotBlockedInPathUp(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Up
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesUp(ci,cj)
		for move in newPositions:
			mi, mj = move

			for i in range(ci - 1, mi, -1):
				rowIndices.append(i)
				columnIndices.append(mj)
			
			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			zipped.append(move)

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathDown(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Down
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesDown(ci,cj)
		for move in newPositions:
			mi, mj = move
			for i in range(ci +  1, mi):
				rowIndices.append(i)
				columnIndices.append(mj)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			zipped.append(move)
			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathLeft(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Left
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeft(ci,cj)
		for move in newPositions:
			mi, mj = move

			for j in range(cj - 1, mj, -1):
				rowIndices.append(ci)
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			zipped.append(move)

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathRight(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Right
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRight(ci,cj)
		for move in newPositions:
			mi, mj = move
			
			for j in range(cj + 1, mj,):
				rowIndices.append(ci)
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			zipped.append(move)

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

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
		ci, cj = curPos
		newPositions = []
		takeableMovesUp = []
		takeableMovesUpTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesUp(ci,cj)

		for newPos in newPositions:
			ni, nj = newPos
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				takeableMovesUpTemp.append(newPos)

		for move in takeableMovesUpTemp:
			mi, mj = move
			if move in self.possibleMovesUp(ci, cj):
				for i in range(ci - 1, mi, -1):
					rowIndices.append(i)
					columnIndices.append(mj)

				zipped = []
				for i,j in zip(rowIndices, columnIndices):
					zipped.append((i,j))
				if len(zipped) > 0:
					for zipMove in zipped:
						zi, zj = zipMove
						movesOccupied.append(isinstance(board[zi][zj], NoType))
					if all(move for move in movesOccupied):
						takeableMovesUp.append(move)
				else:
					if not isinstance(board[mi][mj], NoType):
						takeableMovesUp.append(move)
				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesUp))

	def takeableMovesDown(self, curPos, newPos, board):
		ci, cj = curPos
		newPositions = []
		takeableMovesDown = []
		takeableMovesDownTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesDown(ci,cj)

		for newPos in newPositions:
			ni, nj = newPos
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				takeableMovesDownTemp.append(newPos)

		for move in takeableMovesDownTemp:
			mi, mj = move
			if move in self.possibleMovesDown(ci,cj):
				for i in range(ci + 1, mi):
					rowIndices.append(i)
					columnIndices.append(mj)

				zipped = []
				for i,j in zip(rowIndices, columnIndices):
					zipped.append((i,j))

				if len(zipped) > 0:
					for zipMove in zipped:
						zi, zj = zipMove
						movesOccupied.append(isinstance(board[zi][zj], NoType))
					if all(move for move in movesOccupied):
						takeableMovesDown.append(move)
				else:
					if not isinstance(board[mi][mj], NoType):
						takeableMovesDown.append(move)	
				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesDown))

	def takeableMovesLeft(self, curPos, newPos, board):
		ci, cj = curPos
		newPositions = []
		takeableMovesLeft = []
		takeableMovesLeftTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeft(ci,cj)

		for newPos in newPositions:
			ni, nj = newPos
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				takeableMovesLeftTemp.append(newPos)

		for move in takeableMovesLeftTemp:
			mi, mj = move
			if move in self.possibleMovesLeft(ci,cj):
				for i in range(cj - 1, mj, -1):
					rowIndices.append(mi)
					columnIndices.append(i)

				zipped = []
				for i,j in zip(rowIndices, columnIndices):
					zipped.append((i,j))

				if len(zipped) > 0:
					for zipMove in zipped:
						zi, zj = zipMove
						movesOccupied.append(isinstance(board[zi][zj], NoType))
					if all(move for move in movesOccupied):
						takeableMovesLeft.append(move)
				else:
					if not isinstance(board[mi][mj], NoType):
						takeableMovesLeft.append(move)	

				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeft))

	def takeableMovesRight(self, curPos, newPos, board):
		ci, cj = curPos
		newPositions = []
		takeableMovesRight = []
		takeableMovesRightTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRight(ci,cj)

		for newPos in newPositions:
			ni, nj = newPos
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				takeableMovesRightTemp.append(newPos)

		for move in takeableMovesRightTemp:
			mi, mj = move
			if move in self.possibleMovesRight(ci,cj):
				for i in range(cj + 1, mj):
					rowIndices.append(mi)
					columnIndices.append(i)

				zipped = []
				for i,j in zip(rowIndices, columnIndices):
					zipped.append((i,j))

				if len(zipped) > 0:
					for zipMove in zipped:
						zi, zj = zipMove
						movesOccupied.append(isinstance(board[zi][zj], NoType))
					if all(move for move in movesOccupied):
						takeableMovesRight.append(move)
				else:
					if not isinstance(board[mi][mj], NoType):
						takeableMovesRight.append(move)	

				movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesRight))

class Knight(ChessPiece):
	def __init__(self, c):
		super(Knight, self).__init__(c)

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
		ci,cj = curPos
		legalMoves = []
		possibleMoves = self.possibleMoves(ci, cj)
		for move in possibleMoves:
			r, c = move
			if isinstance(board[r][c], NoType):
				legalMoves.append(move)

		return legalMoves

	def takeableMoves(self, curPos, newPos, board):
		ci,cj = curPos
		takeableMoves = []
		possibleMoves = self.possibleMoves(ci,cj)
		for move in possibleMoves:
			r, c = move
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))

		return list(set(takeableMoves))

class Bishop(ChessPiece):
	def __init__(self, c):
		super(Bishop, self).__init__(c)

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
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleColumnsToGoLeft = c

		# Diagonal left up
		rowsDone = []
		columnsDone = []
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
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleColumnsToGoRight = 7 - c

		# Diagonal right up
		rowsDone = []
		columnsDone = []
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(c, 8):
				if possibleRowsToGoUp - possibleColumnsToGoRight <= i < possibleRowsToGoUp and \
					c < j <=c + possibleColumnsToGoRight and i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesLeftDown(self, r, c):
		possibleMoves = []
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c

		# Diagonal left down
		rowsDone = []
		columnsDone = []
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
		possibleMoves = []
		
		# Diagonal right down
		rowsDone = []
		columnsDone = []
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
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Diagonal left up
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeftUp(ci,cj)
		for move in newPositions:
			mi, mj = move
			for i in range(ci-1, mi, -1):
				rowIndices.append(i)
			for j in range(cj-1, mj, -1): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			zipped.append(move)

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(path))

	def legalMovesAndNotBlockedInPathRightUp(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Diagonal right up
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRightUp(ci,cj)
		for move in newPositions:
			mi, mj = move
			for i in range(ci-1, mi, -1):
				rowIndices.append(i)
			for j in range(mj, cj, -1): 
				columnIndices.append(j)
			
			zipped = []
			for i,j in zip(rowIndices, reversed(columnIndices)):
				zipped.append((i,j))
			zipped.append(move)
			
			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))
			
			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))
			
			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathLeftDown(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		rowIndices = []
		columnIndices = []
		newPositions = []
		movesOccupied = []

		# Diagonal left down
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesLeftDown(ci,cj)
		for move in newPositions:
			mi, mj = move
			for i in range(mi - 1, ci, -1):
				rowIndices.append(i)
			for j in range(cj - 1, mj, -1): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, reversed(columnIndices)):
				zipped.append((i,j))
			zipped.append(move)

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(path))

	def legalMovesAndNotBlockedInPathRightDown(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		movesOccupied = []
		rowIndices = []
		columnIndices = []
		newPositions = []

		# Diagonal right down
		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMovesRightDown(ci,cj)
		for move in newPositions:
			mi, mj = move
			for i in range(mi, ci, -1):
				rowIndices.append(i)
			for j in range(mj, cj, -1): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))

			for zipMove in zipped:
				zi, zj = zipMove
				movesOccupied.append(isinstance(board[zi][zj], NoType))

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
		ci, cj = curPos
		takeableMovesLeftUp = []
		takeableMovesLeftUpTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		possibleMovesLeftUp = self.possibleMovesLeftUp(ci,cj)
		for move in possibleMovesLeftUp:
			mi, mj = move
			if not isinstance(board[mi][mj], NoType) and self.color() != board[mi][mj].color():
				takeableMovesLeftUpTemp.append(move)

		for move in takeableMovesLeftUpTemp:
			mi, mj = move
			for i in range(ci - 1, mi, -1):
				rowIndices.append(i)
			for j in range(cj - 1, mj, -1): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))

			if len(zipped) > 0:
				for zipMove in zipped:
					zi, zj = zipMove
					movesOccupied.append(isinstance(board[zi][zj], NoType))
				if all(move for move in movesOccupied):
					takeableMovesLeftUp.append(move)
			else:
				if not isinstance(board[mi][mj], NoType):
					takeableMovesLeftUp.append(move)
			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeftUp))

	def takeableMovesRightUp(self, curPos, newPos, board):
		ci, cj = curPos
		takeableMovesRightUp = []
		takeableMovesRightUpTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		possibleMovesRightUp = self.possibleMovesRightUp(ci,cj)
		for move in possibleMovesRightUp:
			mi, mj = move
			if not isinstance(board[mi][mj], NoType) and self.color() != board[mi][mj].color():
				takeableMovesRightUpTemp.append(move)

		for move in takeableMovesRightUpTemp:
			mi, mj = move
			for i in range(ci - 1, mi, -1):
				rowIndices.append(i)
			for j in range(cj + 1, mj): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			if len(zipped) > 0:
				for zipMove in zipped:
					zi, zj = zipMove
					movesOccupied.append(isinstance(board[zi][zj], NoType))
				if all(move for move in movesOccupied):
					takeableMovesRightUp.append(move)
			else:
				if not isinstance(board[mi][mj], NoType):
					takeableMovesRightUp.append(move)
			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesRightUp))

	def takeableMovesLeftDown(self, curPos, newPos, board):
		ci, cj = curPos
		takeableMovesLeftDown = []
		takeableMovesLeftDownTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		possibleMovesLeftDown = self.possibleMovesLeftDown(ci,cj)
		for move in possibleMovesLeftDown:
			mi, mj = move
			if not isinstance(board[mi][mj], NoType) and self.color() != board[mi][mj].color():
				takeableMovesLeftDownTemp.append(move)
		
		for move in takeableMovesLeftDownTemp:
			mi, mj = move
			for i in range(mi - 1, ci - 1, -1):
				rowIndices.append(i)
			for j in range(cj - 1, mj, -1): 
				columnIndices.append(j)
			zipped = []
			for i,j in zip(rowIndices, reversed(columnIndices)):
				zipped.append((i,j))
			if len(zipped) > 0:
				for zipMove in zipped:
					zi, zj = zipMove
					movesOccupied.append(isinstance(board[zi][zj], NoType))
				if all(move for move in movesOccupied):
					takeableMovesLeftDown.append(move)
			else:
				if not isinstance(board[mi][mj], NoType):
					takeableMovesLeftDown.append(move)
			movesOccupied = []; rowIndices = []; columnIndices = []
		
		return list(set(takeableMovesLeftDown))
	
	def takeableMovesRightDown(self, curPos, newPos, board):
		ci, cj = curPos
		takeableMovesRightDown = []
		takeableMovesRightDownTemp = []
		rowIndices = []
		columnIndices = []
		movesOccupied = []

		possibleMovesRightDown = self.possibleMovesRightDown(ci,cj)
		for move in possibleMovesRightDown:
			mi, mj = move
			if not isinstance(board[mi][mj], NoType) and self.color() != board[mi][mj].color():
				takeableMovesRightDownTemp.append(move)
		
		for move in takeableMovesRightDownTemp:
			mi, mj = move
			for i in range(ci + 1, mi):
				rowIndices.append(i)
			for j in range(cj + 1, mj): 
				columnIndices.append(j)

			zipped = []
			for i,j in zip(rowIndices, columnIndices):
				zipped.append((i,j))
			if len(zipped) > 0:
				for zipMove in zipped:
					zi, zj = zipMove
					movesOccupied.append(isinstance(board[zi][zj], NoType))
				if all(move for move in movesOccupied):
					takeableMovesRightDown.append(move)
			else:
				if not isinstance(board[mi][mj], NoType):
					takeableMovesRightDown.append(move)
			movesOccupied = []; rowIndices = []; columnIndices = []

		return list(set(takeableMovesRightDown))

class Queen(ChessPiece):
	def __init__(self, c):
		super(Queen, self).__init__(c)

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
		ci, cj = curPos
		temp = self.possibleMoves(ci, cj)
		path = []
		for move in temp:
			r, c = move
			if isinstance(board[r][c], NoType):
				path.append(move)

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		ci,cj = curPos
		takeableMoves = []
		temp = self.possibleMoves(ci, cj)

		for move in temp:
			r, c = move
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))

		return list(set(takeableMoves))