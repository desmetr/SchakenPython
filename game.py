from chesspiece import *
import numpy as np

class Game:
	def __init__(self):
		self.board = [[NoType(pieceColor.White)] * 8 for i in range(8)]
		self.time = 0
		self.firstMoveWhite = not self.time
		self.firstMoveBlack = not self.time

		self.blackPiecesInGame = []
		self.whitePiecesInGame = []

		self.check = False
		self.checkmate = False
		self.colorInCheckmate = None

	def setCheckmateBoard(self):
		P1B = Pawn(pieceColor.Black)
		KnB = Knight(pieceColor.Black)
		P3B = Pawn(pieceColor.Black)
		P4B = Pawn(pieceColor.Black)
		KB = King(pieceColor.Black)
		RB = Rook(pieceColor.Black)
		self.board[0][4] = KB
		self.board[1][6] = RB
		self.board[0][3] = P1B
		self.board[0][5] = KnB
		self.board[1][3] = P3B
		self.board[1][4] = P4B
		self.blackPiecesInGame.extend([RB, KB, P1B, KnB, P3B, P4B])

		B1W = Bishop(pieceColor.White)
		self.board[3][7] = B1W
		self.whitePiecesInGame.extend([B1W])

		self.printStatus(None,None,None,True)
		# self.isCheck(pieceColor.Black)
		# self.isCheck(pieceColor.White)

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
		
		legalMovesAndNotBlocked = legalMoves
		# Check if another piece is blocking path to newPos
		# Ask every piece for the path from the current pos to newPos
		if newPos in legalMoves:
			if not (isinstance(piece, Knight) or isinstance(piece, King)):
				legalMovesAndNotBlocked = piece.getLegalMovesAndNotBlockedInPath((ci, cj), newPos, self.board)
		
		return legalMovesAndNotBlocked

	def move(self, piece, newPos): # Verplaats piece naar rij r en kolom c
		i, j = self.getCurrentPosOfPiece(piece)
		r, c = newPos

		if piece.color() != pieceColor.White and self.time == 0:
			print("> BOARD AT TIME ", self.time, ": MOVE " + str(piece) + " FROM ", (i,j), " TO ", newPos, " NOT ALLOWED. WHITE HAS TO START.\n")
			return False

		legalMoves = self.legalMoves(piece, newPos)
		takeableMoves = piece.takeableMoves((i,j), (r,c), self.board)

		self.isCheck(piece.color())
		# print("isCheck", self.check)
		self.isCheckmate(piece.color())
		# print("isCheckmate", self.checkmate)
		if self.checkmate:
			self.handleEndGame()

		# Check if piece can take another piece on newPos
		if not isinstance(self.board[r][c], NoType) and newPos in takeableMoves and self.board[r][c].color() != self.board[i][j].color():
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
		takeableWhitePieces = []
		for whitePiece in self.whitePiecesInGame:
			(wi,wj) = self.getCurrentPosOfPiece(whitePiece)
			for blackPiece in self.blackPiecesInGame:
				(bi,bj) = self.getCurrentPosOfPiece(blackPiece)
				takeableMoves = blackPiece.takeableMoves((bi,bj), (wi,wj), self.board)
				# if isinstance(blackPiece, Queen):
				# 	print(blackPiece, " at ", (bi,bj), "->", takeableMoves)
				if (wi,wj) in takeableMoves:
					# print("'",(wi,wj))
					takeableWhitePieces.append((whitePiece, (wi,wj)))
		return takeableWhitePieces

	def isCheck(self, color, verbose=True):
		if color == pieceColor.Black:
			takeableBlackPieces = self.findAllTakeableBlackPieces()
			# print("@1",takeableBlackPieces)
			for piece, pos in takeableBlackPieces:
				if isinstance(piece, King):
					if verbose: print("> BLACK IS IN CHESS")
					self.check = True
		if color == pieceColor.White:
			takeableWhitePieces = self.findAllTakeableWhitePieces()
			# print("@2",takeableWhitePieces)
			for piece, pos in takeableWhitePieces:
				if isinstance(piece, King):
					if verbose: print("> WHITE IS IN CHESS")
					self.check = True

	def isCheckmate(self, color):
		self.isCheck(color, False)
		if self.check:
			if color == pieceColor.Black:
				# Check if by moving the king, you resolve check, if so, not checkmate 
				canPieceResolve = []
				for blackPiece in self.blackPiecesInGame:
					if isinstance(blackPiece, King):
						r, c = self.getCurrentPosOfPiece(blackPiece)
						possibleMovesOfKing = blackPiece.possibleMoves(r, c)
						# print("possibleMovesOfKing",possibleMovesOfKing)

						for whitePiece in self.whitePiecesInGame:
							r, c = self.getCurrentPosOfPiece(whitePiece)
							possibleMovesWhite = whitePiece.possibleMoves(r, c)
							intersection = [move for move in possibleMovesWhite if move in possibleMovesOfKing]
							canPieceResolve.append(all(move in intersection for move in possibleMovesOfKing))
							# print("possibleMovesWhite", possibleMovesWhite)
							# print("intersection", intersection)
							# print(all(move in intersection for move in possibleMovesOfKing))

						# print("canPieceResolve", canPieceResolve)
						# print("any", any(result for result in canPieceResolve))
						self.checkmate = any(result for result in canPieceResolve)
				
				# If moving the king doesn't resolve checkmate, try moving the other remaining pieces to resolve, if this helps, not checkmate
				if not self.checkmate:
					# print("tweede if")
					canPieceResolve = []
					for blackPiece in self.blackPiecesInGame:
						if not isinstance(blackPiece, King):
							# print("--------")
							r, c = self.getCurrentPosOfPiece(blackPiece)
							possibleMovesOfPiece = blackPiece.possibleMoves(r, c)
							# print(blackPiece,(r,c),"possibleMovesOfPiece",possibleMovesOfPiece)

							for whitePiece in self.whitePiecesInGame:
								r, c = self.getCurrentPosOfPiece(whitePiece)
								possibleMovesWhite = whitePiece.possibleMoves(r, c)
								# print("possibleMovesWhite", possibleMovesWhite)
								intersection = [move for move in possibleMovesWhite if move in possibleMovesOfPiece]
								# print("intersection", intersection)
								canPieceResolve.append(any(move in intersection for move in possibleMovesOfPiece))
								# print(any(move in intersection for move in possibleMovesOfPiece))

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
						possibleMovesOfKing = whitePiece.possibleMoves(r, c)
						# print("possibleMovesOfKing",possibleMovesOfKing)

						for blackPiece in self.blackPiecesInGame:
							r, c = self.getCurrentPosOfPiece(blackPiece)
							possibleMovesBlack = blackPiece.possibleMoves(r, c)
							intersection = [move for move in possibleMovesBlack if move in possibleMovesOfKing]
							canPieceResolve.append(all(move in intersection for move in possibleMovesOfKing))
							# print("possibleMovesBlack", possibleMovesBlack)
							# print("intersection", intersection)
							# print(all(move in intersection for move in possibleMovesOfKing))

						# print("canPieceResolve", canPieceResolve)
						# print("any", any(result for result in canPieceResolve))
						self.checkmate = any(result for result in canPieceResolve)
				
				# If moving the king doesn't resolve checkmate, try moving the other remaining pieces to resolve, if this helps, not checkmate
				if not self.checkmate:
					# print("tweede if")
					canPieceResolve = []
					for whitePiece in self.whitePiecesInGame:
						if not isinstance(whitePiece, King):
							# print("--------")
							r, c = self.getCurrentPosOfPiece(whitePiece)
							possibleMovesOfPiece = whitePiece.possibleMoves(r, c)
							# print(blackPiece,(r,c),"possibleMovesOfPiece",possibleMovesOfPiece)

							for blackPiece in self.blackPiecesInGame:
								r, c = self.getCurrentPosOfPiece(blackPiece)
								possibleMovesBlack = blackPiece.possibleMoves(r, c)
								# print("possibleMovesBlack", possibleMovesBlack)
								intersection = [move for move in possibleMovesBlack if move in possibleMovesOfPiece]
								# print("intersection", intersection)
								canPieceResolve.append(any(move in intersection for move in possibleMovesOfPiece))
								# print(any(move in intersection for move in possibleMovesOfPiece))

							# print("canPieceResolve", canPieceResolve)
							# print("any", any(result for result in canPieceResolve))
							self.checkmate = any(result for result in canPieceResolve)
				
				if self.checkmate:
					self.colorInCheckmate = pieceColor.White 
					self.handleEndGame()

	def pat(self, color):
		return False

	def handleEndGame(self):
		print(">", self.colorInCheckmate.name.upper(), "IS IN CHECKMATE, END GAME.")
		self.checkmate = False
		self.check = False
		self.colorInCheckmate = None

	def printBoard(self):
		result = ""
		color = ""
		for i in range(0, 8):
			for j in range(0, 8):
				color = "_W" if self.board[i][j].color() == pieceColor.White else "_B"
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