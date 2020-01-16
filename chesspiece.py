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

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos):
		return []

	def takeableMoves(self, r, c):
		return []

class Pawn(ChessPiece):
	def __init__(self, c):
		super(Pawn, self).__init__(c)

	def piece(self):
		return Piece(pieceType.Pawn, self.color())
	
	def __str__(self):
		return self.color().name + " Pawn"

	def __repr__(self):
		return self.color().name + " Pawn"

	def setImage(self):
		self.image = PhotoImage(file="resources/" + self.pColor.name.lower() + "-pawn.png")

	def possibleMoves(self, r, c, firstMoveBlack=False, firstMoveWhite=False):
		possibleMoves = []
		if self.color() == pieceColor.Black:
			if r + 1 < 8: possibleMoves.append((r + 1, c))
			if firstMoveBlack:
				if r + 2 < 8: possibleMoves.append((r + 2, c))
		else:
			if r - 1 >= 0: possibleMoves.append((r - 1, c))
			if firstMoveWhite:
				if r - 2 >= 0: possibleMoves.append((r - 2, c))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))
		return list(set(possibleMoves))

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
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
			# print(curPos)
			print(newPos)
			if self.color() == pieceColor.Black:
				# print(ci + 1, ni + 1)
				for i in range(ci + 1, ni + 1):
					if (i, nj) != curPos:
						path.append((i, nj))
			else:
				# print(ci, ni - 1, '-1')
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

	def possibleMoves(self, r, c, _=None, __=None):
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c

		# Rows to go up
		for i in range(possibleRowsToGoUp + 1):
			if not (i, c) == (r, c):
				possibleMoves.append((i, c))
		# Rows to go down
		for i in range(r, r + possibleRowsToGoDown + 1):
			if not (i, c) == (r, c):
				possibleMoves.append((i, c))
		# Columns to go left
		for i in range(possibleColumnsToGoLeft, -1, -1):
			if not (r, i) == (r, c):
				possibleMoves.append((r, i))
		# Columns to go right
		for i in range(c, c + possibleColumnsToGoRight + 1):
			if not (r, i) == (r, c):
				possibleMoves.append((r, i))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		ci, cj = curPos
		newPositions = []
		path = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMoves(ci,cj)
		print("newPositions", newPositions)
		for newPos in newPositions:
			ni, nj = newPos
			if isinstance(board[ni][nj], NoType):
				path.append(newPos)
		# for newPos in newPositions:
		# 	temp = []
		# 	ni, nj = newPos

		# 	if self.color() == pieceColor.Black:
		# 		print("range", ci + 1, ni + 1)
		# 		for i in range(ci + 1, ni + 1):
		# 			if (i, nj) != curPos:
		# 				temp.append((i, nj))
		# 	else:
		# 		for i in range(ci, ni - 1, -1):
		# 			if (i, nj) != curPos:
		# 				temp.append((i, nj))

		# 	# print(board[ci][cj],"temp",temp)
		# for move in temp:
		# 	r, c = move
		# 	if isinstance(board[r][c], NoType):
		# 		path.append((r,c))
		# 	else:
		# 		break
		# print("path", path)
		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		ci, cj = curPos
		newPositions = []
		path = []

		if newPos:
			newPositions.append(newPos)
		else:
			newPositions = self.possibleMoves(ci,cj)

		for newPos in newPositions:
			ni, nj = newPos
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				path.append(newPos)

		return list(set(path))

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

	def possibleMoves(self, r, c, _=None, __=None):
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

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		return []

	def takeableMoves(self, curPos, newPos, board):
		ci,cj = curPos
		takeableMoves = []
		temp = self.possibleMoves(ci,cj)
		for move in temp:
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

	def possibleMoves(self, r, c, _=None, __=None):
		return self.possibleMovesLeftUp(r,c) + self.possibleMovesRightUp(r,c) + self.possibleMovesLeftDown(r,c) + self.possibleMovesRightDown(r,c) 

	def possibleMovesLeftUp(self, r, c, _=None, __=None):
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c

		# Diagonal left up
		rowsDone = []
		columnsDone = []
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				if possibleRowsToGoUp - possibleColumnsToGoLeft <= i < possibleRowsToGoUp and \
					j < possibleColumnsToGoLeft and \
					i not in rowsDone and \
					j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRightUp(self, r, c, _=None, __=None):
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c
		# Diagonal right up
		rowsDone = []
		columnsDone = []
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(c, 8):
				if possibleRowsToGoUp - possibleColumnsToGoRight <= i < possibleRowsToGoUp and \
					c < j <=c + possibleColumnsToGoRight and \
					i not in rowsDone and \
					j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesLeftDown(self, r, c, _=None, __=None):
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c
		# print("possibleRowsToGoUp",possibleRowsToGoUp)
		# print("possibleRowsToGoDown",possibleRowsToGoDown)
		# print("possibleColumnsToGoLeft",possibleColumnsToGoLeft)
		# print("possibleColumnsToGoRight",possibleColumnsToGoRight)
		# Diagonal left down
		rowsDone = []
		columnsDone = []
		for i in range(r, 8):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				if r < i <= r + possibleRowsToGoDown and \
					j < possibleColumnsToGoLeft and \
					i not in rowsDone and \
					j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))

		return list(set(possibleMoves))

	def possibleMovesRightDown(self, r, c, _=None, __=None):
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c
		# # Diagonal right down
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

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		ci, cj = curPos
		path = []
		addMoveToPath = True
		rowIndices = []
		columnIndices = []

		possibleRowsToGoUp = ci
		possibleRowsToGoDown = 7 - ci
		possibleColumnsToGoLeft = cj
		possibleColumnsToGoRight = 7 - cj

		# Diagonal left up
		newPositions = []
		movesOccupied = []
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
				addMoveToPath = (addMoveToPath and isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []
			rowIndices = []
			columnIndices = []
		addMoveToPath = True
		
		# Diagonal right up
		newPositions = []
		movesOccupied = []
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
				addMoveToPath = (addMoveToPath and isinstance(board[zi][zj], NoType))
			
			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))
			
			movesOccupied = []
			rowIndices = []
			columnIndices = []
		addMoveToPath = True

		# Diagonal left down
		newPositions = []
		movesOccupied = []
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
				addMoveToPath = (addMoveToPath and isinstance(board[zi][zj], NoType))

			if all(move for move in movesOccupied):
				path.append(move)
			path = list(set(path))

			movesOccupied = []
			rowIndices = []
			columnIndices = []
		addMoveToPath = True

		# Diagonal right down
		newPositions = []
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

			for zipMove in reversed(zipped):
				zi, zj = zipMove
				addMoveToPath = (addMoveToPath and isinstance(board[zi][zj], NoType))
			if addMoveToPath:
				path.append(move)

			addMoveToPath = True
			rowIndices = []
			columnIndices = []

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		takeableMoves = []
		ci, cj = curPos
		legalMovesAndNotBlocked = self.getLegalMovesAndNotBlockedInPath(curPos, newPos, board)
		possibleMoves = self.possibleMoves(ci,cj)
		intersection = [move for move in legalMovesAndNotBlocked if move in possibleMoves]
		temp = legalMovesAndNotBlocked + intersection # TODO
		print("temp",temp)
		for move in temp:
			r, c = move
			# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
			# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))
					# if move in legalMovesAndNotBlocked:

		return list(set(takeableMoves))

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

	def possibleMoves(self, r, c, _=None, __=None):
		possibleMoves = []

		possibleMoves.append(Rook(self.color()).possibleMoves(r,c))
		possibleMoves.append(Bishop(self.color()).possibleMoves(r,c))
		possibleMoves = list(itertools.chain(*possibleMoves))

		if (r,c) in possibleMoves:
			possibleMoves.remove((r,c))
		
		return list(set(possibleMoves))

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		path = []
		path.append(Rook(self.color()).getLegalMovesAndNotBlockedInPath(curPos, newPos, board))
		path.append(Bishop(self.color()).getLegalMovesAndNotBlockedInPath(curPos, newPos, board))
		path = list(itertools.chain(*path))
		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		path = []
		path.append(Rook(self.color()).takeableMoves(curPos, newPos, board))
		path.append(Bishop(self.color()).takeableMoves(curPos, newPos, board))
		path = list(itertools.chain(*path))
		# print("takeableMoves Queen", path)
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

	def possibleMoves(self, r, c, _=None, __=None):
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

	def getLegalMovesAndNotBlockedInPath(self, curPos, newPos, board):
		ci, cj = curPos
		temp = self.possibleMoves(ci, cj)
		path = []
		for move in temp:
			r, c = move
			if isinstance(board[r][c], NoType):
				path.append((r,c))
			else:
				break
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