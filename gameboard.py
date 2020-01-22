import tkinter as tk
from tkinter import *
from math import floor
from chesspiece import *
from tkinter import *
from game import Game
import mainwindow

class GameBoard(tk.Frame):
	def __init__(self, parent, game, rows=8, columns=8, size=64, color1="white", color2="blue"):
		'''size is the size of a square, in pixels'''
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
		self.blackPiecesListbox = Listbox(self.parent)
		self.whitePiecesListbox = Listbox(self.parent)

		for piece in self.pieces:
			piece.setImage()

		canvas_width = columns * size
		canvas_height = rows * size

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
								width=canvas_width, height=canvas_height, background="bisque")
		
		# self.blackPiecesListbox.place(x=0, y=0)
		# self.whitePiecesListbox.place(x=0, y=1)
		self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
		# self.blackPiecesListbox.pack()
		# self.whitePiecesListbox.pack()

		self.menubar = Menu(self.parent)
		self.menubar.add_command(label="New", command=self.newGame)
		self.menubar.add_command(label="Quit", command=self.parent.quit)
		# self.menubar.add_command(label="Black Pieces", command=self.getTakenBlackPieces())
		# self.menubar.add_command(label="White Pieces", command=self.getTakenWhitePieces())
		self.parent.config(menu=self.menubar)

		self.drawAllPieces()

		# this binding will cause a refresh if the user interactively
		# changes the window size
		self.canvas.bind("<Configure>", self.refresh)
		self.canvas.bind("<Button-1>", self.click)

	def drawAllPieces(self):
		self.canvas.delete("image")
		for piece in self.pieces:
			r, c = self.game.getCurrentPosOfPiece(piece)
			self.imagesBoard[r][c] = self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

	def click(self, event):
		# Figure out which square we've clicked
		col_size = row_size = event.widget.master.size

		c = floor(event.x / col_size)
		r = floor(event.y / row_size)
		piece = self.game.getPieceOnPosition((r, c))
		x1 = (c * self.size)
		y1 = (r * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size

		lastColor = "white" if (r + c) % 2 == 0 else "blue"

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

					self.firstClick = False
			else:	
				if self.previousPiece != piece:
					print("A")
					prevR, prevC = self.game.getCurrentPosOfPiece(self.previousPiece)
					prevX1 = (prevC * self.size)
					prevY1 = (prevR * self.size)
					prevX2 = prevX1 + self.size
					prevY2 = prevY1 + self.size

					if (prevR, prevC) != (r,c):
						prevLastColor = "white" if (prevR + prevC) % 2 == 0 else "blue"
						self.resetDrawLegalMovesAndNotBlockedInPath(self.previousPiece, prevR, prevC)
						self.resetDrawTakeableMoves(self.previousPiece, prevR, prevC)
						if self.game.move(self.previousPiece, (r,c)):
							print("B")
							self.whiteTurn = not self.whiteTurn
							# self.canvas.delete(self.imagesBoard[prevR][prevC])
							self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
							self.canvas.create_rectangle(prevX1, prevY1, prevX2, prevY2, outline="black", fill=prevLastColor, tags="square")
							# self.canvas.delete("image")
							self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=self.previousPiece.image, tags="image")
							self.drawAllPieces()
							# self.imagesBoard[prevR][prevC] = None
						else:
							print("C")
							self.canvas.create_rectangle(prevX1, prevY1, prevX2, prevY2, outline="black", fill=prevLastColor, tags="square")
							self.canvas.create_image(prevC * self.size, prevR * self.size, anchor=NW, image=self.previousPiece.image, tags="image")

							self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
							self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

						self.previousPiece.selected = False
					else:
						print("D")
						self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
						self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

					self.previousPiece = None

				elif self.previousPiece == piece:
					print("E")
					piece.selected = False
					self.previousPiece = None
					self.resetDrawLegalMovesAndNotBlockedInPath(piece, r, c)
					self.resetDrawTakeableMoves(piece, r, c)
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")


				elif not piece.selected:
					print("F")
					piece.selected = True
					if not isinstance(piece, NoType):
						self.previousPiece = piece
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green", tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")
				else:
					print("G")
					piece.selected = False
					if not isinstance(piece, NoType):
						self.previousPiece = piece
					self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
					self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image, tags="image")

				self.firstClick = True
			print(piece)

		# See if check or checkmate
		# self.game.isCheckmate(pieceColor.Black)
		# self.game.isCheckmate(pieceColor.White)
		# blackIsCheck = self.game.isCheck(pieceColor.Black)
		# whiteIsCheck = self.game.isCheck(pieceColor.White)
		# if blackIsCheck or whiteIsCheck:
		# 	color = "Black"
		# 	if whiteIsCheck: color = "White" 
		# 	return messagebox.showinfo("Chess", color + " is in chess!")

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

	def getTakenBlackPieces(self):
		for piece in self.game.takenBlackPieces:
			if piece not in self.blackPiecesListbox:
				self.blackPiecesListbox.insert(END, piece)

	def getTakenWhitePieces(self):
		for piece in self.game.takenWhitePieces:
			if piece not in self.whitePiecesListbox:
				self.whitePiecesListbox.insert(END, piece)

	def refresh(self, event):
		'''Redraw the board, possibly in response to window being resized'''
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

	# def addpiece(self, name, image, row=0, column=0):
	# 	'''Add a piece to the playing board'''
	# 	self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
	# 	self.placepiece(name, row, column)

	def placepiece(self, name, row, column):
		'''Place a piece at the given row/column'''
		# self.pieces[name] = (row, column)
		x0 = (column * self.size) + int(self.size/2)
		y0 = (row * self.size) + int(self.size/2)
		self.canvas.coords(name, x0, y0)

	def newGame(self):
		self.previousGame = self.game
		self.game = Game(self.parent)
		self.game.setStartBoard()
		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		for piece in self.pieces:
			piece.setImage()
		self.drawAllPieces()
