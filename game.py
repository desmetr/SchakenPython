from chesspiece import *
import numpy as np
from tkinter import messagebox
import tkinter as tk

class Game:
	def __init__(self, root):
		self.board = [[NoType(pieceColor.White)] * 8 for i in range(8)]
		self.time = 0
		self.root = root

		self.blackPiecesInGame = []
		self.takenBlackPieces = []
		self.whitePiecesInGame = []
		self.takenWhitePieces = []

		self.pawnToPromote = None
		self.check = False
		self.checkmate = False
		self.colorInCheckmate = None

	def setPawnBoard(self):
		P1B = Pawn(pieceColor.Black)
		# P2B = Pawn(pieceColor.Black)
		# P3B = Pawn(pieceColor.Black)
		# P4B = Pawn(pieceColor.Black)
		# P5B = Pawn(pieceColor.Black)
		# P6B = Pawn(pieceColor.Black)
		# P7B = Pawn(pieceColor.Black)
		# P8B = Pawn(pieceColor.Black)
		self.board[6][0] = P1B
		# self.board[1][1] = P2B
		# self.board[1][2] = P3B
		# self.board[1][3] = P4B
		# self.board[1][4] = P5B
		# self.board[1][5] = P6B
		# self.board[1][6] = P7B
		# self.board[1][7] = P8B
		# self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B])
		self.blackPiecesInGame.extend([P1B])

		P1W = Pawn(pieceColor.White)
		# P2W = Pawn(pieceColor.White)
		# P3W = Pawn(pieceColor.White)
		# P4W = Pawn(pieceColor.White)
		# P5W = Pawn(pieceColor.White)
		# P6W = Pawn(pieceColor.White)
		# P8W = Pawn(pieceColor.White)
		# P7W = Pawn(pieceColor.White)
		self.board[1][0] = P1W
		# self.board[6][1] = P2W
		# self.board[6][2] = P3W
		# self.board[6][3] = P4W
		# self.board[6][4] = P5W
		# self.board[6][5] = P6W
		# self.board[6][6] = P7W
		# self.board[6][7] = P8W
		# self.whitePiecesInGame.extend([P8W, P1W, P2W, P3W, P4W, P5W, P6W, P7W])
		self.whitePiecesInGame.extend([P1W])

		self.printStatus(None,None,None,True)
	
	def setRookBoard(self):
		R1B = Rook(pieceColor.Black)
		R2B = Rook(pieceColor.Black)
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		self.board[0][7] = R1B
		# self.board[7][7] = R2B
		self.board[0][3] = P1B
		self.board[4][0] = P2B
		self.board[5][3] = P3B
		self.blackPiecesInGame.extend([R1B,P1B,P2B,P3B])
		R1W = Rook(pieceColor.White)
		R2W = Rook(pieceColor.White)
		P1W = Pawn(pieceColor.White)
		self.board[4][3] = R1W
		self.board[7][7] = R2W
		self.board[4][6] = P1W
		self.whitePiecesInGame.extend([R1W,R2W,P1W])
		self.printStatus(None,None,None,True)

	def setKnightBoard(self):
		Kn1B = Knight(pieceColor.Black)
		# Kn2B = Knight(pieceColor.Black)
		# P1B = Pawn(pieceColor.Black)
		# P2B = Pawn(pieceColor.Black)
		# P3B = Pawn(pieceColor.Black)
		# P4B = Pawn(pieceColor.Black)
		# P5B = Pawn(pieceColor.Black)
		# P6B = Pawn(pieceColor.Black)
		# P7B = Pawn(pieceColor.Black)
		# P8B = Pawn(pieceColor.Black)
		self.board[4][4] = Kn1B
		# self.board[0][6] = Kn2B
		# self.board[5][0] = P1B
		# self.board[1][1] = P2B
		# self.board[1][2] = P3B
		# self.board[1][3] = P4B
		# self.board[1][4] = P5B
		# self.board[1][5] = P6B
		# self.board[1][6] = P7B
		# self.board[5][7] = P8B
		# self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B, Kn1B, Kn2B])
		self.blackPiecesInGame.extend([Kn1B])

		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		# Kn1W = Knight(pieceColor.White)
		# Kn2W = Knight(pieceColor.White)
		self.board[6][0] = P1W
		self.board[6][1] = P2W
		self.board[2][2] = P3W
		self.board[6][3] = P4W
		self.board[6][4] = P5W
		self.board[6][5] = P6W
		self.board[6][6] = P7W
		self.board[2][7] = P8W
		# self.board[7][1] = Kn1W
		# self.board[7][6] = Kn2W
		self.whitePiecesInGame.extend([P1W, P2W, P3W, P4W, P5W, P6W, P7W, P8W])
	
		self.printStatus(None,None,None,True)

	def setBishopBoard(self):
		B1B = Bishop(pieceColor.Black)
		B2B = Bishop(pieceColor.Black)
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		P5B = Pawn(pieceColor.Black)
		P6B = Pawn(pieceColor.Black)
		P7B = Pawn(pieceColor.Black)
		P8B = Pawn(pieceColor.Black)
		# self.board[2][2] = P1B
		# self.board[2][3] = P2B
		# self.board[2][4] = P3B
		# self.board[2][5] = P4B
		# self.board[4][2] = P5B
		# self.board[4][3] = P6B
		# self.board[4][4] = P7B
		# self.board[4][5] = P8B
		self.board[3][3] = B1B
		self.board[3][4] = B2B
		# self.blackPiecesInGame.extend([P1B,P2B,P3B,P4B,P5B,P6B,P7B,P8B,B1B,B2B])
		self.blackPiecesInGame.extend([B1B,B2B])
		# self.blackPiecesInGame.extend([P1B,P2B,B1B,B2B])

		B1W = Bishop(pieceColor.White)
		B2W = Bishop(pieceColor.White)
		# self.board[7][2] = B1W
		# self.board[7][7] = B2W
		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		self.board[0][0] = P1W
		self.board[0][1] = P2W
		self.board[0][6] = P3W
		self.board[0][7] = P4W
		self.board[6][0] = P5W
		self.board[6][1] = P6W
		self.board[6][6] = P7W
		self.board[6][7] = P8W
		self.whitePiecesInGame.extend([P1W,P2W,P3W,P4W,P5W,P6W,P7W,P8W])
		# self.whitePiecesInGame.extend([B1W,B2W,P1W,P2W,P3W,P4W])

		self.printStatus(None,None,None,True)

	def setQueenBoard(self):
		QB = Queen(pieceColor.Black)
		self.board[4][0] = QB
		self.blackPiecesInGame.extend([QB])
		QW = Queen(pieceColor.White)
		self.board[7][3] = QW
		self.whitePiecesInGame.extend([QW])
		self.printStatus(None,None,None,True)

	def setKingBoard(self):
		KB = King(pieceColor.Black)
		self.board[1][4] = KB
		self.blackPiecesInGame.extend([KB])
		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		self.board[0][3] = P1W
		self.board[0][4] = P2W
		self.board[0][5] = P3W
		self.board[1][3] = P4W
		self.board[1][5] = P5W
		self.board[2][3] = P6W
		self.board[2][4] = P7W
		self.board[2][5] = P8W
		self.whitePiecesInGame.extend([P8W, P1W, P2W, P3W, P4W, P5W, P6W, P7W])
		self.printStatus(None,None,None,True)

	def setCheckBoard(self):
		KB = King(pieceColor.Black)
		self.board[0][4] = KB
		self.blackPiecesInGame.extend([KB])

		QW = Queen(pieceColor.White)
		RW = Rook(pieceColor.White)
		self.board[5][5] = QW
		self.whitePiecesInGame.extend([QW])

		self.printStatus(None,None,None,True)

	def setCheckmateBoard(self):
		KB = King(pieceColor.Black)
		self.board[0][4] = KB
		self.blackPiecesInGame.extend([KB])

		Kn1W = Knight(pieceColor.White)
		QW = Queen(pieceColor.White)
		self.board[3][5] = Kn1W
		self.board[1][4] = QW
		self.whitePiecesInGame.extend([QW,Kn1W])

		self.printStatus(None,None,None,True)

	def setStartBoard(self):
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		P5B = Pawn(pieceColor.Black)
		P6B = Pawn(pieceColor.Black)
		P7B = Pawn(pieceColor.Black)
		P8B = Pawn(pieceColor.Black)
		R1B = Rook(pieceColor.Black)
		R2B = Rook(pieceColor.Black)
		Kn1B = Knight(pieceColor.Black)
		Kn2B = Knight(pieceColor.Black)
		B1B = Bishop(pieceColor.Black)
		B2B = Bishop(pieceColor.Black)
		QB = Queen(pieceColor.Black)
		KB = King(pieceColor.Black)
		self.board[1][0] = P1B
		self.board[1][1] = P2B
		self.board[1][2] = P3B
		self.board[1][3] = P4B
		self.board[1][4] = P5B
		self.board[1][5] = P6B
		self.board[1][6] = P7B
		self.board[1][7] = P8B
		self.board[0][0] = R1B
		self.board[0][7] = R2B
		self.board[0][1] = Kn1B
		self.board[0][6] = Kn2B
		self.board[0][2] = B1B
		self.board[0][5] = B2B
		self.board[0][3] = QB
		self.board[0][4] = KB
		self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B, R1B, R2B, Kn1B, Kn2B, B1B, B2B, QB, KB])

		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		R1W = Rook(pieceColor.White)
		R2W = Rook(pieceColor.White)
		Kn1W = Knight(pieceColor.White)
		Kn2W = Knight(pieceColor.White)
		B1W = Bishop(pieceColor.White)
		B2W = Bishop(pieceColor.White)
		QW = Queen(pieceColor.White)
		KW = King(pieceColor.White)
		self.board[6][0] = P1W
		self.board[6][1] = P2W
		self.board[6][2] = P3W
		self.board[6][3] = P4W
		self.board[6][4] = P5W
		self.board[6][5] = P6W
		self.board[6][6] = P7W
		self.board[6][7] = P8W
		self.board[7][0] = R1W
		self.board[7][7] = R2W
		self.board[7][1] = Kn1W
		self.board[7][6] = Kn2W
		self.board[7][2] = B1W
		self.board[7][5] = B2W
		self.board[7][3] = QW
		self.board[7][4] = KW
		self.whitePiecesInGame.extend([P1W, P2W, P3W, P4W, P5W, P6W, P7W, P8W, R1W, R2W, Kn1W, Kn2W, B1W, B2W, QW, KW])

		self.printStatus(None,None,None,True)
		# self.isCheck()

	def getPieceOnPosition(self, pos):
		r, c = pos
		return self.board[r][c]
	
	def getCurrentPosOfPiece(self, piece):
		r = c = -1
		for i in range(0,8):
			for j in range(0,8):
				if self.board[i][j] == piece:
					r = i
					c = j
		return (r,c)

	def getCurrentPosOfPieceDuringCheckmate(self, piece, board):
		r = c = -1
		for i in range(0,8):
			for j in range(0,8):
				if board[i][j] == piece:
					r = i
					c = j
		return (r,c)

	def legalMoves(self, piece, newPos):
		ci, cj = self.getCurrentPosOfPiece(piece)

		possibleMoves = piece.possibleMoves(ci, cj)

		legalMoves = []
		for move in possibleMoves:
			r, c = move
			if isinstance(self.board[r][c], NoType):
				legalMoves.append(move)

		legalMovesAndNotBlocked = legalMoves

		if newPos in legalMoves:
			legalMovesAndNotBlocked = piece.legalMovesAndNotBlockedInPath((ci, cj), newPos, self.board)

		return legalMovesAndNotBlocked

	def legalMovesDuringCheckmate(self, piece, newPos, board):
		ci, cj = self.getCurrentPosOfPieceDuringCheckmate(piece, board)

		possibleMoves = piece.possibleMoves(ci, cj)

		legalMoves = []
		for move in possibleMoves:
			r, c = move
			if isinstance(board[r][c], NoType):
				legalMoves.append(move)

		legalMovesAndNotBlocked = legalMoves

		if newPos in legalMoves:
			legalMovesAndNotBlocked = piece.legalMovesAndNotBlockedInPath((ci, cj), newPos, board)

		return legalMovesAndNotBlocked

	def move(self, piece, newPos):
		i, j = self.getCurrentPosOfPiece(piece)
		r, c = newPos

		if piece.color() != pieceColor.White and self.time == 0:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED. WHITE HAS TO START.\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed. White has to start.")

			return False

		legalMoves = self.legalMoves(piece, newPos)
		takeableMoves = piece.takeableMoves((i,j), (r,c), self.board)
		piece.firstMove = False

		# Check if piece can take another piece on newPos
		if not isinstance(self.board[r][c], NoType) and newPos in takeableMoves and self.board[r][c].color() != self.board[i][j].color():
			print("> You can take piece ", self.board[r][c], " on position", newPos, "!")
			oldPiece = self.board[r][c]
			if oldPiece.color() == pieceColor.Black: 
				self.blackPiecesInGame.remove(oldPiece)
				self.takenBlackPieces.append(oldPiece)
			if oldPiece.color() == pieceColor.White: 
				self.whitePiecesInGame.remove(oldPiece)
				self.takenWhitePieces.append(oldPiece)
			
			self.board[i][j] = NoType(pieceColor.White)
			self.board[r][c] = piece

			self.time += 1
			self.printStatus(piece, (i,j), (r,c))
			return True

		# If not, check if piece can move to newPos and act accordingly
		if (r,c) in legalMoves:
			oldPiece = self.board[i][j]
			self.board[i][j] = NoType(pieceColor.White)
			self.board[r][c] = piece

			# if isinstance(piece, Pawn) and piece.canPromote(r, c):
			# 	self.pawnToPromote = piece
			# 	self.promoteWindow()
			# 	self.root.wait_window(self.win)
			# 	self.promotePawn()
			# 	print("AA")
			# print("BB")
			self.time += 1
			self.printStatus(piece, (i,j), (r,c))
			return True
		else:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed.")

			return False

	def moveDuringCheckmate(self, piece, newPos):
		print(newPos)
		tempBoard = self.board
		i, j = self.getCurrentPosOfPieceDuringCheckmate(piece, tempBoard)
		r, c = newPos

		legalMoves = self.legalMovesDuringCheckmate(piece, newPos, tempBoard)
		takeableMoves = piece.takeableMoves((i,j), (r,c), tempBoard)
		piece.firstMove = False
		# Check if piece can take another piece on newPos
		if not isinstance(tempBoard[r][c], NoType) and newPos in takeableMoves and tempBoard[r][c].color() != tempBoard[i][j].color():
			oldPiece = tempBoard[r][c]
			tempBoard[i][j] = NoType(pieceColor.White)
			tempBoard[r][c] = piece
			
		# If not, check if piece can move to newPos and act accordingly
		if (r,c) in legalMoves:
			oldPiece = tempBoard[i][j]
			tempBoard[i][j] = NoType(pieceColor.White)
			tempBoard[r][c] = piece
		print("###",self.getCurrentPosOfPiece(piece))

		result = ""
		color = ""
		for i in range(0, 8):
			for j in range(0, 8):
				color = "_W" if tempBoard[i][j].color() == pieceColor.White else "_B"
				selected = "_T" if tempBoard[i][j].selected else "_F"
				if isinstance(tempBoard[i][j], Pawn):
					result += "P" + color + "  "
				elif isinstance(tempBoard[i][j], Rook):
					result += "R" + color + "  "
				elif isinstance(tempBoard[i][j], Knight):
					result += "KN" + color + " "
				elif isinstance(tempBoard[i][j], Bishop):
					result += "B" + color + "  "
				elif isinstance(tempBoard[i][j], Queen):
					result += "Q" + color + "  "
				elif isinstance(tempBoard[i][j], King):
					result += "K" + color + "  "
				else:
					result += "x    "
			result += "\n"
		print(result)

		print("##",self.getCurrentPosOfPiece(piece))

		return tempBoard

	def promoteWindow(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Promote")

		l = tk.Label(self.win, text="Choose piece to promote to:")
		l.grid(row=0, column=0)

		bQueen = tk.Button(self.win, text="Queen", command=self.promoteCallback("Queen"))
		# bQueen = tk.Button(self.win, text="Queen", command=self.promoteToQueen)
		bQueen.grid(row=0, column=1)

		bRook = tk.Button(self.win, text="Rook", command=self.promoteCallback("Rook"))
		# bRook = tk.Button(self.win, text="Rook", command=self.promoteToRook)
		bRook.grid(row=0, column=2)

		bBishop = tk.Button(self.win, text="Bishop", command=self.promoteCallback("Bishop"))
		# bBishop = tk.Button(self.win, text="Bishop", command=self.promoteToBishop)
		bBishop.grid(row=0, column=3)

		bKnight = tk.Button(self.win, text="Knight", command=self.promoteCallback("Knight"))
		# bKnight = tk.Button(self.win, text="Knight", command=self.promoteToKnight)
		bKnight.grid(row=0, column=4)

	def promoteCallback(self, promotedPiece):
		self.promotedPiece = promotedPiece

	def promotePawn(self):
		newPiece = None
		r, c = self.getCurrentPosOfPiece(self.pawnToPromote)
		newColor = self.pawnToPromote.color()

		if self.pawnToPromote and newColor == pieceColor.Black:
			self.blackPiecesInGame.remove(self.pawnToPromote)
		elif self.pawnToPromote and newColor == pieceColor.White:
			self.whitePiecesInGame.remove(self.pawnToPromote)
		if self.promotedPiece == "Queen": 	newPiece = Queen(newColor)
		if self.promotedPiece == "Rook":	newPiece = Rook(newColor)
		if self.promotedPiece == "Bishop":	newPiece = Bishop(newColor)
		if self.promotedPiece == "Knight":	newPiece = Knight(newColor)

		self.board[r][c] = newPiece

		print("> BOARD AT TIME ", self.time, ": PROMOTED " + str(self.pawnToPromote) + " ON ", (r,c), " TO A", newPiece, "\n")
		self.pawnToPromote = None


	# def promoteToQueen(self):
	# 	newQueen = None
	# 	r, c = self.getCurrentPosOfPiece(self.pawnToPromote)

	# 	if self.pawnToPromote.color() == pieceColor.Black:
	# 		if self.pawnToPromote:
	# 			self.blackPiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newQueen = Queen(pieceColor.Black)
	# 		self.blackPiecesInGame.append(newQueen)
	# 	elif self.pawnToPromote.color() == pieceColor.White:
	# 		if self.pawnToPromote:
	# 			self.whitePiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newQueen = Queen(pieceColor.White)
	# 		self.whitePiecesInGame.append(newQueen)
		
	# 	self.board[r][c] = newQueen
	# 	self.win.destroy()

	# def promoteToRook(self):
	# 	newRook = None
	# 	r, c = self.getCurrentPosOfPiece(self.pawnToPromote)

	# 	if self.pawnToPromote.color() == pieceColor.Black:
	# 		if self.pawnToPromote:
	# 			self.blackPiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newRook = Rook(pieceColor.Black)
	# 		self.blackPiecesInGame.append(newRook)
	# 	elif self.pawnToPromote.color() == pieceColor.White:
	# 		if self.pawnToPromote:
	# 			self.whitePiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newRook = Rook(pieceColor.White)
	# 		self.whitePiecesInGame.append(newRook)

	# 	self.board[r][c] = newRook
	# 	self.win.destroy()

	# def promoteToBishop(self):
	# 	newBishop = None
	# 	r, c = self.getCurrentPosOfPiece(self.pawnToPromote)
	
	# 	if self.pawnToPromote.color() == pieceColor.Black:
	# 		if self.pawnToPromote:
	# 			self.blackPiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newBishop = Bishop(pieceColor.Black)
	# 		self.blackPiecesInGame.append(newBishop)
	# 	elif self.pawnToPromote.color() == pieceColor.White:
	# 		if self.pawnToPromote:
	# 			self.whitePiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newBishop = Bishop(pieceColor.White)
	# 		self.whitePiecesInGame.append(newBishop)

	# 	self.board[r][c] = newBishop
	# 	self.win.destroy()
	
	# def promoteToKnight(self):
	# 	newKnight = None
	# 	r, c = self.getCurrentPosOfPiece(self.pawnToPromote)
	
	# 	if self.pawnToPromote.color() == pieceColor.Black:
	# 		if self.pawnToPromote:
	# 			self.blackPiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newKnight = Knight(pieceColor.Black)
	# 		self.blackPiecesInGame.append(newKnight)
	# 	elif self.pawnToPromote.color() == pieceColor.White:
	# 		if self.pawnToPromote:
	# 			self.whitePiecesInGame.remove(self.pawnToPromote)
	# 			self.pawnToPromote = None
	# 		newKnight = Knight(pieceColor.White)
	# 		self.whitePiecesInGame.append(newKnight)

	# 	self.board[r][c] = newKnight
	# 	self.win.destroy()
	
	def findAllTakeableBlackPieces(self):
		takeableBlackPieces = []
		for blackPiece in self.blackPiecesInGame:
			(bi,bj) = self.getCurrentPosOfPiece(blackPiece)
			for whitePiece in self.whitePiecesInGame:
				(wi,wj) = self.getCurrentPosOfPiece(whitePiece)
				if (bi,bj) in whitePiece.takeableMoves((wi,wj), (bi,bj), self.board):
					takeableBlackPieces.append((blackPiece, (bi,bj)))
		return takeableBlackPieces

	def findAllTakeableWhitePieces(self):
		takeableWhitePieces = []
		for whitePiece in self.whitePiecesInGame:
			(wi,wj) = self.getCurrentPosOfPiece(whitePiece)
			for blackPiece in self.blackPiecesInGame:
				(bi,bj) = self.getCurrentPosOfPiece(blackPiece)
				takeableMoves = blackPiece.takeableMoves((bi,bj), (wi,wj), self.board)
				if (wi,wj) in takeableMoves:
					takeableWhitePieces.append((whitePiece, (wi,wj)))
		return takeableWhitePieces

	def isCheck(self, verbose=True):
		blackIsCheck = self.isCheckBlack()
		whiteIsCheck = self.isCheckWhite()
		print("> BOARD AT TIME ", self.time, ": BLACK IS", "" if blackIsCheck else " NOT ", "IN CHECK.")
		print("------------------------------------")
		print("> BOARD AT TIME ", self.time, ": WHITE IS", "" if whiteIsCheck else " NOT ", "IN CHECK.")
		print("------------------------------------")
		return (blackIsCheck, whiteIsCheck)

	def isCheckBlack(self, board=None):
		if not board: 
			board = self.board

		blackKing = None
		for piece in self.blackPiecesInGame:
			if isinstance(piece, King):
				blackKing = piece
		posBlackKing = self.getCurrentPosOfPiece(blackKing) if not board else self.getCurrentPosOfPieceDuringCheckmate(blackKing, board)
		for whitePiece in self.whitePiecesInGame:
			posWhitePiece = self.getCurrentPosOfPiece(whitePiece) if not board else self.getCurrentPosOfPieceDuringCheckmate(whitePiece, board)
			takeableMoves = whitePiece.takeableMoves(posWhitePiece, None, board)
			if posBlackKing in takeableMoves:
				return True
		return False
					
	def isCheckWhite(self, board=None):
		if not board: 
			board = self.board
		
		whiteKing = None
		for piece in self.whitePiecesInGame:
			if isinstance(piece, King):
				whiteKing = piece
		posWhiteKing = self.getCurrentPosOfPiece(whiteKing) if not board else self.getCurrentPosOfPieceDuringCheckmate(whiteKing, board)
		for blackPiece in self.whitePiecesInGame:
			posBlackPiece = self.getCurrentPosOfPiece(blackPiece) if not board else self.getCurrentPosOfPieceDuringCheckmate(blackPiece, board)
			takeableMoves = blackPiece.takeableMoves(posBlackPiece, None, board)
			if posWhiteKing in takeableMoves:
				return True
		return False
					
	def isCheckmate(self):
		blackIsCheckmate = self.isCheckmateBlack()
		whiteIsCheckmate = self.isCheckmateWhite()
		print("> BOARD AT TIME ", self.time, ": BLACK IS", "" if blackIsCheckmate else " NOT ", "IN CHECKMATE.")
		print("------------------------------------")
		print("> BOARD AT TIME ", self.time, ": WHITE IS", "" if whiteIsCheckmate else " NOT ", "IN CHECKMATE.")
		print("------------------------------------")
		return (blackIsCheckmate, whiteIsCheckmate)

	def isCheckmateBlack(self):
		if self.isCheckBlack():
			blackKing = None
			for piece in self.blackPiecesInGame:
				if isinstance(piece, King):
					blackKing = piece
			r, c = self.getCurrentPosOfPiece(blackKing)
			possibleMovesKing = blackKing.possibleMoves(r, c)
			originalBoard = self.board
			possibleBoards = []
			for move in possibleMovesKing:
				print("#",self.getCurrentPosOfPiece(blackKing))
				possibleBoards.append(self.moveDuringCheckmate(blackKing, move))
			print("----")
			movesCanSolve = []
			for board in possibleBoards:
				movesCanSolve.append(self.isCheckBlack(board))
			self.printBoard()
			print(movesCanSolve)
			if any(move for move in movesCanSolve):
				return True
		return False

	def isCheckmateWhite(self):
		if self.isCheckWhite():

			return True
		return False

	def pat(self, color):
		return False

	def handleEndGame(self):
		print(">", self.colorInCheckmate.name.upper(), "IS IN CHECKMATE, END GAME.")
		messagebox.showinfo("Checkmate", "Board at time " + str(self.time) + ": " + self.colorInCheckmate.name.upper() + " is checkmate! End of game!")
		self.root.quit()
		self.checkmate = False
		self.check = False
		self.colorInCheckmate = None

	def printBoard(self):
		result = ""
		color = ""
		for i in range(0, 8):
			for j in range(0, 8):
				color = "_W" if self.board[i][j].color() == pieceColor.White else "_B"
				selected = "_T" if self.board[i][j].selected else "_F"
				if isinstance(self.board[i][j], Pawn):
					result += "P" + color + "  "
				elif isinstance(self.board[i][j], Rook):
					result += "R" + color + "  "
				elif isinstance(self.board[i][j], Knight):
					result += "KN" + color + " "
				elif isinstance(self.board[i][j], Bishop):
					result += "B" + color + "  "
				elif isinstance(self.board[i][j], Queen):
					result += "Q" + color + "  "
				elif isinstance(self.board[i][j], King):
					result += "K" + color + "  "
				else:
					result += "x    "
			result += "\n"
		print(result)
		print("> BLACK PIECES STILL IN THE GAME:")
		print(self.blackPiecesInGame)
		print("> WHITE PIECES STILL IN THE GAME:")
		print(self.whitePiecesInGame)
		print("\n")

	def printStatus(self, piece, curPos, newPos, setup=False):
		if setup:
			print("> BOARD AT TIME ", self.time, ": SET UP NEW GAME")
			print("------------------------------------")	
			self.printBoard()
		else:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", curPos, " TO ", newPos)
			print("--------------------------------------------------------------")
			self.printBoard()
			# print("> BLACK PIECES IN DANGER:", self.findAllTakeableBlackPieces())
			# print("> WHITE PIECES IN DANGER:", self.findAllTakeableWhitePieces())
		self.isCheck()
		self.isCheckmate()