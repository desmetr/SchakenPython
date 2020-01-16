from chesspiece import *
import numpy as np
from tkinter import messagebox
import logging

f= open("chess.log","w+")

class Game:
	def __init__(self, root):
		self.board = [[NoType(pieceColor.White)] * 8 for i in range(8)]
		self.time = 0
		self.firstMoveWhite = not self.time
		self.firstMoveBlack = not self.time

		self.root = root

		self.blackPiecesInGame = []
		self.whitePiecesInGame = []

		self.check = False
		self.checkmate = False
		self.colorInCheckmate = None

	def setPawnBoard(self):
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		P5B = Pawn(pieceColor.Black)
		P6B = Pawn(pieceColor.Black)
		P7B = Pawn(pieceColor.Black)
		P8B = Pawn(pieceColor.Black)
		self.board[1][0] = P1B
		self.board[1][1] = P2B
		self.board[1][2] = P3B
		self.board[1][3] = P4B
		self.board[1][4] = P5B
		self.board[1][5] = P6B
		self.board[1][6] = P7B
		self.board[1][7] = P8B
		self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B])

		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		# self.board[6][0] = P1W
		self.board[2][1] = P2W
		self.board[2][2] = P3W
		self.board[2][3] = P4W
		self.board[2][4] = P5W
		self.board[2][5] = P6W
		self.board[2][6] = P7W
		self.board[2][7] = P8W
		self.whitePiecesInGame.extend([P8W, P2W, P3W, P4W, P5W, P6W, P7W])

		self.printStatus(None,None,None,True)
	
	def setRookBoard(self):
		R1B = Rook(pieceColor.Black)
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		# R2B = Rook(pieceColor.Black)
		self.board[0][0] = R1B
		# self.board[0][7] = R2B
		# self.board[2][5] = R1B
		self.blackPiecesInGame.extend([R1B])
		R1W = Rook(pieceColor.White)
		R2W = Rook(pieceColor.White)
		self.board[0][1] = R1W
		self.board[7][0] = R2W
		# self.board[4][4] = R1W
		self.whitePiecesInGame.extend([R1W,R2W])
		self.printStatus(None,None,None,True)

	def setKnightBoard(self):
		Kn1B = Knight(pieceColor.Black)
		Kn2B = Knight(pieceColor.Black)
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		P5B = Pawn(pieceColor.Black)
		P6B = Pawn(pieceColor.Black)
		P7B = Pawn(pieceColor.Black)
		P8B = Pawn(pieceColor.Black)
		self.board[0][1] = Kn1B
		# self.board[0][6] = Kn2B
		self.board[1][0] = P1B
		self.board[1][1] = P2B
		self.board[1][2] = P3B
		self.board[1][3] = P4B
		self.board[1][4] = P5B
		self.board[1][5] = P6B
		self.board[1][6] = P7B
		self.board[1][7] = P8B
		# self.board[3][4] = Kn1B
		self.blackPiecesInGame.extend([P1B, P2B, P3B, P4B, P5B, P6B, P7B, P8B, Kn1B])

		Kn1W = Knight(pieceColor.White)
		Kn2W = Knight(pieceColor.White)
		self.board[2][0] = Kn1W
		self.board[2][2] = Kn2W
		# self.board[1][6] = Kn1W
		self.whitePiecesInGame.extend([Kn1W, Kn2W])
	
		self.printStatus(None,None,None,True)

	def setBishopBoard(self):
		B1B = Bishop(pieceColor.Black)
		B2B = Bishop(pieceColor.Black)
		P1B = Pawn(pieceColor.Black)
		P2B = Pawn(pieceColor.Black)
		self.board[1][1] = P1B
		# self.board[6][2] = P2B
		self.board[0][2] = B1B
		self.board[0][5] = B2B
		self.blackPiecesInGame.extend([P1B,P2B,B1B,B2B])

		B1W = Bishop(pieceColor.White)
		B2W = Bishop(pieceColor.White)
		self.board[7][2] = B1W
		self.board[7][7] = B2W
		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		self.board[2][0] = P1W
		self.board[2][4] = P2W
		self.board[2][3] = P3W
		self.board[2][7] = P4W
		# self.board[6][4] = P5W
		# self.board[6][5] = P6W
		# self.board[6][6] = P7W
		# self.board[6][7] = P8W
		self.whitePiecesInGame.extend([B1W,B2W,P1W,P2W,P3W,P4W])

		self.printStatus(None,None,None,True)

	def setQueenBoard(self):
		QB = Queen(pieceColor.Black)
		self.board[0][3] = QB
		# self.board[4][4] = QB
		self.blackPiecesInGame.extend([QB])
		QW = Queen(pieceColor.White)
		self.board[7][3] = QW
		# self.board[4][4] = QW
		self.whitePiecesInGame.extend([QW])
		self.printStatus(None,None,None,True)

	def setKingBoard(self):
		KB = King(pieceColor.Black)
		self.board[0][4] = KB
		# self.board[3][5] = KB
		self.blackPiecesInGame.extend([KB])
		P1W = Pawn(pieceColor.White)
		P2W = Pawn(pieceColor.White)
		P3W = Pawn(pieceColor.White)
		P4W = Pawn(pieceColor.White)
		P5W = Pawn(pieceColor.White)
		P6W = Pawn(pieceColor.White)
		P8W = Pawn(pieceColor.White)
		P7W = Pawn(pieceColor.White)
		# self.board[6][0] = P1W
		self.board[0][3] = P2W
		self.board[0][5] = P3W
		self.board[1][3] = P4W
		self.board[1][4] = P5W
		self.board[1][5] = P6W
		self.board[2][6] = P7W
		self.board[2][7] = P8W
		self.whitePiecesInGame.extend([P8W, P2W, P3W, P4W, P5W, P6W, P7W])
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
		self.isCheck(pieceColor.Black)
		self.isCheck(pieceColor.White)

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

	def legalMoves(self, piece, newPos):
		ci, cj = self.getCurrentPosOfPiece(piece)
		# Get all possible moves of a piece, regardless of the state of the game
		possibleMoves = piece.possibleMoves(ci, cj, self.firstMoveBlack, self.firstMoveWhite)

		if isinstance(piece, Pawn) and piece.color() == pieceColor.White:
			self.firstMoveWhite = False
		if isinstance(piece, Pawn) and piece.color() == pieceColor.Black:
			self.firstMoveBlack = False

		# Check with state of the game to eliminate all positions another piece is already on
		legalMoves = []
		for move in possibleMoves:
			r, c = move
			if isinstance(self.board[r][c], NoType):
				legalMoves.append(move)
		# if isinstance(piece, Queen):
		# 	print("legalMoves", legalMoves)
		legalMovesAndNotBlocked = legalMoves
		# Check if another piece is blocking path to newPos
		# Ask every piece for the path from the current pos to newPos
		if newPos in legalMoves:
			legalMovesAndNotBlocked = piece.getLegalMovesAndNotBlockedInPath((ci, cj), newPos, self.board)
		# if isinstance(piece, Queen):
		# 	print("legalMovesAndNotBlocked", legalMovesAndNotBlocked)
		return legalMovesAndNotBlocked

	def move(self, piece, newPos): # Verplaats piece naar rij r en kolom c
		i, j = self.getCurrentPosOfPiece(piece)
		r, c = newPos

		if piece.color() != pieceColor.White and self.time == 0:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED. WHITE HAS TO START.\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed. White has to start.")

			return False

		legalMoves = self.legalMoves(piece, newPos)
		# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",piece)
		takeableMoves = piece.takeableMoves((i,j), (r,c), self.board)
		# if isinstance(piece, Queen):
			# print("takeableMoves", takeableMoves)

		# self.isCheck(piece.color())
		# print("isCheck", self.check)
		# self.isCheckmate(piece.color())
		# print("isCheckmate", self.checkmate)
		# if self.checkmate:
		# 	self.handleEndGame()

		# Check if piece can take another piece on newPos
		if not isinstance(self.board[r][c], NoType) and newPos in takeableMoves and self.board[r][c].color() != self.board[i][j].color():
			# print("IN TAKE")
			print("> You can take piece ", self.board[r][c], " on position", newPos, "!")
			oldPiece = self.board[r][c]
			if oldPiece.color() == pieceColor.Black: self.blackPiecesInGame.remove(oldPiece)
			if oldPiece.color() == pieceColor.White: self.whitePiecesInGame.remove(oldPiece)
			
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

			self.time += 1
			self.printStatus(piece, (i,j), (r,c))
			return True
		else:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED\n")
			messagebox.showinfo("Wrong Move", "Board at time " + str(self.time) + ": move " + str(piece) + " from " + str((i,j)) + " to " + str(newPos) + " not allowed.")

			return False

	def findAllTakeableBlackPieces(self):
		takeableBlackPieces = []
		for blackPiece in self.blackPiecesInGame:
			(bi,bj) = self.getCurrentPosOfPiece(blackPiece)
			for whitePiece in self.whitePiecesInGame:
				(wi,wj) = self.getCurrentPosOfPiece(whitePiece)
				# if isinstance(whitePiece, Bishop):
					# print((bi,bj))
					# print(whitePiece, " at ", (wi,wj), "->", whitePiece.takeableMoves((wi,wj), (bi,bj), self.board))
				if (bi,bj) in whitePiece.takeableMoves((wi,wj), (bi,bj), self.board):
					takeableBlackPieces.append((blackPiece, (bi,bj)))
		return takeableBlackPieces

	def findAllTakeableWhitePieces(self):
		f.write(str(self.time) + "@@@@@@@@@@@@@@@@@@@@@@@\n")
		takeableWhitePieces = []
		for whitePiece in self.whitePiecesInGame:
			(wi,wj) = self.getCurrentPosOfPiece(whitePiece)
			f.write("(wi,wj)"+str((wi,wj))+"\n")
			for blackPiece in self.blackPiecesInGame:
				(bi,bj) = self.getCurrentPosOfPiece(blackPiece)
				f.write("\t(bi,bj)"+str((bi,bj))+"\n")
				takeableMoves = blackPiece.takeableMoves((bi,bj), (wi,wj), self.board)
				f.write("\t"+str(blackPiece)+" takeableMoves " + str(takeableMoves)+"\n")
				# if isinstance(blackPiece, Queen):
				# 	print(blackPiece, " at ", (bi,bj), "->", takeableMoves)
				if (wi,wj) in takeableMoves:
					# print("'",(wi,wj))
					takeableWhitePieces.append((whitePiece, (wi,wj)))
				# f.write("\t\ttakeableWhitePieces"+str(takeableWhitePieces)+"\n")
		return takeableWhitePieces

	def isCheck(self, color, verbose=True):
		if color == pieceColor.Black:
			takeableBlackPieces = self.findAllTakeableBlackPieces()
			# print("@1",takeableBlackPieces)
			for piece, pos in takeableBlackPieces:
				if isinstance(piece, King):
					if verbose: 
						print("> BLACK IS IN CHESS")
						# messagebox.showinfo("Chess", "Board at time " + str(self.time) + ": Black is in chess!")
					self.check = True
					break
		if color == pieceColor.White:
			takeableWhitePieces = self.findAllTakeableWhitePieces()
			# print("@2",takeableWhitePieces)
			for piece, pos in takeableWhitePieces:
				if isinstance(piece, King):
					if verbose: 
						print("> WHITE IS IN CHESS")
						# messagebox.showinfo("Chess", "Board at time " + str(self.time) + ": White is in chess!")
					self.check = True
					break

	def isCheckmate(self, color):
		self.isCheck(color, False)
		isResolved = False
		if self.check:
			if color == pieceColor.Black:
				# Check if by moving the king, you resolve check, if so, not checkmate 
				canPieceResolve = []
				for blackPiece in self.blackPiecesInGame:
					if isinstance(blackPiece, King):
						r, c = self.getCurrentPosOfPiece(blackPiece)
						# possibleMovesOfKing = blackPiece.possibleMoves(r, c)
						possibleMovesOfKing = blackPiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
						takeableMovesOfKing = blackPiece.takeableMoves((r, c), None, self.board)
						possibleMovesOfKing.extend(takeableMovesOfKing)
						print("possibleMovesOfKing",possibleMovesOfKing)

						for whitePiece in self.whitePiecesInGame:
							r, c = self.getCurrentPosOfPiece(whitePiece)
							possibleMovesWhite = whitePiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
							intersection = [move for move in possibleMovesWhite if move in possibleMovesOfKing]
							canPieceResolve.append(all(move in intersection for move in possibleMovesOfKing))
							print(whitePiece,"possibleMovesWhite", possibleMovesWhite)
							print("intersection", intersection)
							print(all(move in intersection for move in possibleMovesOfKing))

						print("canPieceResolve", canPieceResolve)
						print("any", any(result for result in canPieceResolve))
						self.checkmate = any(result for result in canPieceResolve)
						isResolved = not self.checkmate

				# If moving the king doesn't resolve checkmate, try moving the other remaining pieces to resolve, if this helps, not checkmate
				if not isResolved:
					print("tweede if")
					canPieceResolve = []
					for blackPiece in self.blackPiecesInGame:
						if not isinstance(blackPiece, King):
							print("--------")
							rB, cB = self.getCurrentPosOfPiece(blackPiece)
							# possibleMovesOfPiece = blackPiece.possibleMoves(r, c)
							possibleMovesOfPiece = blackPiece.getLegalMovesAndNotBlockedInPath((rB, cB), None, self.board)

							# print(blackPiece,(r,c),"possibleMovesOfPiece",possibleMovesOfPiece)
							possibleMovesOfPiece.append((rB,cB))
							# print(blackPiece,(r,c),"possibleMovesOfPiece",possibleMovesOfPiece)

							for whitePiece in self.whitePiecesInGame:
								rW, cW = self.getCurrentPosOfPiece(whitePiece)
								LegalMovesAndNotBlockedInPathWhite = whitePiece.getLegalMovesAndNotBlockedInPath((rW, cW), None, self.board)
								# print(whitePiece,"LegalMovesAndNotBlockedInPathWhite", LegalMovesAndNotBlockedInPathWhite)
								intersection = [move for move in LegalMovesAndNotBlockedInPathWhite if move in possibleMovesOfPiece]
								# print("intersection", intersection)
								canPieceResolve.append(any(move in intersection for move in LegalMovesAndNotBlockedInPathWhite))
								if any(move in intersection for move in LegalMovesAndNotBlockedInPathWhite):
									print(any(move in intersection for move in LegalMovesAndNotBlockedInPathWhite))
									print(blackPiece,(rB,cB),"possibleMovesOfPiece",possibleMovesOfPiece)
									print(whitePiece,(rW,cW),"LegalMovesAndNotBlockedInPathWhite", LegalMovesAndNotBlockedInPathWhite)
									print("intersection", intersection)

							# print("canPieceResolve", canPieceResolve)
							# print("any", any(result for result in canPieceResolve))
							self.checkmate = any(result for result in canPieceResolve)

				if self.checkmate:
					self.colorInCheckmate = pieceColor.Black
					self.handleEndGame()

			if color == pieceColor.White:
				# Check if by moving the king, you resolve check, if so, not checkmate 
				canPieceResolve = []
				for whitePiece in self.whitePiecesInGame:
					if isinstance(whitePiece, King):
						r, c = self.getCurrentPosOfPiece(whitePiece)
						# possibleMovesOfKing = whitePiece.possibleMoves(r, c)
						possibleMovesOfKing = whitePiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
						# f.write("possibleMovesOfKing "+str(possibleMovesOfKing)+"\n")

						for blackPiece in self.blackPiecesInGame:
							r, c = self.getCurrentPosOfPiece(blackPiece)
							possibleMovesBlack = blackPiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
							intersection = [move for move in possibleMovesBlack if move in possibleMovesOfKing]
							canPieceResolve.append(all(move in intersection for move in possibleMovesOfKing))
							# f.write("possibleMovesBlack "+str(possibleMovesBlack)+"\n")
							# f.write("intersection "+str(intersection)+"\n")
							# f.write(str(all(move in intersection for move in possibleMovesOfKing))+"\n")

						# f.write("canPieceResolve "+str(canPieceResolve)+"\n")
						# f.write("any "+ str(any(result for result in canPieceResolve))+"\n")
						self.checkmate = any(result for result in canPieceResolve)
						isResolved = not self.checkmate
				
				# If moving the king doesn't resolve checkmate, try moving the other remaining pieces to resolve, if this helps, not checkmate
				if not isResolved:
					# f.write("tweede if"+"\n")
					canPieceResolve = []
					for whitePiece in self.whitePiecesInGame:
						if not isinstance(whitePiece, King):
							# f.write("--------"+"\n")
							r, c = self.getCurrentPosOfPiece(whitePiece)
							# possibleMovesOfPiece = whitePiece.possibleMoves(r, c).append((r,c))
							possibleMovesOfPiece = whitePiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
							possibleMovesOfPiece.append((r,c))
							# f.write(str(blackPiece)+str((r,c))+" possibleMovesOfPiece "+str(possibleMovesOfPiece)+"\n")

							for blackPiece in self.blackPiecesInGame:
								r, c = self.getCurrentPosOfPiece(blackPiece)
								possibleMovesBlack = blackPiece.getLegalMovesAndNotBlockedInPath((r, c), None, self.board)
								# f.write("possibleMovesBlack "+str(possibleMovesBlack)+"\n")
								intersection = [move for move in possibleMovesBlack if move in possibleMovesOfPiece]
								# f.write("intersection "+str(intersection)+"\n")
								canPieceResolve.append(any(move in intersection for move in possibleMovesOfPiece))
								# f.write(str(any(move in intersection for move in possibleMovesOfPiece))+"\n")

							# f.write("canPieceResolve "+ str(canPieceResolve)+"\n")
							# f.write("any " + str(any(result for result in canPieceResolve))+"\n")
							self.checkmate = any(result for result in canPieceResolve)
				
				if self.checkmate:
					self.colorInCheckmate = pieceColor.White 
					self.handleEndGame()

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