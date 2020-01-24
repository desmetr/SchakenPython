from enums import *
from chesspiece import *
from game import Game
from tkinter import Tk, Button
import tkinter as tk
from gameboard import GameBoard

class MainWindow():
	def __init__(self):
		root = tk.Tk()
		root.title("Schaken")

		self.game = Game(root)
		self.game.setStartBoard()
		# self.game.setEnPassantBoard()
		# self.game.setRokadeBoard()
		# self.game.setCheckBoard()	
		# self.game.setCheckmateBoard()	
		# self.game.setPawnBoard()
		# self.game.setRookBoard()
		# self.game.setKnightBoard()
		# self.game.setBishopBoard()
		# self.game.setQueenBoard()
		# self.game.setKingBoard()
		# self.game.setPromoteBoard()

		board = GameBoard(root, self.game)
		board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
		root.mainloop()

		# for piece in self.game.whitePiecesInGame + self.game.blackPiecesInGame:
		# for piece in self.game.blackPiecesInGame:
		# for piece in self.game.whitePiecesInGame:
			# if isinstance(piece, Rook):
			# 	print("--------")
			# r,c = self.game.getCurrentPosOfPiece(piece)
			# print("(r,c)=",(r,c))
			# print("possibleMoves=", piece.possibleMoves(r,c))
			# print("legalMovesAndNotBlockedInPath=", piece.legalMovesAndNotBlockedInPath((r,c), None, self.game.board))
			# print("takeableMoves=", piece.takeableMoves((r,c), None, self.game.board))