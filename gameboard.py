import tkinter as tk
from tkinter import *
from math import floor
import mainwindow
class GameBoard(tk.Frame):
	def __init__(self, parent, game, rows=8, columns=8, size=64, color1="white", color2="blue"):
		'''size is the size of a square, in pixels'''

		self.game = game
		self.rows = rows
		self.columns = columns
		self.size = size
		self.color1 = color1
		self.color2 = color2
		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		self.previousPiece = None
		self.imagesBoard = [[None] * 8 for i in range(8)]

		for piece in self.pieces:
			piece.setImage()

		canvas_width = columns * size
		canvas_height = rows * size

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
								width=canvas_width, height=canvas_height, background="bisque")
		self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

		for piece in self.pieces:
			r, c = self.game.getCurrentPosOfPiece(piece)
			self.imagesBoard[r][c] = self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image)

		# this binding will cause a refresh if the user interactively
		# changes the window size
		self.canvas.bind("<Configure>", self.refresh)
		self.canvas.bind("<Button-1>", self.click)

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

		lastColor = "white" if r % 2 == 0 and c % 2 == 0 else "blue"
		if self.previousPiece:
			self.game.move(self.previousPiece, (r,c))	

			# self.previousPiece = piece
			# self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
			self.previousPiece = None
		elif piece.selected:
			piece.selected = False
			self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=lastColor, tags="square")
		else:
			piece.selected = True
			self.previousPiece = piece
			self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green", tags="square")
		# self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image)
		# print(piece)

		# if not isinstance(piece, NoType):
		# 	self.game.move(self.selected_piece[1], position)
		# 	self.selected_piece = None
		# 	self.hilighted = None
		# 	self.pieces = {}
		# 	self.refresh()
		# 	self.draw_pieces()

		# self.hilight(position)
		# self.refresh()
		
		for image in self.imagesBoard:
			# r, c = self.game.getCurrentPosOfPiece(piece)
			self.canvas.delete(image)

		self.pieces = self.game.blackPiecesInGame + self.game.whitePiecesInGame
		for piece in self.pieces:
			r, c = self.game.getCurrentPosOfPiece(piece)
			# self.canvas.delete(self.imagesBoard[r][c])
			# print(r,c)
			self.canvas.create_image(c * self.size, r * self.size, anchor=NW, image=piece.image)

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
