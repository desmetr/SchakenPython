piece = self.game.getPieceOnPosition((1,3)) # BLACK PAWN
self.game.move(piece, (2,3))

piece = self.game.getPieceOnPosition((6,0)) # WHITE PAWN
self.game.move(piece, (4,0))

piece = self.game.getPieceOnPosition((0,0)) # BLACK ROOK
self.game.move(piece, (7,0))

piece = self.game.getPieceOnPosition((7,0)) # WHITE ROOK
self.game.move(piece, (5,0))

piece = self.game.getPieceOnPosition((0,1)) # BLACK KNIGHT
self.game.move(piece, (2,2))

piece = self.game.getPieceOnPosition((7,6)) # WHITE KNIGHT
self.game.move(piece, (5,7))

piece = self.game.getPieceOnPosition((0,5)) # BLACK BISHOP
self.game.move(piece, (2,3))

piece = self.game.getPieceOnPosition((7,2)) # WHITE BISHOP
self.game.move(piece, (2,7))

piece = self.game.getPieceOnPosition((0,3)) # BLACK QUEEN
self.game.move(piece, (3,0))

piece = self.game.getPieceOnPosition((7,3)) # WHITE QUEEN
self.game.move(piece, (4,0))

piece = self.game.getPieceOnPosition((7,4)) # BLACK KING
self.game.move(piece, (6,5))

piece = self.game.getPieceOnPosition((7,3)) # WHITE KING
self.game.move(piece, (4,0))		