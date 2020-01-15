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
		print("(r,c)", r,c)
		if self.color() == pieceColor.Black:
			if r + 1 < 8: possibleMoves.append((r + 1, c))
			if firstMoveBlack:
				if r + 2 < 8: possibleMoves.append((r + 2, c))
		else:
			if r - 1 >= 0: possibleMoves.append((r - 1, c))
			if firstMoveWhite:
				if r - 2 >= 0: possibleMoves.append((r - 2, c))
		print("possibleMoves",possibleMoves)
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
			if ci - 1 > 0:
				if cj - 1 >= 0: temp.append((ci - 1, cj - 1))
				if cj + 1 < 8: temp.append((ci - 1, cj + 1))
		for move in temp:
			r, c = move
			# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
			# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))
				else:
					# print("############ JA")
					break
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
		# print("possibleRowsToGoUp", possibleRowsToGoUp)
		# print("possibleRowsToGoDown", possibleRowsToGoDown)
		# print("possibleColumnsToGoLeft", possibleColumnsToGoLeft)
		# print("possibleColumnsToGoRight", possibleColumnsToGoRight)

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
		# print("newPositions", newPositions)
		for newPos in newPositions:
			ni, nj = newPos
			# print(newPos)
			# print("not ", isinstance(board[ni][nj], NoType), " and ", board[ni][nj].color(), " != ", self.color())
			if not isinstance(board[ni][nj], NoType) and board[ni][nj].color() != self.color():
				path.append(newPos)

		# path = []
		# temp = []
		# ci, cj = curPos
		# ni, nj = newPos

		# if self.color() == pieceColor.Black:
		# 	for i in range(ci + 1, ni + 1):
		# 		if (i, nj) != curPos:
		# 			temp.append((i, nj))
		# else:
		# 	# print("range", ci, ni - 1)
		# 	for i in range(ci, ni - 1, -1):
		# 		if (i, nj) != curPos:
		# 			temp.append((i, nj))
		# # print(board[ci][cj],"temp",temp)
		# for move in temp:
		# 	r, c = move
		# 	# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
		# 	# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
		# 	if not isinstance(board[r][c], NoType):
		# 		if board[r][c].color() != board[ci][cj].color():
		# 			path.append((r,c))
		# 		else:
		# 			# print("############ JA")
		# 			break
		# print("path", path)
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
			# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
			# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))
				else:
					# print("############ JA")
					break
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
		# r = 4
		# c = 2
		possibleMoves = []
		possibleRowsToGoUp = r
		possibleRowsToGoDown = 7 - r
		possibleColumnsToGoLeft = c
		possibleColumnsToGoRight = 7 - c
		# print("possibleRowsToGoUp", possibleRowsToGoUp)
		# print("possibleRowsToGoDown", possibleRowsToGoDown)
		# print("possibleColumnsToGoLeft", possibleColumnsToGoLeft)
		# print("possibleColumnsToGoRight", possibleColumnsToGoRight)

		# Diagonal left up
		rowsDone = []
		columnsDone = []
		# print("rangeI", possibleRowsToGoUp, "->", 0)
		# print("rangeJ", possibleColumnsToGoLeft, "->", -1)
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				# print(possibleRowsToGoUp - possibleColumnsToGoLeft, " <= ", i , " < ", possibleRowsToGoUp, " and ", j ," < ", possibleColumnsToGoLeft)
				if possibleRowsToGoUp - possibleColumnsToGoLeft <= i < possibleRowsToGoUp and \
					j < possibleColumnsToGoLeft and \
					i not in rowsDone and \
					j not in columnsDone:
						# print((i,j))
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)
		# print("possibleMoves1", possibleMoves)
		# Diagonal right up
		rowsDone = []
		columnsDone = []
		for i in range(possibleRowsToGoUp, -1, -1):
			for j in range(c, 8):
				# print("if ", possibleRowsToGoUp - possibleColumnsToGoRight, " <= ", i, " < ", possibleRowsToGoUp, " and ", c, " < ", j, " <= ", c + possibleColumnsToGoRight)
				if possibleRowsToGoUp - possibleColumnsToGoRight <= i < possibleRowsToGoUp and \
					c < j <=c + possibleColumnsToGoRight and \
					i not in rowsDone and \
					j not in columnsDone:
						# print((i,j))
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)
		# print("possibleMoves2", possibleMoves)
					
		# Diagonal left down
		rowsDone = []
		columnsDone = []
		for i in range(r, 8):
			for j in range(possibleColumnsToGoLeft, -1, -1):
				# print("if ", r, " < ", i, " <= ", r + possibleRowsToGoDown, " and ", j, " < ", possibleColumnsToGoLeft)
				if r < i <= r + possibleRowsToGoDown and \
					j < possibleColumnsToGoLeft and \
					i not in rowsDone and \
					j not in columnsDone:
						# print((i,j))
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)
		# print("possibleMoves3", possibleMoves)

		# # Diagonal right down
		rowsDone = []
		columnsDone = []
		for i in range(r, 8):
			for j in range(c, 8):
				if i not in rowsDone and j not in columnsDone:
						possibleMoves.append((i, j))
						rowsDone.append(i)
						columnsDone.append(j)
		# print("possibleMoves4", possibleMoves)

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
		for newPos in newPositions:
			ni, nj = newPos
			possibleRowsToGoUp = ci
			possibleRowsToGoDown = 7 - ci
			possibleColumnsToGoLeft = cj
			possibleColumnsToGoRight = 7 - cj
			# print("possibleRowsToGoUp", possibleRowsToGoUp)
			# print("possibleRowsToGoDown", possibleRowsToGoDown)
			# print("possibleColumnsToGoLeft", possibleColumnsToGoLeft)
			# print("possibleColumnsToGoRight", possibleColumnsToGoRight)
			# print("curPos", curPos)
			# print("newPos", newPos)
			# print("rangeI", xx, "->", xx)
			# print("rangeJ", xx, "->", xx)

			# Diagonal left up
			rowsDone = []
			columnsDone = []
			temp = []
			for i in range(possibleRowsToGoUp, -1, -1):
				for j in range(possibleColumnsToGoLeft, -1, -1):
					if possibleRowsToGoUp - possibleColumnsToGoLeft <= i < possibleRowsToGoUp and \
						j < possibleColumnsToGoLeft and \
						i not in rowsDone and \
						j not in columnsDone:
							temp.append((i, j))
							rowsDone.append(i)
							columnsDone.append(j)
			# print("temp1",temp)
			for move in temp:
				r, c = move
				if isinstance(board[r][c], NoType):
					path.append((r,c))
				else:
					break
			# print("path1",path)

			# Diagonal right up
			rowsDone = []
			columnsDone = []
			temp = []
			# print("rangeI", possibleRowsToGoUp, "->", 0)
			# print("rangeJ", cj + 1, "->",8)
			for i in range(possibleRowsToGoUp, 0, -1):
				for j in range(cj + 1, 8):
					# print(possibleRowsToGoUp - possibleColumnsToGoRight, " <= ", i, " < ", possibleRowsToGoUp, " and ", cj, " <= ", j, " <= ", cj + possibleColumnsToGoRight, rowsDone, columnsDone)
					# if ci < i <= possibleRowsToGoDown and \
					# 	j < possibleColumnsToGoLeft and \
					if possibleRowsToGoUp - possibleColumnsToGoRight <= i < possibleRowsToGoUp and \
						cj <= j <= cj + possibleColumnsToGoRight and \
						i not in rowsDone and \
						j not in columnsDone:
							temp.append((i, j))
							rowsDone.append(i)
							columnsDone.append(j)
			# print("temp2",temp)
			for move in temp:
				r, c = move
				if isinstance(board[r][c], NoType):
					path.append((r,c))
				else:
					break
			# print("path2",path)

			# Diagonal left down
			rowsDone = []
			columnsDone = []
			temp = []
			for i in range(ci, 8):
				for j in range(cj - 1, -1, -1):
					if ci < i <= possibleRowsToGoDown and \
						j < possibleColumnsToGoLeft and \
						i not in rowsDone and \
						j not in columnsDone:
							temp.append((i, j))
							rowsDone.append(i)
							columnsDone.append(j)
			# print("temp3",temp)
			for move in temp:
				r, c = move
				if isinstance(board[r][c], NoType):
					path.append((r,c))
				else:
					break
			# print("path3",path)

			# Diagonal right down
			rowsDone = []
			columnsDone = []
			temp = []
			for i in range(ci, 8):
				for j in range(cj, 8):
					if ci < i < 8 and \
						cj < j < 8 and \
						i not in rowsDone and \
						j not in columnsDone:
							temp.append((i, j))
							rowsDone.append(i)
							columnsDone.append(j)
			# print("temp4",temp)
			for move in temp:
				r, c = move
				if isinstance(board[r][c], NoType):
					path.append((r,c))
				else:
					break
			# print("path4",path)

		return list(set(path))

	def takeableMoves(self, curPos, newPos, board):
		takeableMoves = []
		temp = self.getLegalMovesAndNotBlockedInPath(curPos, newPos, board)
		for move in temp:
			r, c = move
			# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
			# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))
				else:
					# print("############ JA")
					break
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
		# print("possibleMoves1", possibleMoves)
		possibleMoves.append(Bishop(self.color()).possibleMoves(r,c))
		# print("possibleMoves2", possibleMoves)
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
			# print("(r,c)",(r,c),"(ci,cj)",(ci,cj),"(ni,nj)",(ni,nj))
			# print("not ", isinstance(board[r][c], NoType), " and ", board[r][c].color(), " != ", board[ci][cj].color())
			if not isinstance(board[r][c], NoType):
				if board[r][c].color() != board[ci][cj].color():
					takeableMoves.append((r,c))
				else:
					# print("############ JA")
					break
		return list(set(takeableMoves))