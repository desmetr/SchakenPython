import tkinter as tk
from tkinter import *
from PIL import ImageTk
from math import floor
from chesspiece import *
from tkinter import *
import tkinter.filedialog
from game import Game
import mainwindow
import csv

class GameBoard(tk.Frame):
	def __init__(self, parent, game, rows=8, columns=8, size=64, color1="white", color2="blue"):
		self.parent = parent
		self.game = game
		self.previousGame = None
		self.rows = rows
		self.columns = columns
		self.size = size
		self.color1 = color1
		self.color2 = color2
		self.previousPiece = None
		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		self.imagesBoard = [[None] * 8 for i in range(8)]
		self.whiteTurn = True
		self.firstClick = True
		self.endOfGame = False
		self.blackPiecesListbox = Listbox(self.parent)
		self.whitePiecesListbox = Listbox(self.parent)

		canvas_width = columns * size
		canvas_height = rows * size

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
								width=canvas_width, height=canvas_height, background="bisque")
		
		self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

		self.menubar = Menu(self.parent)
		self.menubar.add_command(label="New", command=self.newGame)
		self.menubar.add_command(label="Quit", command=self.parent.quit)
		self.menubar.add_command(label="Save", command=self.save)
		self.menubar.add_command(label="Open", command=self.open)
		# self.menubar.add_command(label="Undo Move", command=self.undo)
		# self.menubar.add_command(label="Redo Move", command=self.redo)
		self.parent.config(menu=self.menubar)

		self.drawAllPieces()

		self.parent.bind('<Control-z>', self.undo)
		self.parent.bind('<Control-y>', self.redo)
		self.parent.bind('<Control-n>', self.newGameEvent)
		self.canvas.bind("<Configure>", self.refresh)
		self.canvas.bind("<Button-1>", self.click)

	def drawAllPieces(self):
		self.canvas.delete("image")
		for piece in self.pieces:
			r, c = self.game.getCurrentPosOfPiece(piece)
			self.imagesBoard[r][c] = self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

	def click(self, event):
		col_size = row_size = event.widget.master.size

		c = floor(event.x / col_size)
		r = floor(event.y / row_size)
		piece = self.game.getPieceOnPosition((r, c))
		x1 = (c * self.size)
		y1 = (r * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size

		lastColor = "white" if (r + c) % 2 == 0 else "blue"
		
		self.drawCheckmate(piece, r, c)
		# self.drawPat()

		if self.endOfGame:
			return

		self.resetDrawCheck()

		if not self.previousPiece and self.whiteTurn != (piece.color() == pieceColor.White):
			messagebox.showinfo("Wrong turn", "Not your turn!")
			return 
		else:
			if self.firstClick:
				if not isinstance(piece, NoType):
					self.previousPiece = piece
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green", tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")
					
					self.drawLegalMovesAndNotBlockedInPath(piece, r, c)
					self.drawTakeableMoves(piece, r, c)
					if isinstance(piece, King):
						self.drawRokadeMoves(piece)
					if isinstance(piece, Pawn):
						self.drawEnPassant(piece, r, c)

					self.firstClick = False
			else:	
				if self.previousPiece != piece:
					prevR, prevC = self.game.getCurrentPosOfPiece(self.previousPiece)
					prevX1 = (prevC * self.size)
					prevY1 = (prevR * self.size)
					prevX2 = prevX1 + self.size
					prevY2 = prevY1 + self.size

					if (prevR, prevC) != (r,c):
						prevLastColor = "white" if (prevR + prevC) % 2 == 0 else "blue"
						self.resetDrawLegalMovesAndNotBlockedInPath(self.previousPiece, prevR, prevC)
						self.resetDrawTakeableMoves(self.previousPiece, prevR, prevC)
						self.resetDrawRokadeMoves(self.previousPiece)
						if isinstance(self.previousPiece, Pawn):
							self.resetDrawEnPassant(self.previousPiece, prevR, prevC)

						if self.game.move(self.previousPiece, (r,c)):
							self.whiteTurn = not self.whiteTurn
							self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
							self.canvas.create_rectangle(prevX1, prevY1, prevX2, prevY2, outline="black", fill=prevLastColor, tags="square")
							self.drawCheck()
							self.drawAllPieces()
						else:
							self.canvas.create_rectangle(prevX1, prevY1, prevX2, prevY2, outline="black", fill=prevLastColor, tags="square")
							self.canvas.create_image(prevC * self.size, prevR * self.size, anchor=NW, image=self.previousPiece.image, tags="image")

							self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
							self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

						self.previousPiece.selected = False
					else:
						self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
						self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

					self.previousPiece = None

				elif self.previousPiece == piece:
					piece.selected = False
					self.previousPiece = None
					self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
					self.resetDrawTakeableMoves(piece, r, c)
					self.resetDrawRokadeMoves(piece)
					if isinstance(piece, Pawn):
						self.resetDrawEnPassant(piece, r, c)
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")


				elif not piece.selected:
					piece.selected = True
					if not isinstance(piece, NoType):
						self.previousPiece = piece
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green", tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")
				else:
					piece.selected = False
					if not isinstance(piece, NoType):
						self.previousPiece = piece
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

				self.firstClick = True

	def drawCheck(self):
		if self.game.isCheckBlack():
			kingR, kingC = self.game.getBlackKingPosition()
			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, width=4, outline="red", tags="check")
		if self.game.isCheckWhite():
			kingR, kingC = self.game.getWhiteKingPosition()
			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, width=4, outline="red", tags="check")

	def resetDrawCheck(self):
		if self.game.isCheckBlack():
			kingR, kingC = self.game.getBlackKingPosition()
			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, outline="black", tags="check")
		if self.game.isCheckWhite():
			kingR, kingC = self.game.getWhiteKingPosition()
			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, outline="black", tags="check")

	def drawCheckmate(self, piece, r, c):
		if self.game.isCheckmateBlack():
			blackKing = self.game.getBlackKing()
			kingR, kingC = self.game.getBlackKingPosition()
			
			self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
			self.resetDrawTakeableMoves(piece, r, c)

			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, fill="black", tags="checkmate")
			self.canvas.create_image(kingC * self.size, kingR * self.size, anchor=NW, image=blackKing.image, tags="image")
			messagebox.showinfo("Checkmate!", "Black is checkmate! End of game.")
			self.endOfGame = True

		if self.game.isCheckmateWhite():
			whiteKing = self.game.getWhiteKing()
			kingR, kingC = self.game.getWhiteKingPosition()

			self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
			self.resetDrawTakeableMoves(piece, r, c)
			
			kingX1 = (kingC * self.size)
			kingY1 = (kingR * self.size)
			kingX2 = kingX1 + self.size
			kingY2 = kingY1 + self.size
			
			self.canvas.create_rectangle(kingX1, kingY1, kingX2, kingY2, fill="black", tags="checkmate")
			self.canvas.create_image(kingC * self.size, kingR * self.size, anchor=NW, image=whiteKing.image, tags="image")
			messagebox.showinfo("Checkmate!", "White is checkmate! End of game.")
			self.endOfGame = True

	def drawPat(self):
		if self.game.patBlack():
			messagebox.showinfo("Pat!", "Black is in pat! No more possible moves. End of game.")
			self.endOfGame = True
		if self.game.patWhite():
			messagebox.showinfo("Pat!", "White is in pat! No more possible moves. End of game.")
			self.endOfGame = True

	def drawLegalMovesAndNotBlockedInPath(self, piece, r, c):
		for move in piece.legalMovesAndNotBlockedInPath((r,c), None, self.game.board):
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="yellow", tags="square")

	def drawTakeableMoves(self, piece, r, c):
		for move in piece.takeableMoves((r,c), None, self.game.board):
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			takeablePiece = self.game.getPieceOnPosition((moveR, moveC))
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="red", tags="square")
			self.canvas.create_image(moveC * self.size, moveR * self.size, anchor=NW, image=takeablePiece.image, tags="image")

	def drawRokadeMoves(self, piece):
		rokadeMoves = self.game.rokade(piece.color())
		for move in rokadeMoves:
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, width=4,outline="magenta", tags="rokade")

	def drawEnPassant(self, piece, r, c):
		if piece.enPassantLeft(r, c, self.game.board):
			if piece.color() == pieceColor.Black:
				moveX1 = (c - 1) * self.size
				moveY1 = (r + 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="yellow", tags="enpassant")
			else:
				moveX1 = (c - 1) * self.size
				moveY1 = (r - 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="yellow", tags="enpassant")
			takeablePiece = self.game.getPieceOnPosition((r, c - 1))
			moveX1 = (c - 1) * self.size
			moveY1 = r * self.size
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="red", tags="enpassant")
			self.canvas.create_image((c - 1) * self.size, r * self.size, anchor=NW, image=takeablePiece.image, tags="image")

		if piece.enPassantRight(r, c, self.game.board):
			if piece.color() == pieceColor.Black:
				moveX1 = (c + 1) * self.size
				moveY1 = (r + 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="yellow", tags="enpassant")
			else:
				moveX1 = (c + 1) * self.size
				moveY1 = (r - 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="yellow", tags="enpassant")
			takeablePiece = self.game.getPieceOnPosition((r, c + 1))
			moveX1 = (c + 1) * self.size
			moveY1 = r * self.size
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill="red", tags="enpassant")
			self.canvas.create_image((c + 1) * self.size, r * self.size, anchor=NW, image=takeablePiece.image, tags="image")
	
	def resetDrawLegalMovesAndNotBlockedInPath(self, piece, r, c):
		for move in piece.legalMovesAndNotBlockedInPath((r,c), None, self.game.board):
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			lastColor = "white" if (moveR + moveC) % 2 == 0 else "blue"
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="square")

	def resetDrawTakeableMoves(self, piece, r, c):
		for move in piece.takeableMoves((r,c), None, self.game.board):
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			lastColor = "white" if (moveR + moveC) % 2 == 0 else "blue"
			takeablePiece = self.game.getPieceOnPosition((moveR, moveC))
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="square")
			self.canvas.create_image(moveC * self.size, moveR * self.size, anchor=NW, image=takeablePiece.image, tags="image")

	def resetDrawRokadeMoves(self, piece):
		rokadeMoves = self.game.rokade(piece.color())
		self.canvas.delete("rokade")
		for move in rokadeMoves:
			moveR, moveC = move
			moveX1 = (moveC * self.size)
			moveY1 = (moveR * self.size)
			moveX2 = moveX1 + self.size
			moveY2 = moveY1 + self.size
			lastColor = "white" if (moveR + moveC) % 2 == 0 else "blue"
			self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", tags="rokade")

	def resetDrawEnPassant(self, piece, r, c):
		lastColor = "white" if (r + c) % 2 == 0 else "blue"
		moveX1 = c * self.size
		moveY1 = r * self.size
		moveX2 = moveX1 + self.size
		moveY2 = moveY1 + self.size
		self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
	
		if piece.enPassantLeft(r, c, self.game.board):
			if piece.color() == pieceColor.Black:
				lastColor = "white" if (r + (c - 1)) % 2 == 0 else "blue"
				moveX1 = (c - 1) * self.size
				moveY1 = r * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
				lastColor = "white" if ((r + 1) + (c - 1)) % 2 == 0 else "blue"
				moveX1 = (c - 1) * self.size
				moveY1 = (r + 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
			else:
				lastColor = "white" if ((r - 1) + (c - 1)) % 2 == 0 else "blue"
				moveX1 = (c - 1) * self.size
				moveY1 = (r - 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
				lastColor = "white" if (r + (c - 1)) % 2 == 0 else "blue"
				moveX1 = (c - 1) * self.size
				moveY1 = r * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
		if piece.enPassantRight(r, c, self.game.board):
			if piece.color() == pieceColor.Black:
				lastColor = "white" if ((r + 1) + (c + 1)) % 2 == 0 else "blue"
				moveX1 = (c + 1) * self.size
				moveY1 = (r + 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
				lastColor = "white" if (r + (c + 1)) % 2 == 0 else "blue"
				moveX1 = (c + 1) * self.size
				moveY1 = r * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
			else:
				lastColor = "white" if ((r + 1) + (c - 1)) % 2 == 0 else "blue"
				moveX1 = (c + 1) * self.size
				moveY1 = (r - 1) * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")
				lastColor = "white" if (r + (c + 1)) % 2 == 0 else "blue"
				moveX1 = (c + 1) * self.size
				moveY1 = r * self.size
				moveX2 = moveX1 + self.size
				moveY2 = moveY1 + self.size
				self.canvas.create_rectangle(moveX1, moveY1, moveX2, moveY2, outline="black", fill=lastColor, tags="enpassant")

	def getTakenBlackPieces(self):
		for piece in self.game.takenBlackPieces:
			if piece not in self.blackPiecesListbox:
				self.blackPiecesListbox.insert(END, piece)

	def getTakenWhitePieces(self):
		for piece in self.game.takenWhitePieces:
			if piece not in self.whitePiecesListbox:
				self.whitePiecesListbox.insert(END, piece)

	def refresh(self, event):
		xsize = int((event.width-1) / self.columns)
		ysize = int((event.height-1) / self.rows)
		self.size = min(xsize, ysize)
		self.canvas.delete("square")
		color = self.color2
		for row in range(self.rows):
			color = self.color1 if color == self.color2 else self.color2
			for col in range(self.columns):
				x1 = (col * self.size)
				y1 = (row * self.size)
				x2 = x1 + self.size
				y2 = y1 + self.size
				self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
				color = self.color1 if color == self.color2 else self.color2
	
		for piece in self.pieces:
			r, c = self.game.getCurrentPosOfPiece(piece)
			self.placepiece(str(piece), r, c)
		self.canvas.tag_raise("piece")
		self.canvas.tag_lower("square")

	def placepiece(self, name, row, column):
		x0 = (column * self.size) + int(self.size/2)
		y0 = (row * self.size) + int(self.size/2)
		self.canvas.coords(name, x0, y0)

	def undo(self, event):
		self.game.undo()
		self.drawAllPieces()

	def redo(self, event):
		self.game.redo()
		self.drawAllPieces()

	def newGameEvent(self, event):
		self.newGame()

	def newGame(self):
		self.previousGame = self.game
		self.endOfGame = False

		for piece in self.pieces:
			r, c = self.previousGame.getCurrentPosOfPiece(piece)
			x1 = (c * self.size)
			y1 = (r * self.size)
			x2 = x1 + self.size
			y2 = y1 + self.size
			lastColor = "white" if (r + c) % 2 == 0 else "blue"
			self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
			self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")


		self.game = Game(self.parent)
		self.game.setStartBoard()
		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		for piece in self.pieces:
			self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
			self.resetDrawTakeableMoves(piece, r, c)
			

		self.drawAllPieces()

	def save(self):
		fileName = tkinter.filedialog.askopenfilename()

		if fileName:
			with open(fileName, 'w') as f:
				f.write(self.game.boardToString())

	def open(self):
		fileName = tkinter.filedialog.askopenfilename()
		
		self.previousGame = self.game
		self.game.reset()
		self.endOfGame = False
		self.game = Game(self.parent)

		if fileName:
			with open(fileName, 'r') as f:
				reader = csv.reader(f)
				lists = list(reader)

				for i, l in enumerate(lists):
					for j, p in enumerate(l):
						if p == "P_B":	
							pawn = Pawn(pieceColor.Black)
							self.game.board[i][j] = pawn
							self.game.blackPiecesInGame.append(pawn)
						elif p == "R_B":
							rook = Rook(pieceColor.Black)
							self.game.board[i][j] = rook
							self.game.blackPiecesInGame.append(rook)
						elif p == "B_B":
							bishop = Bishop(pieceColor.Black)
							self.game.board[i][j] = bishop
							self.game.blackPiecesInGame.append(bishop)
						elif p == "KN_B":
							knight = Knight(pieceColor.Black)
							self.game.board[i][j] = knight
							self.game.blackPiecesInGame.append(knight)
						elif p == "Q_B":
							queen = Queen(pieceColor.Black)
							self.game.board[i][j] = queen
							self.game.blackPiecesInGame.append(queen)
						elif p == "K_B":
							king = King(pieceColor.Black)
							self.game.board[i][j] = king
							self.game.blackPiecesInGame.append(king)
						elif p == "P_W":	
							pawn = Pawn(pieceColor.White)
							self.game.board[i][j] = pawn
							self.game.whitePiecesInGame.append(pawn)
						elif p == "R_W":
							rook = Rook(pieceColor.White)
							self.game.board[i][j] = rook
							self.game.whitePiecesInGame.append(rook)
						elif p == "B_W":
							bishop = Bishop(pieceColor.White)
							self.game.board[i][j] = bishop
							self.game.whitePiecesInGame.append(bishop)
						elif p == "KN_W":
							knight = Knight(pieceColor.White)
							self.game.board[i][j] = knight
							self.game.whitePiecesInGame.append(knight)
						elif p == "Q_W":
							queen = Queen(pieceColor.White)
							self.game.board[i][j] = queen
							self.game.whitePiecesInGame.append(queen)
						elif p == "K_W":
							king = King(pieceColor.White)
							self.game.board[i][j] = king
							self.game.whitePiecesInGame.append(king)

		for piece in self.pieces:
			r, c = self.previousGame.getCurrentPosOfPiece(piece)
			x1 = (c * self.size)
			y1 = (r * self.size)
			x2 = x1 + self.size
			y2 = y1 + self.size
			lastColor = "white" if (r + c) % 2 == 0 else "blue"
			self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
			self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		for piece in self.pieces:
			self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
			self.resetDrawTakeableMoves(piece, r, c)

		self.drawAllPieces()
