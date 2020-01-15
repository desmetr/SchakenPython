from chessboard import ChessBoard
from chesspiece import *
from game import Game
from tkinter import Tk, Button
import tkinter as tk
from gameboard import GameBoard

class MainWindow():
	def __init__(self):

		# self.master = master
		# master.title("Schaken")
		# gui = BoardGuiTk(master, self.game)
		# gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
		# self.scene = ChessBoard()
		# self.display_moves = QAction(self.tr("&temp"), self)
		# self.display_kills = QAction(self.tr("&temp"), self)
		# self.display_threats = QAction(self.tr("&temp"), self)
		
		root = tk.Tk()
		root.title("Schaken")

		self.game = Game(root)
		self.game.setStartBoard()
		# self.game.setCheckmateBoard()	
		# self.game.setBishopBoard()
		# Black Bishop
		# piece = self.game.getPieceOnPosition((7,5))
		# self.game.move(piece, (5,3))
		
		board = GameBoard(root, self.game)
		board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
		root.mainloop()
		
		# self.game.isCheck(pieceColor.Black)
		# self.game.isCheckmate(pieceColor.Black)
		
		# White Pawn 	on (6,2) 	moves to (4,2)
		# piece = self.game.getPieceOnPosition((6,2))
		# self.game.move(piece, (4,2))

		# Black Pawn 	on (1,7) 	moves to (2,7)
		# piece = self.game.getPieceOnPosition((1,7))
		# self.game.move(piece, (2,7))	
		# White Knight 	on (7,6) 	moves to (5,5)
		# piece = self.game.getPieceOnPosition((7,6))
		# self.game.move(piece, (5,5))	
		# Black Pawn 	on (1,4) 	moves to (2,4)
		# piece = self.game.getPieceOnPosition((1,4))
		# self.game.move(piece, (2,4))	
		# White Queen 	on (7,3)	moves to (4,0)
		# piece = self.game.getPieceOnPosition((7,3))
		# self.game.move(piece, (4,0))	
		# WRONG MOVE: Black Rook on (0,0) moves to (2,0)
		# piece = self.game.getPieceOnPosition((0,0))
		# self.game.move(piece, (0,0)) 
		# Black Bishop 	on (0,5)	moves to (4,1)
		# piece = self.game.getPieceOnPosition((0,5))
		# self.game.move(piece, (4,1))	

		#####################

		# self.view = QGraphicsView(self.scene)
		# self.setCentralWidget(self.view)

		# self.scene.connect(self.clicked)
		# QObject.connect(self.scene, SIGNAL('self.clicked(int,int)'), self, SLOT('self.clicked(int,int)'))

		# self.createActions()
		# self.createMenus()

		
	# Deze functie wordt opgeroepen telkens er op het schaakbord
	# geklikt wordt. x,y geeft de positie aan waar er geklikt
	# werd; r is de 0-based rij, k de 0-based kolom
	def clicked(self, r, k):
		# self.update()
		# Wat hier staat is slechts een voorbeeldje dat wordt afgespeeld ter illustratie.
		# Jouw code zal er helemaal anders uitzien en zal enkel de aanpassing in de spelpositie maken en er voor
		# zorgen dat de visualisatie (al dan niet via update) aangepast wordt.

		# Volgende schaakstukken worden aangemaakt om het voorbeeld te illustreren.
		# In jouw geval zullen de stukken uit game g komen
		p1 = Pawn(pieceColor.Black)
		p2 = Pawn(pieceColor.Black)
		Q = Queen(pieceColor.Black)
		K = King(pieceColor.Black)

		p3 = Pawn(pieceColor.White)
		Kn = Knight(pieceColor.White)
		B = Bishop(pieceColor.White)
		Kw = King(pieceColor.White)

		# self.scene.removeAllMarking() # Alle markeringen weg
		# self.scene.clearBoard()	# Alle stukken weg

		# # plaats alle stukken
		# self.scene.setItem(3, 0, Kn.piece())
		# self.scene.setItem(1, 1, p1.piece())
		# self.scene.setItem(0, 3, Q.piece())
		# self.scene.setItem(0, 4, K.piece())
		# self.scene.setItem(2, 4, p2.piece())
		# self.scene.setItem(3, 3, p3.piece())
		# self.scene.setItem(2, 7, B.piece())
		# self.scene.setItem(5, 3, Kw.piece())

		# if self.display_kills.isChecked():
		# 	# Markeer de stukken die je kan slaan
		# 	scene.setPieceThreat(3, 0, True)
		# 	scene.setPieceThreat(3, 3, True)
		# if self.display_threats.isChecked():
		# 	# Markeer jouw bedreigde stukken
		# 	scene.setPieceThreat(2, 4, True)
		# 	scene.setPieceThreat(1, 1, True)

		# box1 = QMessageBox()
		# box1.setText("Illustratie voor click; zwart is aan de beurt")
		# box1.exec()

		# self.scene.removeAllPieceThreats()  # Eens een stuk gekozen is, worden alle bedreigde stukken niete langer gemarkeerd
		# self.scene.setTileSelect(2, 4, True) # De geselecteerde positie wordt steeds gemarkeerd
		# if self.display_moves.isChecked():
		# 	# Geef de mogelijke zetten weer
		# 	self.scene.setTileFocus(3, 3, True)
		# 	self.scene.setTileFocus(3, 4, True)

		# box1.setText("Illustratie na click; zwart kiest doelpositie")
		# box1.exec()
		# self.scene.clearBoard()
		# self.scene.removeAllMarking()

		# self.scene.setItem(3, 0, Kn.piece())
		# self.scene.setItem(1, 1, p1.piece())
		# self.scene.setItem(0, 3, Q.piece())
		# self.scene.setItem(0, 4, K.piece())
		# self.scene.setItem(2, 7, B.piece())
		# self.scene.setItem(5, 3, Kw.piece())
		# self.scene.setItem(3, 3, p2.piece())

		# if self.display_kills.isChecked():
		# 	self.scene.setPieceThreat(2, 4, True)
		# 	self.scene.setPieceThreat(1, 1, True)
		# if self.display_threats.isChecked():
		# 	self.scene.setPieceThreat(3, 0, True)


		# box1.setText("Illustratie na doelpositie gekozen is; nu is wit aan de beurt")
		# box1.exec()

		# self.scene.removeAllPieceThreats()

		# self.scene.setTileSelect(2, 7, True)
		# if self.display_moves.isChecked():
		# 	for r in range(0, 8):
		# 		if r == 2: 
		# 			continue
		# 		c = 7 - abs(r - 2)
		# 		self.scene.setTileFocus(r, c, True)

		# 	if self.display_threats.isChecked():
		# 		self.scene.setTileThreat(0, 5, True)
		# 		self.scene.setTileThreat(3, 6, True)
		# 		self.scene.setTileThreat(5, 4, True)
		# 		self.scene.setTileThreat(6, 3, True)

		# box1.setText("Wit stuk geselecteerd; wit moet nu een doelpositie kiezen")
		# box1.exec()
		# self.scene.removeAllMarking()
		
	def newGame(self):
		print("IN NEW GAME")

	def save(self):
		fileName = QFileDialog.getSaveFileName(self, tr("Save game"), "", tr("Chess File (*.chs);;All Files (*)"))

		if fileName.isEmpty():
			return
		else:
			file = QFile(fileName)
			if not file.open(QIODevice.WriteOnly):
				QMessageBox.information(self, tr("Unable to open file"), file.errorString())
				return

			out = QDataStream(file)
			out.writeQString("Rb")
			out.writeQString("Hb")
			out.writeQString("Bb")
			out.writeQString("Qb")
			out.writeQString("Kb")
			out.writeQString("Bb")
			out.writeQString("Hb")
			out.writeQString("Rb")
			for i in range(0, 8):
				out.writeQString("Pb")
			for r in range(3, 7):
				for k in range(0, 8):
					out.writeQString(".")
			for i in range(0, 8):
				out.writeQString("Pw")
			out.writeQString("Rw")
			out.writeQString("Hw")
			out.writeQString("Bw")
			out.writeQString("Qw")
			out.writeQString("Kw")
			out.writeQString("Bw")
			out.writeQString("Hw")
			out.writeQString("Rw")

	def open(self):
		fileName = QFileDialog.getOpenFileName(self, tr("Load game"), "", tr("Chess File (*.chs);;All Files (*)"))
		
		if fileName.isEmpty():
			return
		else:
			file = QFile(fileName)

			if not file.open(QIODevice.ReadOnly):
				QMessageBox.information(self, tr("Unable to open file"), file.errorString())
				return

			try:
				in_ = QDataStream(file)
				debugstring = ""
				for r in range(0, 8):
					for k in range(0, 8):
						piece = ""
						in_.readQString(piece)
						debugstring += "\t" + piece
						if in_.status() != QDataStream.Ok:
							raise QString("Error reading file " + fileName)
					debugstring += "\n"
				QMessageBox.information(self, tr("Debug"), debugstring)
			except (QString& Q):
				QMessageBox.information(self, tr("Error reading file"), Q)
		self.update();

	def undo(self):
		box = QMessageBox()
		box.setText(QString("Je hebt undo gekozen"))
		box.exec()

	def redo(self):
		pass

	def visualizationChange(self):
		box = QMessageBox()
		visstring = QString("T" if display_moves.isChecked() else "F") + ("T"if display_kills.isChecked() else "F") + ("T" if display_threats.isChecked() else "F")
		box.setText(QString("Visualization changed : ") + visstring)
		box.exec()


	# Update de inhoud van de grafische weergave van het schaakbord (scene)
	# en maak het consistent met de game state in variabele g.
	def update(self):
		for i in range(0, 8):
			for j in range(0, 8):
				self.scene.setItem(i, j, self.game.getPieceOnPosition(i, j))

	def createActions(self):
		self.newAct = QAction(self.tr("&New"), self)
		self.newAct.setShortcuts(QKeySequence.New)
		self.newAct.setStatusTip(self.tr("Start a new game"))
		self.newAct.triggered.connect(self.newGame)
		# QObject.connect(self.newAct, QAction.triggered, self, 'self.newGame()')

		self.openAct = QAction(self.tr("&Open"), self)
		self.openAct.setShortcuts(QKeySequence.Open)
		self.openAct.setStatusTip(self.tr("Read game from disk"))
		self.openAct.triggered.connect(self.open)
		# QObject.connect(openAct, QAction.triggered, self, MainWindow.open)

		self.saveAct = QAction(self.tr("&Save"), self)
		self.saveAct.setShortcuts(QKeySequence.Save)
		self.saveAct.setStatusTip(self.tr("Save game to disk"))
		self.saveAct.triggered.connect(self.save)
		# QObject.connect(saveAct, QAction.triggered, self, MainWindow.save)

		self.exitAct = QAction(self.tr("&Exit"), self)
		self.exitAct.setShortcuts(QKeySequence.Quit)
		self.exitAct.setStatusTip(self.tr("Abandon game"))
		self.exitAct.triggered.connect(self.on_actionExit_triggered)
		# QObject.connect(exitAct, QAction.triggered, self, MainWindow.on_actionExit_triggered)

		self.undoAct = QAction(self.tr("&Undo"), self)
		self.undoAct.setShortcuts(QKeySequence.Undo)
		self.undoAct.setStatusTip(self.tr("Undo last move"))
		self.undoAct.triggered.connect(self.undo)
		# QObject.connect(undoAct, QAction.triggered, self, MainWindow.undo)

		self.redoAct = QAction(self.tr("&redo"), self)
		self.redoAct.setShortcuts(QKeySequence.Redo)
		self.redoAct.setStatusTip(self.tr("Redo last undone move"))
		self.redoAct.triggered.connect(self.redo)
		# QObject.connect(redoAct, QAction.triggered, self, MainWindow.redo)

		self.display_moves = QAction(self.tr("&valid moves"), self)
		self.display_moves.setStatusTip(self.tr("Show valid moves"))
		self.display_moves.setCheckable(True)
		self.display_moves.setChecked(True)
		self.display_moves.triggered.connect(self.visualizationChange)
		# QObject.connect(display_moves, QAction.triggered, self, MainWindow.visualizationChange)

		self.display_kills = QAction(self.tr("threathed &enemy"), self)
		self.display_kills.setStatusTip(self.tr("Highlight threathened pieces (enemy)"))
		self.display_kills.setCheckable(True)
		self.display_kills.setChecked(True)
		self.display_kills.triggered.connect(self.visualizationChange)
		# QObject.connect(display_kills, QAction.triggered, self, MainWindow.visualizationChange)

		self.display_threats = QAction(self.tr("threathed &player"), self)
		self.display_threats.setStatusTip(self.tr("Highlight threathened pieces (player)"))
		self.display_threats.setCheckable(True)
		self.display_threats.setChecked(True)
		self.display_threats.triggered.connect(self.visualizationChange)
		# QObject.connect(display_threats, QAction.triggered, self, MainWindow.visualizationChange)

	def createMenus(self):
		fileMenu = QMenuBar()
		fileMenu.addMenu(self.tr("&File"))
		fileMenu.addAction(self.newAct)
		fileMenu.addAction(self.openAct)
		fileMenu.addAction(self.saveAct)
		fileMenu.addAction(self.exitAct)
		# self.scene.addWidget(fileMenu, 0, 0, 1, 1)
		
		gameMenu = QMenuBar()
		gameMenu.addMenu(self.tr("&Game"))
		gameMenu.addAction(self.undoAct)
		gameMenu.addAction(self.redoAct)
		# self.scene.addWidget(gameMenu, 0, 0, 1, 2)
		
		visualizeMenu = QMenuBar()
		visualizeMenu.addMenu(self.tr("&Visualize"))
		visualizeMenu.addAction(self.display_moves)
		visualizeMenu.addAction(self.display_kills)
		visualizeMenu.addAction(self.display_threats)
		# self.scene.addWidget(visualizeMenu, 0, 0, 1, 3)
	
	def on_actionExit_triggered(self):
		if QMessageBox.Yes == QMessageBox.question(self, self.tr("Spel verlaten"), self.tr("Bent u zeker dat u het spel wil verlaten?\nNiet opgeslagen wijzigingen gaan verloren.")):
			QApplication.quit()
