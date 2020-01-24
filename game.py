from chesspiece import *
import numpy as np
from tkinter import messagebox
import tkinter as tk
import copy
from collections import deque

class Game:
	def __init__(self, root):
		self.board = [[NoType(pieceColor.NoColor)] * 8 for i in range(8)]
		self.time = 0
		self.root = root

		self.stackOfMoves = deque()
		self.stackOfMovesUndone = deque()
		
		self.blackPiecesInGame = []
		self.takenBlackPieces = []
		self.whitePiecesInGame = []
		self.takenWhitePieces = []

		self.pawnToPromote = None
		self.check = False
		self.checkmate = False
		self.colorInCheckmate = None

		self.blackLongRokadePossible = False
		self.blackShortRokadePossible = False
		self.whiteLongRokadePossible = False
		self.whiteShortRokadePossible = False

	def copyData(self, otherGame):
		for i in range(0,8):
			for j in range(0,8):
				self.board[i][j] = otherGame.board[i][j]
		self.time = otherGame.time

		self.blackPiecesInGame = otherGame.blackPiecesInGame
		self.takenBlackPieces = otherGame.takenBlackPieces
		self.whitePiecesInGame = otherGame.whitePiecesInGame
		self.takenWhitePieces = otherGame.takenWhitePieces

		self.pawnToPromote = otherGame.pawnToPromote
		self.check = otherGame.check
		self.checkmate = otherGame.checkmate
		self.colorInCheckmate = otherGame.colorInCheckmate

		self.blackLongRokadePossible = otherGame.blackLongRokadePossible
		self.blackShortRokadePossible = otherGame.blackShortRokadePossible
		self.whiteLongRokadePossible = otherGame.whiteLongRokadePossible
		self.whiteShortRokadePossible = otherGame.whiteShortRokadePossible

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

	def setRokadeBoard(self):
		KB = King(pieceColor.Black)
		R1B = Rook(pieceColor.Black)
		R2B = Rook(pieceColor.Black)
		B1B = Bishop(pieceColor.Black)
		self.board[0][4] = KB
		self.board[0][0] = R1B
		self.board[0][7] = R2B
		# self.board[0][1] = B1B
		self.blackPiecesInGame.extend([KB, R1B, R2B])

		KW = King(pieceColor.White)
		R1W = Rook(pieceColor.White)
		R2W = Rook(pieceColor.White)
		self.board[7][4] = KW
		self.board[7][0] = R1W
		self.board[7][7] = R2W
		self.whitePiecesInGame.extend([KW, R1W, R2W])
		self.printStatus(None,None,None,True)

	def setPromoteBoard(self):
		P1W = Pawn(pieceColor.White)
		self.board[1][3] = P1W
		self.whitePiecesInGame.extend([P1W])
		self.printStatus(None,None,None,True)

	def setCheckBoard(self):
		KB = King(pieceColor.Black)
		KnB = Knight(pieceColor.Black)
		self.board[0][4] = KB
		self.board[3][3] = KnB
		self.blackPiecesInGame.extend([KB, KnB])

		QW = Queen(pieceColor.White)
		KW = King(pieceColor.White)
		self.board[5][3] = KW		
		self.board[5][5] = QW
		self.whitePiecesInGame.extend([QW, KW])

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

	def setEnPassantBoard(self):
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		P5B = Pawn(pieceColor.Black)
		P6B = Pawn(pieceColor.Black)
		P7B = Pawn(pieceColor.Black)
		P8B = Pawn(pieceColor.Black)
		KB = King(pieceColor.Black)
		self.board[1][0] = P1B
		self.board[1][1] = P2B
		self.board[2][2] = P3B
		self.board[4][3] = P4B
		self.board[1][4] = P5B
		self.board[1][5] = P6B
		self.board[1][6] = P7B
		self.board[4][7] = P8B
		self.board[0][4] = KB
		self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B, KB])

		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		KW = King(pieceColor.White)
		self.board[3][0] = P1W
		self.board[5][1] = P2W
		self.board[6][2] = P3W
		self.board[6][3] = P4W
		self.board[6][4] = P5W
		self.board[3][5] = P6W
		self.board[6][6] = P7W
		self.board[6][7] = P8W
		self.board[7][4] = KW

		self.whitePiecesInGame.extend([P1W, P2W, P3W, P4W, P5W, P6W, P7W, P8W, KW])

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

	def getBlackKingPosition(self):
		blackKing = None
		for piece in self.blackPiecesInGame:
			if isinstance(piece, King):
				blackKing = piece
		return self.getCurrentPosOfPiece(blackKing)

	def getBlackKing(self):
		blackKing = None
		for piece in self.blackPiecesInGame:
			if isinstance(piece, King):
				blackKing = piece
		return blackKing

	def getWhiteKingPosition(self):
		whiteKing = None
		for piece in self.whitePiecesInGame:
			if isinstance(piece, King):
				whiteKing = piece
		return self.getCurrentPosOfPiece(whiteKing)

	def getWhiteKing(self):
		whiteKing = None
		for piece in self.whitePiecesInGame:
			if isinstance(piece, King):
				whiteKing = piece
		return whiteKing

	def undo(self):
		if len(self.stackOfMoves) == 0:
			messagebox.showinfo("No moves to undo", "Board at time " + str(self.time) + ": There are no moves to undo.")
			return
		moveToUndo = self.stackOfMoves.pop()
		piece = moveToUndo[0]
		(i,j) = moveToUndo[1]
		(r,c) = moveToUndo[2]
		takenPiece = moveToUndo[3]
		self.board[i][j] = piece
		self.board[r][c] = takenPiece # If nothing was taken during move, this is NoType

		if not isinstance(takenPiece, NoType):
			if takenPiece.color() == pieceColor.Black: 
				self.blackPiecesInGame.append(takenPiece)
				self.takenBlackPieces.remove(takenPiece)
			if takenPiece.color() == pieceColor.White: 
				self.whitePiecesInGame.append(takenPiece)
				self.takenWhitePieces.remove(takenPiece)

		self.printStatus(piece, (r,c), (i,j))
		self.stackOfMovesUndone.append(moveToUndo)

	def redo(self):
		if len(self.stackOfMovesUndone) == 0:
			messagebox.showinfo("No moves to redo", "Board at time " + str(self.time) + ": There are no moves to redo.")
			return
		moveToRedo = self.stackOfMovesUndone.pop()
		piece = moveToRedo[0]
		(i,j) = moveToRedo[1]
		(r,c) = moveToRedo[2]
		takenPiece = moveToRedo[3]
		self.board[i][j] = takenPiece # If nothing was taken during move, this is NoType
		self.board[r][c] = piece 

		if not isinstance(takenPiece, NoType):
			if takenPiece.color() == pieceColor.Black: 
				self.blackPiecesInGame.remove(takenPiece)
				self.takenBlackPieces.append(takenPiece)
			if takenPiece.color() == pieceColor.White: 
				self.whitePiecesInGame.remove(takenPiece)
				self.takenWhitePieces.append(takenPiece)
		
		self.printStatus(piece, (i,j), (r,c))
		self.stackOfMoves.append(moveToRedo)

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

	def move(self, piece, newPos):
		i, j = self.getCurrentPosOfPiece(piece)
		r, c = newPos
		pieceOnNewPos = self.getPieceOnPosition(newPos)

		if piece.color() != pieceColor.White and self.time == 0:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED. WHITE HAS TO START.\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed. White has to start.")

			return False

		legalMoves = self.legalMoves(piece, newPos)
		takeableMoves = piece.takeableMoves((i,j), (r,c), self.board)

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
			
			self.board[i][j] = NoType(pieceColor.NoColor)
			self.board[r][c] = piece

			self.stackOfMoves.append((piece, (i,j), (r,c), oldPiece))
			self.time += 1
			self.printStatus(piece, (i,j), (r,c))
			return True

		# Handle rokade
		if isinstance(piece, King) and isinstance(pieceOnNewPos, Rook):
			if self.blackLongRokadePossible and (r,c) == (0,0):
				self.board[0][4] = NoType(pieceColor.NoColor)
				self.board[0][0] = NoType(pieceColor.NoColor)
				self.board[0][2] = piece
				self.board[0][3] = pieceOnNewPos
			elif self.blackShortRokadePossible and (r,c) == (0,7):
				self.board[0][4] = NoType(pieceColor.NoColor)
				self.board[0][7] = NoType(pieceColor.NoColor)
				self.board[0][5] = pieceOnNewPos
				self.board[0][6] = piece
			elif self.whiteLongRokadePossible and (r,c) == (7,0):
				self.board[7][4] = NoType(pieceColor.NoColor)
				self.board[7][0] = NoType(pieceColor.NoColor)
				self.board[7][2] = piece
				self.board[7][3] = pieceOnNewPos
			elif self.whiteShortRokadePossible and (r,c) == (7,7):
				self.board[7][4] = NoType(pieceColor.NoColor)
				self.board[7][7] = NoType(pieceColor.NoColor)
				self.board[7][5] = pieceOnNewPos
				self.board[7][6] = piece
			self.blackLongRokadePossible = False
			self.blackShortRokadePossible = False
			self.whiteLongRokadePossible = False
			self.whiteShortRokadePossible = False
			
			self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
			self.time += 1
			self.printStatus(piece, (i,j), (r,c))
			return True

		# Handle en passant left
		if isinstance(piece, Pawn) and piece.enPassantLeft(i, j, self.board):
			if piece.color() == pieceColor.Black and (r,c) == (i + 1, j - 1):
				self.board[i][j] = NoType(pieceColor.NoColor)
				self.board[i][j - 1] = NoType(pieceColor.NoColor)
				self.board[r][c] = piece
				
				self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
				self.time += 1
				self.printStatus(piece, (i,j), (r,c))
				return True
			if piece.color() == pieceColor.White and (r,c) == (i - 1, j - 1):
				self.board[i][j] = NoType(pieceColor.NoColor)
				self.board[i][j - 1] = NoType(pieceColor.NoColor)
				self.board[r][c] = piece
				
				self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
				self.time += 1
				self.printStatus(piece, (i,j), (r,c))
				return True
		# Handle en passant right
		if isinstance(piece, Pawn) and piece.enPassantRight(i, j, self.board):
			if piece.color() == pieceColor.Black and (r,c) == (i + 1, j + 1):
				self.board[i][j] = NoType(pieceColor.NoColor)
				self.board[i][j + 1] = NoType(pieceColor.NoColor)
				self.board[r][c] = piece
				
				self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
				self.time += 1
				self.printStatus(piece, (i,j), (r,c))
				return True
			if piece.color() == pieceColor.White and (r,c) == (i - 1, j + 1):
				self.board[i][j] = NoType(pieceColor.NoColor)
				self.board[i][j + 1] = NoType(pieceColor.NoColor)
				self.board[r][c] = piece
				
				self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
				self.time += 1
				self.printStatus(piece, (i,j), (r,c))
				return True

		# If not, check if piece can move to newPos and act accordingly
		if (r,c) in legalMoves:
			# Only move if it doesn't put king in check.
			checkGame = Game(self.root)
			checkGame.copyData(self)
			checkGame.checkMove(piece, newPos)
			if piece.color() == pieceColor.Black:
				if checkGame.isCheckBlack():
					messagebox.showinfo("Check", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed. Black would be in check!")
					return False
			elif checkGame.isCheckWhite():
				messagebox.showinfo("Check", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed. White would be in check!")
				return False
			checkGame = None

			piece.firstMove = False
			oldPiece = self.board[i][j]
			self.board[i][j] = NoType(pieceColor.NoColor)
			self.board[r][c] = piece

			self.time += 1
			if isinstance(piece, Pawn) and piece.canPromote(r, c):
				self.pawnToPromote = piece
				self.promoteWindow()
				self.root.wait_window(self.win)
				self.promotePawn()
			self.stackOfMoves.append((piece, (i,j), (r,c), NoType(pieceColor.NoColor)))
			self.printStatus(piece, (i,j), (r,c))
			return True
		else:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed.")

			return False

	def checkMove(self, piece, newPos):
		i, j = self.getCurrentPosOfPiece(piece)
		r, c = newPos
		self.board[i][j] = NoType(pieceColor.NoColor)
		self.board[r][c] = piece

	def promoteWindow(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Promote")

		l = tk.Label(self.win, text="Choose piece to promote to:")
		l.grid(row=0, column=0)

		bQueen = tk.Button(self.win, text="Queen", command=(lambda: self.promoteCallback("Queen")))
		bQueen.grid(row=0, column=1)

		bRook = tk.Button(self.win, text="Rook", command=(lambda: self.promoteCallback("Rook")))
		bRook.grid(row=0, column=2)

		bBishop = tk.Button(self.win, text="Bishop", command=(lambda: self.promoteCallback("Bishop")))
		bBishop.grid(row=0, column=3)

		bKnight = tk.Button(self.win, text="Knight", command=(lambda: self.promoteCallback("Knight")))
		bKnight.grid(row=0, column=4)

	def promoteCallback(self, promotedPiece):
		self.promotedPiece = promotedPiece
		self.win.destroy()

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

		if newColor == pieceColor.Black:	self.blackPiecesInGame.append(newPiece)
		if newColor == pieceColor.White:	self.whitePiecesInGame.append(newPiece)

		self.board[r][c] = newPiece

		print("> BOARD AT TIME ", self.time, ": PROMOTED " + str(self.pawnToPromote) + " ON ", (r,c), " TO A", newPiece)
		print("---------------------------------------------------------------------")
		self.pawnToPromote = None

	def isCheck(self, verbose=True):
		blackIsCheck = self.isCheckBlack()
		whiteIsCheck = self.isCheckWhite()
		# print("> BOARD AT TIME ", self.time, ": BLACK IS", "" if blackIsCheck else " NOT ", "IN CHECK.")
		# print("------------------------------------")
		# print("> BOARD AT TIME ", self.time, ": WHITE IS", "" if whiteIsCheck else " NOT ", "IN CHECK.")
		# print("------------------------------------")
		return (blackIsCheck, whiteIsCheck)

	def isCheckBlack(self):
		blackKing = None
		for piece in self.blackPiecesInGame:
			if isinstance(piece, King):
				blackKing = piece
		posBlackKing = self.getCurrentPosOfPiece(blackKing)
		for whitePiece in self.whitePiecesInGame:
			posWhitePiece = self.getCurrentPosOfPiece(whitePiece)
			takeableMoves = whitePiece.takeableMoves(posWhitePiece, None, self.board)
			if posBlackKing in takeableMoves:
				return True
		return False
					
	def isCheckWhite(self):
		whiteKing = None
		for piece in self.whitePiecesInGame:
			if isinstance(piece, King):
				whiteKing = piece
		posWhiteKing = self.getCurrentPosOfPiece(whiteKing)
		for blackPiece in self.blackPiecesInGame:
			posBlackPiece = self.getCurrentPosOfPiece(blackPiece)
			takeableMoves = blackPiece.takeableMoves(posBlackPiece, None, self.board)
			if posWhiteKing in takeableMoves:
				return True
		return False
					
	def isCheckmate(self):
		blackIsCheckmate = self.isCheckmateBlack()
		whiteIsCheckmate = self.isCheckmateWhite()
		# print("> BOARD AT TIME ", self.time, ": BLACK IS", "" if blackIsCheckmate else " NOT ", "IN CHECKMATE.")
		# print("------------------------------------")
		# print("> BOARD AT TIME ", self.time, ": WHITE IS", "" if whiteIsCheckmate else " NOT ", "IN CHECKMATE.")
		# print("------------------------------------")
		return (blackIsCheckmate, whiteIsCheckmate)

	def isCheckmateBlack(self):
		if self.isCheckBlack():
			king = None
			for piece in self.blackPiecesInGame:
				if isinstance(piece, King):
					king = piece
			r, c = self.getCurrentPosOfPiece(king)
			possibleMovesKing = king.possibleMoves(r, c)

			checkGames = []
			for move in possibleMovesKing:
				checkGame = Game(self.root)
				checkGame.copyData(self)
				checkGame.checkMove(king, move)
				checkGames.append(checkGame)

			checkInGames = [checkGame.isCheckBlack() for checkGame in checkGames]
			return all(check for check in checkInGames)			
		return False

	def isCheckmateWhite(self):
		if self.isCheckWhite():
			king = None
			for piece in self.whitePiecesInGame:
				if isinstance(piece, King):
					king = piece
			r, c = self.getCurrentPosOfPiece(king)
			possibleMovesKing = king.possibleMoves(r, c)
			
			checkGames = []
			for move in possibleMovesKing:
				checkGame = Game(self.root)
				checkGame.copyData(self)
				checkGame.checkMove(king, move)
				checkGames.append(checkGame)

			checkInGames = [checkGame.isCheckWhite() for checkGame in checkGames]
			return all(check for check in checkInGames)		
		return False	

	def rokade(self, color):
		if color == pieceColor.Black:
			return self.rokadeBlack()
		elif color == pieceColor.White:
			return self.rokadeWhite()

	def rokadeBlack(self):
		rookLongRokade = self.getPieceOnPosition((0,0))
		blackKing = self.getPieceOnPosition((0,4))
		rookShortRokade = self.getPieceOnPosition((0,7))

		rokadeMoves = []
		
		if not self.isCheckBlack():
			if not isinstance(rookLongRokade, NoType) and not isinstance(blackKing, NoType):
				if isinstance(self.getPieceOnPosition((0,1)), NoType) and \
				   isinstance(self.getPieceOnPosition((0,2)), NoType) and \
				   isinstance(self.getPieceOnPosition((0,3)), NoType):
					if not self.checkIfBlackKingInCheckOnPositions([(0,2),(0,3)]):	# Dit kijkt zowel plaatsen waar hij over zou gaan als plaats waar hij terechtkomt
						self.blackLongRokadePossible = True
						rokadeMoves.extend([(0,2),(0,3)])
			if not isinstance(rookShortRokade, NoType) and not isinstance(blackKing, NoType):
				if isinstance(self.getPieceOnPosition((0,5)), NoType) and \
				   isinstance(self.getPieceOnPosition((0,6)), NoType):
					if not self.checkIfBlackKingInCheckOnPositions([(0,5),(0,6)]):
						self.blackShortRokadePossible = True
						rokadeMoves.extend([(0,5),(0,6)])
		return rokadeMoves

	def checkIfBlackKingInCheckOnPositions(self, positions):
		for move in positions:
			for whitePiece in self.whitePiecesInGame:
				posWhitePiece = self.getCurrentPosOfPiece(whitePiece)
				takeableMoves = whitePiece.takeableMoves(posWhitePiece, None, self.board)
				if move in takeableMoves:
					return True
		return False

	def rokadeWhite(self):
		rookLongRokade = self.getPieceOnPosition((7,0))
		whiteKing = self.getPieceOnPosition((7,4))
		rookShortRokade = self.getPieceOnPosition((7,7))
		
		rokadeMoves = []
		
		if not self.isCheckWhite():
			if not isinstance(rookLongRokade, NoType) and not isinstance(whiteKing, NoType):
				if isinstance(self.getPieceOnPosition((7,1)), NoType) and \
				   isinstance(self.getPieceOnPosition((7,2)), NoType) and \
				   isinstance(self.getPieceOnPosition((7,3)), NoType):
					if not self.checkIfWhiteKingInCheckOnPositions([(7,2),(7,3)]):
						self.whiteLongRokadePossible = True
						rokadeMoves.extend([(7,2),(7,3)])
			if not isinstance(rookShortRokade, NoType) and not isinstance(whiteKing, NoType):
				if isinstance(self.getPieceOnPosition((7,5)), NoType) and \
				   isinstance(self.getPieceOnPosition((7,6)), NoType):
					if not self.checkIfWhiteKingInCheckOnPositions([(7,5),(7,6)]):
						self.whiteShortRokadePossible = True
						rokadeMoves.extend([(7,5),(7,6)])
		return rokadeMoves

	def checkIfWhiteKingInCheckOnPositions(self, positions):
		for move in positions:
			for blackPiece in self.blackPiecesInGame:
				posBlackPiece = self.getCurrentPosOfPiece(blackPiece)
				takeableMoves = blackPiece.takeableMoves(posBlackPiece, None, self.board)
				if move in takeableMoves:
					return True
		return False

	def pat(self):
		self.patBlack()
		self.patWhite()

	def patBlack(self):
		possibleMoves = []
		for blackPiece in self.blackPiecesInGame:
			posBlackPiece = self.getCurrentPosOfPiece(blackPiece)
			possibleMoves.extend(blackPiece.legalMovesAndNotBlocked(posBlackPiece, None, self.board))
			possibleMoves.extend(blackPiece.takeableMoves(posBlackPiece, None, self.board))

		return len(possibleMoves) == 0

	def patWhite(self):
		possibleMoves = []
		for whitePiece in self.whitePiecesInGame:
			posWhitePiece = self.getCurrentPosOfPiece(whitePiece)
			possibleMoves.extend(whitePiece.legalMovesAndNotBlocked(whitePiece, posWhitePiece[0], posWhitePiece[1]))
			possibleMoves.extend(whitePiece.takeableMoves(posWhitePiece, None, self.board))

		return len(possibleMoves) == 0

	def boardToString(self):
		result = ""
		color = ""
		for i in range(0, 8):
			comma = ","
			for j in range(0, 8):
				color = "_W" if self.board[i][j].color() == pieceColor.White else "_B"
				selected = "_T" if self.board[i][j].selected else "_F"
				if j == 7:
					comma = ""
				if isinstance(self.board[i][j], Pawn):
					result += "P" + color + comma
				elif isinstance(self.board[i][j], Rook):
					result += "R" + color + comma
				elif isinstance(self.board[i][j], Knight):
					result += "KN" + color + comma
				elif isinstance(self.board[i][j], Bishop):
					result += "B" + color + comma
				elif isinstance(self.board[i][j], Queen):
					result += "Q" + color + comma
				elif isinstance(self.board[i][j], King):
					result += "K" + color + comma
				else:
					result += "x" + comma
			result += "\n"
		return result

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
		# print("> BLACK PIECES STILL IN THE GAME:")
		# print(self.blackPiecesInGame)
		# print("> WHITE PIECES STILL IN THE GAME:")
		# print(self.whitePiecesInGame)
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

		# print("> STACK OF MOVES AT TIME ", self.time)
		# print(self.stackOfMoves)

		self.isCheck()
		self.isCheckmate()

	def reset(self):
		self.board = [[NoType(pieceColor.NoColor)] * 8 for i in range(8)]
		self.time = 0

		self.stackOfMoves = deque()

		self.blackPiecesInGame = []
		self.takenBlackPieces = []
		self.whitePiecesInGame = []
		self.takenWhitePieces = []

		self.pawnToPromote = None
		self.check = False
		self.checkmate = False
		self.colorInCheckmate = None

		self.blackLongRokadePossible = False
		self.blackShortRokadePossible = False
		self.whiteLongRokadePossible = False
		self.whiteShortRokadePossible = False