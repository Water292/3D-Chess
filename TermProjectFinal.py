#abhasin1 
#Aayush Bhasin
#Section E
#Term Project

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random
#All the chess piece images and the backgrounds are not my original work, 
#the creators have been attributed right above where these have been created.
#http://creativecommons.org/licenses/by/4.0/legalcode
#All files have been unaltered besides a change in size and conversion to .gif
#Only the images used for check have been modified to include "CHECK" as text
#The use of any of these picturs has not been endorsed by the creators

class Animation(object):
    # Override these methods when creating your own animation
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    
    # Call app.run(width,height) to get your app started
    def run(self, width=300, height=300):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()

        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
            self.canvas.update()

        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()

        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()

        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)

        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
            
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()
        print("Bye")

class Chess(Animation):

    def mousePressed(self, event):
        if self.mode == "SplashScreen":
            self.SplashScreenmousePressed(event)
        if self.mode == "Chess":
            self.ChessmousePressed(event)

    def keyPressed(self, event):
        if self.mode == "SplashScreen":
            self.SplashScreenkeyPressed(event)
        if self.mode == "Chess":
            self.ChesskeyPressed(event)

    def timerFired(self):
        if self.mode == "SplashScreen":
            self.SplashScreentimerFired()
        if self.mode == "Chess":
            self.ChesstimerFired()

    def redrawAll(self):
        if self.mode == "SplashScreen":
            self.SplashScreenredrawAll()
        if self.mode == "Chess":
            self.ChessredrawAll()

    def SplashScreenmousePressed(self, event):
        if self.splashPlayButton.containsPoint(event.x, event.y):
            self.mode = "Chess"

    def SplashScreenkeyPressed(self, event):
        if event.keysym == "p" or event.keysym == "P":
            self.mode = "Chess"

    def SplashScreentimerFired(self):
        pass

    def SplashScreenredrawAll(self):
        self.canvas.create_image(self.width/2, self.height/2, 
                image = self.background)
        self.canvas.create_image(self.width/2, self.height/2, 
                image = self.splashPhoto)
        self.splashPlayButton.draw(self)
        extraGap = 30
        self.canvas.create_text(self.width/2, self.height/2 + extraGap, text =
            "It doesn't matter who we are...", 
            fill = "white", font = "Calibiri 30")
        gap = 40
        self.canvas.create_text(self.width/2, self.height/2 + extraGap + gap, 
            text = "what matters is our plan.", 
            fill = "white", font = "Calibiri 30")
        Ypos = 2*self.height/5
        self.canvas.create_image(self.width/2, Ypos, image = self.title)


    def init(self):
        filename = "Title.gif"
        self.title = PhotoImage(file = filename)
        self.mode = "SplashScreen"
        filename =  "knightBG.gif"
        #https://pixabay.com/p-147065/?no_redirect
        #public domain
        self.splashPhoto = PhotoImage(file = filename)
        #http://www.freestockphotos.biz/stockphoto/9090
        #By Petr Kratochvil
        self.background = PhotoImage(file = "Blue.gif").zoom(2,2)
        #the photo's used to indicate Check
#https://pixabay.com/static/uploads/photo/2013/07/12/13/27/knight-147065_640.png
        self.whiteCheck = PhotoImage(file = "Checkwhite.gif").subsample(3,3)
#https://pixabay.com/static/uploads/photo/2013/07/12/13/27/knight-147065_640.png
        self.blackCheck = PhotoImage(file = "Checkblack.gif").subsample(3,3)
        #initializing boards with initial positions 
        Ypos = 5*self.height/6
        Xpos = self.width/12
        sizeX, sizeY = 200, 50
        self.splashPlayButton = Button("PLAY", Xpos, Ypos, sizeX, sizeY)
        self.whiteBoard = Board(0,1)
        self.neutralBoard = Board(2,3)
        self.blackBoard = Board(4,5)
        self.white1 = MovableBoard(self.whiteBoard, 0, 0)
        self.white2 = MovableBoard(self.whiteBoard, 0, 4)
        self.black1 = MovableBoard(self.blackBoard, 4, 0)
        self.black2 = MovableBoard(self.blackBoard, 4, 4)
        self.boards = [self.whiteBoard, self.neutralBoard, self.blackBoard, 
                        self.white1, self.white2, self.black1, self.black2]
        self.movableBoards = [self.white1, self.white2, self.black1,self.black2]
        self.fixedBoards = [self.whiteBoard, self.neutralBoard, self.blackBoard]
        #initializing all the buttons at their positions
        self.margin = 20
        tutorialButtonX, tutorialButtonY = 20, 150
        tutorialButtonWidth = 160
        tutorialButtonHeight = 30
        self.tutorialButton = Button("TUTORIAL MODE", tutorialButtonX, 
                    tutorialButtonY, tutorialButtonWidth, tutorialButtonHeight)
        (restartButtonX, restartButtonY) = (tutorialButtonX, 
                                tutorialButtonY + tutorialButtonHeight + 20)
        (restartButtonWidth, restartButtonHeight) = (tutorialButtonWidth, 
                                                    tutorialButtonHeight)
        self.restartButton = Button("RESTART", restartButtonX, restartButtonY,
                        restartButtonWidth, restartButtonHeight)
        (helpButtonX, helpButtonY) = (restartButtonX, 
                                restartButtonY + restartButtonHeight + 20)
        (helpButtonWidth, helpButtonHeight) = (restartButtonWidth, 
                                                    restartButtonHeight)
        self.helpButton = Button("INSTRUCTIONS", helpButtonX, helpButtonY,
                        helpButtonWidth, helpButtonHeight)
        (AIButtonX, AIButtonY) = (helpButtonX, 
                                helpButtonY + helpButtonHeight + 20)
        (AIButtonWidth, AIButtonHeight) = (helpButtonWidth, 
                                                    helpButtonHeight)
        self.AIButton = Button("AI", AIButtonX, AIButtonY,
                        AIButtonWidth, AIButtonHeight)
        self.buttons = [self.tutorialButton, self.restartButton, 
                        self.helpButton, self.AIButton]
        self.time = 0 #timer so that AI doesn't move instantaneously 
        self.lastPiece = None #keep last move highlighted for clarity
        self.isGameOver = None
        #place pieces on the board 
        pawnRowWhite, pawnRowBlack = 1, 2
        movablePawnRowWhite, movablePawnRowBlack = 1, 0
        pieceRowWhite, pieceRowBlack = 0, 3
        movablePieceRowWhite, movablePieceRowBlack = 0, 1
        self.wGap = self.width/12
        self.hGap = self.height/40
        fixedRows = fixedCols = len(self.whiteBoard.board)
        movableRows = movableCols = len(self.white1.board)
        #game states
        self.selectedPiece = None
        self.selectedBoard = None
        self.checked = False 
        #To display dead pieces
        trashCenter = 3*self.margin
        trashHeightMargin = 15*self.margin
        self.trashCans = [TrashCan(self.width - trashCenter, 
            self.height- trashHeightMargin, self, "white"), 
            TrashCan(self.width - trashCenter, 
            self.height-self.margin, self, "black")]
        pieceOrder = (Knight, Bishop, Bishop, Knight)
        self.turn = "white"
        pieceOrderMovable1 = (Rook, Queen)
        pieceOrderMovable2 = (King, Rook)
        for col in range(fixedCols):
            self.whiteBoard.board[pawnRowWhite][col] = Pawn("white", self)
            self.blackBoard.board[pawnRowBlack][col] = Pawn("black", self)
            piece = pieceOrder[col]
            self.whiteBoard.board[pieceRowWhite][col] = piece("white", self)
            self.blackBoard.board[pieceRowBlack][col] = piece("black", self)
        for col in range(movableCols):
            self.white1.board[movablePawnRowWhite][col] = Pawn("white", self)
            self.white2.board[movablePawnRowWhite][col] = Pawn("white", self)
            self.black1.board[movablePawnRowBlack][col] = Pawn("black", self)
            self.black2.board[movablePawnRowBlack][col] = Pawn("black", self)
            piece = pieceOrderMovable1[col]
            self.white1.board[movablePieceRowWhite][col] = piece("white", self)
            self.black1.board[movablePieceRowBlack][col] = piece("black", self)
            piece = pieceOrderMovable2[col]
            self.white2.board[movablePieceRowWhite][col] = piece("white", self)
            self.black2.board[movablePieceRowBlack][col] = piece("black", self)
        
        #keep track of pieces on and off the board
        self.whitePieces, self.blackPieces = [], []
        self.removedPiecesWhite, self.removedPiecesBlack = [], []
        for board in self.boards:
            for row in range(len(board.board)):
                for col in range(len(board.board[row])):
                    piece = board.board[row][col]
                    if piece != None: 
                        if piece.color == "white":
                            self.whitePieces.append(piece)
                        elif piece.color == "black":
                                self.blackPieces.append(piece)

    def ChessmousePressed(self, event):
        #movement of attack boards
        if self.findMovableBoard(event) != None:
            self.selectedBoard = self.findMovableBoard(event)
        elif self.selectedBoard != None:
            if self.findRowAndCol(event) != None:
                (row, col, board) = self.findRowAndCol(event)
                if self.selectedBoard.isLegal(row, col, board, self):
                    self.selectedBoard.moveBoard(row, col, board, self)
                    self.isChecked()
            else:
                self.selectedBoard = None
        #selecting a piece
        elif self.findRowAndCol(event) != None:
            (row, col, board) = self.findRowAndCol(event)
            piece = board.board[row][col]
            #making sure  the player who's turn it is selects a piece
            if (self.selectedPiece == None and self.selectedBoard == None and 
                piece != None and piece.color == self.turn):
                self.selectedPiece = piece
                self.selectedPiece.row, self.selectedPiece.col = row, col 
                self.selectedPiece.board = board
            elif self.selectedPiece != None:
                #moving a piece only if the move is valid 
                if (self.selectedPiece.isLegal(row, col, board, self) and
                (piece == None or self.selectedPiece.color != piece.color)):
                    self.selectedPiece.move(board, row, col, self)
                    #if a piece is killed, make changes in the lists keeping 
                    #track of the pieces
                    if piece != None and self.checked == False:
                        if piece.color == "white":
                            self.whitePieces.remove(piece)
                            self.removedPiecesWhite.append(piece)
                        elif piece.color == "black":
                            self.blackPieces.remove(piece)
                            self.removedPiecesBlack.append(piece)
                    #see if the move resulted in a check
                    self.isChecked()
                    if self.checked == True:
                        #if yes check if the king is in checkmate
                        self.checkmate()
                    #otherwise check if the game is in stalemate
                    else:
                        self.stalemate()
        #check if the menu buttons are clicked, and if yes, act accordingly
        elif self.tutorialButton.containsPoint(event.x, event.y):
            self.tutorialButton.selected = not(self.tutorialButton.selected)
        elif self.helpButton.containsPoint(event.x, event.y):
            helpWidth, helpHeight = 800, 500
            HelpMenu.run(helpWidth,helpHeight)
        elif self.restartButton.containsPoint(event.x, event.y):
            answer = messagebox.askyesno("Warning", 
                            "Are you sure you want to restart?")
            if answer == True:
                self.init()
        elif self.AIButton.containsPoint(event.x, event.y):
            self.AIButton.selected = not(self.AIButton.selected)
        else: #any click outside deselects a piece
            self.selectedPiece = None

    def ChesskeyPressed(self, event): 
        #keyboard shortcuts for menu buttons
        if event.keysym == "r":
            answer = messagebox.askyesno("Warning", 
                                "Are you sure you want to restart?")
            if answer == True:
                self.init()
        if event.keysym == "t":
            self.tutorialButton.selected = not(self.tutorialButton.selected)
        if event.keysym == "i":
            helpWidth, helpHeight = 800, 500
            HelpMenu.run(helpWidth,helpHeight)
        if event.keysym == "a":
            self.AIButton.selected = not(self.AIButton.selected)

    def ChesstimerFired(self): 
        #if AI is enabled, the computer plays as black
        if self.AIButton.selected == True:
            pieceIndex, boardIndex, rowIndex, colIndex = 0, 1, 2, 3
            #finds the best move for the AI and if it's a tie, chooses a 
            #random one
            if self.turn == "black":
                self.time += 1 
                possibleMoves = self.listMoves()
                if self.isGameOver != None:
                    return 
                elif len(possibleMoves) == 0: 
                    self.isGameOver = "stalemate"
                    return
                bestMoves = self.lowestCost(possibleMoves)
                move = random.choice(bestMoves)
                #move is a tuple containing info needed to make the move
                piece, board = move[pieceIndex], move[boardIndex]
                row, col = move[rowIndex], move[colIndex]
                if self.time % 4 == 0: #takes a second before every move
                    otherPiece = board.board[row][col]
                    #move the piece
                    piece.move(board, row, col, self)
                    #update the lists keeping track of the pieces
                    if otherPiece != None and self.checked == False:
                        if otherPiece.color == "white":
                            self.whitePieces.remove(otherPiece)
                            self.removedPiecesWhite.append(otherPiece)
                        elif otherPiece.color == "black":
                            self.blackPieces.remove(otherPiece)
                            self.removedPiecesBlack.append(otherPiece)
                    #check if the move results in a check and then for 
                    #checkmate and stalemate
                    self.isChecked()
                    if self.checked == True:
                        self.checkmate()
                    else:
                        self.stalemate()
                    self.time = 0

        

    def ChessredrawAll(self):
        #background
        self.canvas.create_image(self.width/2, self.height/2, 
                                image = self.background)
        #draw boards in the correct order for overlaps to be visually accurate
        #The boards furthest away from the user are drawn first and the closer
        #ones on top
        self.boards.sort(key = lambda x: x.start, reverse = True)

        for board in self.boards:
            board.draw(self)
            if (board == self.whiteBoard or board == self.neutralBoard):
                board.drawLines(self) 
                #lines are used to display the overlap of boards
        for trashCan in self.trashCans:
            trashCan.draw(self)
        self.createTitleBar()

        for button in self.buttons:
            button.draw(self)
        if self.isGameOver != None:
            #On a checkmate or stalemate
            self.canvas.create_text(self.width/2, self.height/2, 
                    text = self.isGameOver.upper(), font = "Arial 50")


    def findRowAndCol(self, event):
        #find out the row and col that was clicked. The col is found using 
        #a linear equation as the col at a particular x coordinate changes
        #with respect to the y value at that point.
        heightMargin = 6*self.hGap
        for board in self.fixedBoards:
            (y2, y1) = (self.height - self.margin - board.height*heightMargin,
                self.height - self.margin - (board.height*heightMargin) - 
                board.rows*self.hGap)
            (x1, x2) = (-self.wGap/2*(event.y-y2)/self.hGap + self.margin + 
                    (board.start/2 + 1)*self.wGap, -self.wGap/2*(event.y-y2)/
                    self.hGap + self.margin + (board.start/2 + 1 + 
                    board.rows)*self.wGap)
            #hgap and wgap are the spaceing between rows and cols respectively
            if y1 < event.y < y2:
                if x1 < event.x < x2:
                    row = int((event.y - y2)*(-1)/self.hGap)
                    col = int((event.x -x1)/self.wGap) 
                    return (row, col, board)
        else: 
            #check the same for movable boards
            for board in self.movableBoards:
                (y1, y2) = (self.height-self.margin-board.height*heightMargin 
                        - (board.start - board.fixedBoard.start + 2)*self.hGap, 
                        self.height - self.margin - board.height*heightMargin
                        - (board.start - board.fixedBoard.start)*self.hGap)
                (x1, x2) = (-self.wGap/2*(event.y - y2)/self.hGap + self.margin 
                        + (board.colStart + board.start/2)*self.wGap,
                        -self.wGap/2*(event.y - y2)/self.hGap + self.margin +
                        (board.colStart + board.start/2 + 2)*self.wGap)
                if y1 < event.y < y2:
                    if x1 < event.x < x2:
                        row = int((event.y - y2)*(-1)/self.hGap)
                        col = int((event.x - x1)/self.wGap)
                        return(row, col, board)
        
    def findMovableBoard(self, event):
        #to see if a player clicked on the movable/attack board itself
        if self.selectedBoard == None and self.selectedPiece == None:
            for board in self.movableBoards:
                if board.isSelected(event.x, event.y):
                    return board

    def isChecked(self):
        #find the position of the king
        for board in self.boards: 
            for row in range(board.rows):
                for col in range(board.cols):
                    piece = board.board[row][col]
                    if isinstance(piece, King) and piece.color == self.turn:
                        kingRow, kingCol, kingBoard = row, col, board
        for board in self.boards: 
            #check if any piece of the opposing color can kill the king
            for row in range(board.rows):
                for col in range(board.cols):
                    piece = board.board[row][col]
                    if piece != None and piece.color != self.turn:
                        piece.row, piece.col, piece.board = row, col, board
                        if piece.isLegal(kingRow, kingCol, kingBoard, self):
                            self.checked = True
                            return
        self.checked = False

    def checkmate(self):
        #if no possible move can be made, only called if the king is checked
        possibleMoves = self.listMoves()
        if len(possibleMoves) == 0:
            self.isGameOver = "checkmate"
            return True
        else:
            return False
            

    def stalemate(self):
        #if no possible move can be made and the king is not checked
        possibleMoves = self.listMoves()
        if len(possibleMoves) == 0:
            self.isGameOver == "stalemate"
            return True
        else:
            return False

    def listMoves(self):
        #for every piece check if it can legally move to a spot on the board
        possibleMoves = list()
        pieces = self.whitePieces if self.turn == "white" else self.blackPieces
        for piece in pieces:
            for board in self.boards:
                for row in range(board.rows):
                    for col in range(board.cols):
                        if piece.isLegal(row, col, board, self):
        #move a pseudolegal move - that which is legal if check is not taken 
        #into account. Then if doesn't result in a check, add it to the list
        #of possible moves
                            piece.move(board, row, col, self, trial = True)
                            #trial makes sure the move is undone after testing
                            otherPiece = board.board[row][col]
                            if self.checked == False:
                            #calculate the cost of a move(useful for AI)
                                cost = self.calculateCost(piece, otherPiece)
                                #store the move as tuple of information
                                currentMove = (piece, board, row, col, cost)
                                possibleMoves.append(currentMove)
        self.isChecked()
        return possibleMoves

    def calculateCost(self, piece, otherPiece):
        #each piece has a value associated with it, so it calculates the 
        #returns the value of the piece killed or none if no piece is killed
        if otherPiece == None:
            return 0
        if otherPiece.color != piece.color: 
            return -otherPiece.points 
        else:
            return otherPiece.points

    def lowestCost(self, possibleMoves):
        #for every possible move, calculate the cost of that move minus the 
        #best move of the opponent corresponding to that move
        pieceIndex, boardIndex, rowIndex, colIndex = 0, 1, 2, 3
        costIndex = 4
        bestCost = None
        bestMoves = []
        for i in range(len(possibleMoves)):
            #calculate cost of current move
            currentMove = possibleMoves[i]
            cost = currentMove[costIndex]
            piece, board = currentMove[pieceIndex], currentMove[boardIndex]
            row, col = currentMove[rowIndex], currentMove[colIndex]
            self.turn = "black"
            piece.move(board, row, col, self)
            self.isChecked()
            if self.checked == True: #incentive to check
                if self.checkmate() == True: #always make a checkmate move 
                    return
            possibleMovesWhite = self.listMoves()
            bestNewCost = None
            for j in range(len(possibleMovesWhite)): #calculate opponents cost
                nextMove = possibleMovesWhite[j]
                newCost = nextMove[costIndex]
                if bestNewCost == None or newCost < bestNewCost:
                    bestNewCost = newCost 
            #subtract it from cost to get the cost over 2 moves
            totalCost = cost - bestNewCost if bestNewCost != None else cost
            if bestCost == None or totalCost < bestCost:
                bestCost = totalCost
                bestMoves = [currentMove]
            elif totalCost == bestCost:
                bestMoves.append(currentMove)
            piece.undoMove(row, col, board)
            #take the board back to the original state
            self.turn = "black"
            self.isChecked()
        return bestMoves 
        
    def createTitleBar(self):
        #The tile bar shows the player name and the relative strength of each
        #player based on remaining pieces
        x = y = 20
        height = 30
        margin = 10
        totalWidth = 240
        whitePoints = self.getWhitePoints()
        blackPoints = self.getBlackPoints()
        whiteWidth = totalWidth*whitePoints/(whitePoints + blackPoints)
        #relative strength
        color1 = "white" if self.turn == "black" else "red"
        color2 = "black" if self.turn == "white" else "red"
        #The player who's turn it is, is displayed in red
        self.canvas.create_rectangle(x, y, x + totalWidth, y + height)
        self.canvas.create_rectangle(x, y, x + whiteWidth, y + height,
                                    width = 0, fill = "thistle4")
        self.canvas.create_rectangle(x + whiteWidth, y, x + totalWidth, 
                        y + height, width = 0, fill = "thistle3")
        self.canvas.create_text(x + margin, y + height/2, 
                        fill = color1, text = "Player W", anchor = W)
        self.canvas.create_text(x + totalWidth - margin, y + height/2, 
                        fill = color2, text = "Player B", anchor = E)
        if self.checked == True:
        #image of the knight taken from:
        #https://pixabay.com/en/knight-black-chess-figure-game-147065/
        #modified to include the "CHECK"
            img = self.whiteCheck if self.turn == "white" else self.blackCheck
            self.canvas.create_image(x + totalWidth/2, y + height, image = img,
                                    anchor = N)

    def getWhitePoints(self):
        totalPoints = 0
        for piece in self.whitePieces:
            if isinstance(piece, King) == False:
                totalPoints += piece.points
        return totalPoints

    def getBlackPoints(self):
        totalPoints = 0
        for piece in self.blackPieces:
            if isinstance(piece, King) == False:
                totalPoints += piece.points
        return totalPoints


class Board(object):
    def __init__(self, height, start):
        self.height = height
        self.start = start 
        self.colStart = 1
        self.rows = self.cols = 4
        self.board = [[None] * self.cols for row in range(self.rows)]
        #initialize an empty board
    
    def draw(self, game):
        startMargin = self.start*game.wGap/2 + self.colStart*game.wGap
        heightMargin = self.height*6*game.hGap
        if isinstance(self, MovableBoard):
            start = self.start - self.fixedBoard.start
            #adjust position of movable board if it isn't fixed at 0,0
        else:
            start = 0 #for fixed boards
        for row in range(self.rows):
            for col in range(self.cols + 1):
                self.fill = "wheat" if (row+col)%2 == 1 else "brown"
                #give a slanted 3D look
                (x0,y0) = (startMargin + game.margin + (col + row/2)*game.wGap, 
                    game.height - (row+start)*game.hGap - game.margin - 
                    heightMargin)
                x1,y1 = x0 + game.wGap/2, y0 - game.hGap
                x2,y2 = x1 + game.wGap, y1
                x3,y3 = x2 - game.wGap/2, y0
                if col == self.cols: #numbers to help identify rows
                    game.canvas.create_text(x0 + game.wGap/2, (y0 + y2)/2, 
                                    text = str(row + self.start), anchor = N)
                    continue               
                piece = self.board[row][col] 
            #display all possible moves of a selected piece in tutorial mode 
                if (game.tutorialButton.selected == True and
                game.selectedPiece != None and 
                game.selectedPiece.isLegal(row, col, self, game) and
                (piece == None or piece.color != game.selectedPiece.color)):
                    game.selectedPiece.move(self, row, col, game, trial = True)
                    if game.checked == False: 
                        #account for pseudo legal moves
                        self.fill = "blue"
                    game.isChecked()
                game.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
             fill = self.fill, activefill = "red", outline = "black", width = 2)
                #create each block/square
        for row in range(self.rows): #draw all pieces at the correct position
            for col in range(self.cols):
                (x0,y0) = (startMargin + game.margin + (col + row/2)*game.wGap, 
                    game.height - (row + start)*game.hGap - game.margin - 
                    heightMargin)
                piece = self.board[row][col]
                if piece != None:
                    x, y = (2*x0 + 1.5*game.wGap)/2, (2*y0 - game.hGap)/2
                    piece.draw(game, x, y)
                    piece.board, piece.row, piece.col = self, row, col
                
    
    def drawLines(self, game):
        #lines help the user see overlapping rows
        startMargin = self.start*game.wGap/2 + self.colStart*game.wGap
        heightMargin = self.height*6*game.hGap
        (leftGap, rightGap) = self.findGap(game)
        for row in range(self.rows):
            for col in range(self.cols):
                (x0,y0) = (startMargin + game.margin + (col + row/2)*game.wGap, 
                    game.height - (row)*game.hGap - game.margin - heightMargin)
                x1,y1 = x0 + game.wGap/2, y0 - game.hGap
                x2,y2 = x1 + game.wGap, y1
                x3,y3 = x2 - game.wGap/2, y0
                if type(self) == Board:
                    if (row, col) == (2, 0):
                        game.canvas.create_line(x0, y0, x0, y0 - 10*game.hGap)
                    elif (row, col) == (3, 0):
                        game.canvas.create_line(x1, y1 - leftGap, x1, y1 - 
                            8*game.hGap)
                        game.canvas.create_line(x1, y1 - 8*game.hGap, x1, 
                                            y1 - 10*game.hGap, fill = "grey")
    #The colour is different as this part of the line is behind the other board
                    elif (row, col) == (3, 3):
                        game.canvas.create_line(x2, y2 - rightGap, x2, y2 - 
                            10*game.hGap)
                    elif (row, col) == (2, 3):
                        game.canvas.create_line(x3, y3, x3, y3 - 10*game.hGap)

    def findGap(self, game):
        #make changes to the line length so that it doesn't cross a 
        #movable board on top of it
        leftGap, rightGap = 0, 0
        for board in game.movableBoards:
            if board.fixedBoard == self:
                start = board.start - board.fixedBoard.start + 1 
                if start == 4:
                    leftGap = 6*game.hGap if board.colStart == 0 else leftGap
                    rightGap = 6*game.hGap if board.colStart == 4 else rightGap
        return (leftGap, rightGap)  

class MovableBoard(Board):
    def __init__(self, fixedBoard, start, colStart):
        self.fixedBoard = fixedBoard #keep a reference to a fixed board
        self.height = self.fixedBoard.height + 1
        self.start = start + self.fixedBoard.start - 1
        self.colStart = colStart 
        self.rows = self.cols = 2
        self.board = [[None] * self.cols for row in range(self.rows)]

    def draw(self, game): #draw a thick line for selection purposes
        super().draw(game)
        startMargin = self.start*game.wGap/2 + self.colStart*game.wGap
        heightMargin = self.height*6*game.hGap
        start = self.start - self.fixedBoard.start
        self.lineX = startMargin + game.margin + 1.5*game.wGap
        self.lineY = game.height - start*game.hGap - game.margin - heightMargin 
        self.lineHeight = 5*game.hGap
        self.lineWidth = 2.5
        self.lineColor = "black" if self != game.selectedBoard else "red"
        game.canvas.create_rectangle(self.lineX - self.lineWidth, 
            self.lineY, self.lineX + self.lineWidth, 
            self.lineY + self.lineHeight, fill = self.lineColor)

    def isSelected(self, x, y): #click on the line for movement
        try:
            return ((self.lineX - self.lineWidth < x < self.lineX + 
            self.lineWidth) and (self.lineY < y < self.lineY + self.lineHeight))
        except:
            pass

    def hasOnePiece(self, game): 
    #can only move it if has one piece of the player making the move and 
    #nothing else
        pieceCount = 0
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece != None and piece.color != game.turn:
                    return False
                elif piece != None and piece.color == game.turn:
                    pieceCount += 1
        return pieceCount == 1

    def isLegal(self, row, col, fixedBoard, game):
        #can only move at adjacent corners of boards
        if (self.hasOnePiece(game) == True):
            if (row, col) == (0, 0):
                start = row + fixedBoard.start - 1
                colStart = col
            elif (row, col) == (3,3):
                start = row + fixedBoard.start
                colStart = col + 1
            elif (row, col) == (3, 0):
                start = row + fixedBoard.start
                colStart = col
            elif (row, col) == (0, 3):
                start = row + fixedBoard.start - 1
                colStart = col + 1
            else:
                return False
            if self.fixedBoard == fixedBoard:
                return (abs(start - self.start) + 
                    abs(colStart - self.colStart) == 4)
            elif self.fixedBoard != fixedBoard:
                return (abs(start - self.start) + 
                    abs(colStart - self.colStart) == 2)

    def moveBoard(self, row, col, fixedBoard, game):
        #move the board to the new position
        oldBoard, oldStart, oldColstart = self.board, self.start, self.colStart
        self.fixedBoard = fixedBoard
        self.height = self.fixedBoard.height + 1
        if row == 0: start = 0
        elif row == 3: start = 4
        if col == 0: colStart = 0
        elif col == 3: colStart = 4
        self.start = start + self.fixedBoard.start - 1
        self.colStart = colStart
        game.isChecked() #account for pseudo legal moves so that check is taken
                        #into account
        if game.checked == True:
            self.start, self.colStart = oldStart, oldColstart
            self.board = oldBoard
            return
        game.selectedBoard = None
        game.turn = "black" if game.turn == "white" else "white" 

#NEVER CREATE A PIECE, ALWAYS CREATE A SUBCLASS
class Piece(object):
    def __init__(self, color, game):
        self.row = self.col = self.board = None
        self.color = color 
        self.moves = 0

    def draw(self, game):
        #the last moved piece is green and the selected piece is red
        self.drawColor = "red" if self == game.selectedPiece else self.color
        self.drawColor="lime green" if self==game.lastPiece else self.drawColor
        filename = "ChessPieces/Chess_%s_%s.gif" % (self.name, self.color)
        self.photo = PhotoImage(file = filename).subsample(2, 2) 

    def __repr__(self):
        return self.name

    def noPieceInWay(self, TgtRow, TgtCol, drow, dcol, row, col, game, 
                    selfBoard = None):
        #recursively check each position in a given direction to see that a 
        #clear path to the destination exists
        if selfBoard == None: 
            selfBoard = self.board
        row += drow 
        col += dcol
        if row == TgtRow and col == TgtCol: #reached position
            return True
        try: #because it fails on certain moves made by a movable board where
        #the row or col is outside the main board
            if (row >= selfBoard.start + selfBoard.rows or 
                row < selfBoard.start or col >= selfBoard.colStart + 
                selfBoard.cols or col < selfBoard.colStart or
                selfBoard.board[row - selfBoard.start][col -selfBoard.colStart]
                 != None):
                #find new boards with the same row and col, as vertical 
                #movements don't count as moves
                flag = False
                for board in game.boards:
                    if flag == False and board != selfBoard:
                        for boardRow in range(len(board.board)):
                            if (board.colStart > col or col - board.colStart 
                                >= board.cols): #account for movable boards
                                continue
                            if (row == boardRow + board.start and 
                        (board.board[boardRow][col - board.colStart] == None)):
                            #found a board with the same row and col!
                                selfBoard = board
                                flag = True #don't check the rest
                if flag == False: 
                    return False
        except:
            return False 
        if row == TgtRow and col == TgtCol:
            return True #reached
        else:
            return self.noPieceInWay(TgtRow, TgtCol, drow, dcol, row, col, 
                game, selfBoard) #test the next block/square in the same way

    def move(self, board, row, col, game, trial = False):
        #trial is for AI and check functions
        (self.oldRow, self.oldCol, self.oldBoard, self.oldPiece) = (
            self.row, self.col, self.board, board.board[row][col])
            #in case we need to undo the move
        flag = True
        if ((board.board[row][col] == None or 
            self.color != board.board[row][col].color) and 
            type(board.board[row][col]) != King): #make a pseudo legal move
            self.oldBoard.board[self.row][self.col] = None
            board.board[row][col] = self
            self.row, self.col = row, col 
            self.board = board
            game.isChecked()
            if (game.checked == True) or (trial == True): 
                self.undoMove(row, col, board) #undo the move if its a trial or
                                            #isn't possible because of check
                return
            else:
                self.moves += 1 #to keep track of pawn double moves
                game.lastPiece = self #to display the last moved piece
                flag = False
                game.selectedPiece = None
                game.turn = "black" if game.turn == "white" else "white"
                #change turn when an actual move is made
        if flag == True:
            game.isChecked() #restore the check state to the original value 
                            #if move conditions weren't met

    def undoMove(self, row, col, board):
        #take the piece to its old place and restore the value of the new place
        #to what it previously was
        self.oldBoard.board[self.oldRow][self.oldCol] = self
        board.board[row][col] = self.oldPiece
        (self.row, self.col, self.board) = (self.oldRow, self.oldCol, 
                                        self.oldBoard)
        

class Pawn(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "Pawn"
        self.points = 1

#"Chess pdt60" by File:Chess pdt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_pdt60.png#/media/
#File:Chess_pdt60.png
#that's all one url

#"Chess plt60" by File:Chess plt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_plt60.png#/media/
#File:Chess_plt60.png
#that's all one url

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x,y, text = "P", fill = self.drawColor)
        if self.color == "white": #Pawn reached the end! Upgrade to Queen
            if type(self.board) == MovableBoard:
                if self.row + self.board.start == 9:
                    self.convertPawn(game)
            elif type(self.board) == Board:
                if self.row + self.board.start == 8:
                    self.convertPawn(game)
        if self.color == "black":
            if type(self.board) == MovableBoard:
                if self.row + self.board.start == 0:
                    self.convertPawn(game)
            elif type(self.board) == Board:
                if self.row + self.board.start == 1:
                    self.convertPawn(game)

    def convertPawn(self, game):
        self.board.board[self.row][self.col] = Queen(self.color, game)
        pieces= game.whitePieces if self.color == "white" else game.blackPieces
        pieces.append(self.board.board[self.row][self.col])
        pieces.remove(self)


    def isLegal(self, boardRow, boardCol, board, game):
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False #only move to an empty spot or kill an opponent 
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]: #can't move on itself
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        if self.color == "white":
            #move 2 places on the first move
            if self.moves == 0 and abs(self.row + self.board.start - row) == 2:
                drow, dcol = 1, 0
                return self.noPieceInWay(row, col, drow, dcol, 
        self.row + self.board.start, self.col + self.board.colStart, game)
            #move only 1 on the other moves
            if row - (self.row + self.board.start) != 1:
                return False
        elif self.color == "black":
            #move 2 places on the first move
            if self.moves == 0 and abs(self.row + self.board.start - row) == 2:
                drow, dcol = -1, 0
                return self.noPieceInWay(row, col, drow, dcol, 
        self.row + self.board.start, self.col + self.board.colStart, game)
            #move only 1 on the other moves
            if (self.row + self.board.start) - row != 1:
                return False
        #col changes if it kills a piece and doesn't otherwise
        if board.board[boardRow][boardCol] != None:
            return abs(col - (self.col + self.board.colStart)) == 1
        else:
            return col == self.col + self.board.colStart


class King(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "King"
        self.points = 0

#"Chess kdt60" by File:Chess kdt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_kdt60.png#/media/
#File:Chess_kdt60.png

#"Chess klt60" by File:Chess klt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_klt60.png#/media/
#File:Chess_klt60.png

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x, y, text = "K", fill = self.drawColor)

    def isLegal(self, boardRow, boardCol, board, game):
        #Move one place in any direction
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]:
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        return (abs(col - (self.col + self.board.colStart)) <= 1 and
                abs(row - (self.row + self.board.start)) <= 1)
        
class Queen(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "Queen"
        self.points = 9

#"Chess qdt60" by File:Chess qdt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_qdt60.png#/media/
#File:Chess_qdt60.png

#"Chess qlt60" by File:Chess qlt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_qlt60.png#/media/
#File:Chess_qlt60.png

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x, y, text = "Q", fill = self.drawColor)

    def isLegal(self, boardRow, boardCol, board, game):
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]:
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        #Rook movement, i.e. move in a straight line. Find the direction of 
        #movement
        if self.col + self.board.colStart - col == 0:
            dcol = 0
            if self.row + self.board.start - row > 0:
                drow = -1
            elif self.row + self.board.start - row < 0:
                drow = 1
            else:
                return False
        elif self.row + self.board.start - row == 0:
            drow = 0
            if self.col + self.board.colStart - col > 0:
                dcol = -1
            elif self.col + self.board.colStart - col < 0:
                dcol = 1
            else:
                return False
        else:
            #Bishop movement, i.e. diagonal movement. Find the direction.
            if (self.row + self.board.start - row == self.col + 
                self.board.colStart - col):
                if self.col + self.board.colStart - col < 0:
                    drow, dcol = 1, 1
                else:
                    drow, dcol = -1, -1
            elif (self.row + self.board.start - row == col - 
                self.col - self.board.colStart):
                if col - self.col - self.board.colStart > 0:
                    drow, dcol = -1, 1
                else:
                    drow, dcol = 1, -1
            else:
                return False
        #check if there is a free path to the destination
        return self.noPieceInWay(row, col, drow, dcol, 
        self.row + self.board.start, self.col + self.board.colStart, game)

class Bishop(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "Bishop"
        self.points = 3

#"Chess bdt60" by File:Chess bdt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_bdt60.png#/media/
#File:Chess_bdt60.png

#"Chess blt60" by File:Chess blt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_blt60.png#/media/
#File:Chess_blt60.png

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x, y, text = "B", fill = self.drawColor)

    def isLegal(self, boardRow, boardCol, board, game):
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]:
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        if (self.row + self.board.start - row == 
            self.col + self.board.colStart - col):
            if self.col + self.board.colStart - col < 0:
                drow, dcol = 1, 1
            else:
                drow, dcol = -1, -1
        elif (self.row + self.board.start - row == 
            col - self.col - self.board.colStart):
            if col - self.col - self.board.colStart > 0:
                drow, dcol = -1, 1
            else:
                drow, dcol = 1, -1
        else:
            return False
        return self.noPieceInWay(row, col, drow, dcol, 
        self.row + self.board.start, self.col + self.board.colStart, game)


class Knight(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "Knight"
        self.points = 3

#"Chess ndt60" by File:Chess ndt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_ndt60.png#/media/
#File:Chess_ndt60.png

#"Chess nlt60" by File:Chess nlt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_nlt60.png#/media/
#File:Chess_nlt60.png 

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x, y, text = "N", fill = self.drawColor)

    def isLegal(self, boardRow, boardCol, board, game):
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]:
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        #Move 3 places but not in a straight line
        return ((abs(col - (self.col + self.board.colStart)) +
                abs(row - (self.row + self.board.start)) == 3) and
               (abs(col - (self.col + self.board.colStart)) != 0) and
               (abs(row - (self.row + self.board.start)) != 0))

class Rook(Piece):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.name = "Rook"
        self.points = 5

#"Chess rdt60" by File:Chess rdt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_rdt60.png#/media/
#File:Chess_rdt60.png

#"Chess rlt60" by File:Chess rlt45.svg. Licensed under CC BY-SA 3.0 via 
#Wikimedia Commons - 
#https://commons.wikimedia.org/wiki/File:Chess_rlt60.png#/media/
#File:Chess_rlt60.png

    def draw(self, game, x, y):
        super().draw(game)
        game.canvas.create_image(x, y + game.hGap/2, image = self.photo, 
                                 anchor = S)
        game.canvas.create_text(x, y, text = "R", fill = self.drawColor)

    def isLegal(self, boardRow, boardCol, board, game):
        otherPiece = board.board[boardRow][boardCol]
        if otherPiece != None and otherPiece.color == self.color:
            return False
        self.prevBoard = self.board
        if self == board.board[boardRow][boardCol]:
            return False
        row = boardRow + board.start
        col = boardCol + board.colStart
        if self.col + self.board.colStart - col == 0:
            dcol = 0
            if self.row + self.board.start - row > 0:
                drow = -1
            elif self.row + self.board.start - row < 0:
                drow = 1
            else:
                return False
        elif self.row + self.board.start - row == 0:
            drow = 0
            if self.col + self.board.colStart - col > 0:
                dcol = -1
            elif self.col + self.board.colStart - col < 0:
                dcol = 1
            else:
                return False
        else:
            return False
        return self.noPieceInWay(row, col, drow, dcol, 
        self.row + self.board.start, self.col + self.board.colStart, game)

class TrashCan(object): #display the dead
    def __init__(self, x, y, game, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, game):
        height = 180
        width = 80
        deltaWidth = 5
        deltaHeight = 10
        deltaArc = 40
        game.canvas.create_rectangle(self.x - width/2, self.y, self.x +
            width/2, self.y - height, fill = self.color, outline = self.color)
        game.canvas.create_rectangle(self.x - width/2 - deltaWidth, self.y - 
            deltaHeight, self.x + width/2 + deltaWidth, self.y + deltaHeight, 
            fill = self.color, outline = self.color)
        game.canvas.create_arc(self.x - width/2 - deltaWidth, self.y - height -
            deltaArc, self.x + width/2 + deltaWidth, self.y - height + 
            deltaArc ,fill = self.color, outline = self.color, 
            extent = 180)
        colGap = 20
        rowGap = 40
        piecesPerRow = 3
        leftEnd = self.x - colGap
        #iterate through the list of remove pieces, and draw them in the 
        #correct trashcan
        if self.color == "white":
            for i in range(len(game.removedPiecesBlack)):
                piece = game.removedPiecesBlack[i]
                row = i//piecesPerRow
                col = i%piecesPerRow
                piece.draw(game, leftEnd + col*colGap, self.y - row*rowGap)
        elif self.color == "black":
            for i in range(len(game.removedPiecesWhite)):
                piece = game.removedPiecesWhite[i]
                row = i//piecesPerRow
                col = i%piecesPerRow
                piece.draw(game, leftEnd + col*colGap, self.y - row*rowGap)

class Button(object):
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.selected = False

    def containsPoint(self, x, y):
        #if the x and y coordinate lie in the area covered by the button
        if (self.x < x < self.x + self.width and self.y < y < 
            self.y + self.height):
            return True
        else:
            return False

    def draw(self, game):
        #add spaces to the text so that activefill works properly
        totalChars = round(self.width/10)
        spaces = int((totalChars - len(self.name))/2)
        self.fill = "green" if self.selected == True else "pink"
        if self.name == "PLAY": self.fill = "thistle3"
        game.canvas.create_rectangle(self.x, self.y, self.x + self.width, 
                    self.y + self.height, fill = self.fill)
        game.canvas.create_text(self.x + self.width/2, self.y + self.height/2, 
            fill = "blue", text = " "*spaces + self.name + " "*spaces, 
            font = "Menlo 16", activefill = "red",) 

class Instructions(Animation): 
    #new window so people can learn and play side by side
    def run(self, width=300, height=300):
        # create the root and the canvas
        root = Toplevel()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()

        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
            self.canvas.update()

        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()

        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()

        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)

        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
            
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()
        print("Bye")

    def init(self):
    #image- https://www.flickr.com/photos/finlap/3684612986 #blue vignette
    #By- sure2talk
    #https://creativecommons.org/licenses/by/2.0/legalcode
    #This picture has been used as a background and no other modification
    #has been made. 
        self.pages = 6
        self.page = 1
        self.pageDict = {1: "Home", 2: "RulesPt1", 3: "RulesPt2", 
                4: "GameplayMvmt", 5: "GameplayButtons", 6: "GameplayWidgets"}
        #a dictionary with filenames for the image corresponding to the page
        #number
        self.photoList = list()
        #store the photoimage for all the images
        for i in range(1, self.pages + 1):
            filename = filename = "attachments/" + self.pageDict[i] + ".gif"
            photo = PhotoImage(file = filename).subsample(2,2)
            self.photoList.append(photo)
        self.margin = 20
        buttonWidth = 90
        buttonHeight = 30
        #to move through pages
        self.nextButton = Button("NEXT", self.width - self.margin - 
            buttonWidth, self.height - self.margin - buttonHeight,
            buttonWidth, buttonHeight)
        self.previousButton = Button("PREVIOUS", self.margin, self.height -
            self.margin - buttonHeight, buttonWidth, buttonHeight)

    def mousePressed(self, event):
        #change page number on clicking buttons
        if (self.nextButton.containsPoint(event.x, event.y) and 
            self.page < self.pages):
            self.page += 1
        if (self.previousButton.containsPoint(event.x, event.y) and 
            self.page > 1):
            self.page -= 1
    
    def keyPressed(self, event): 
        #change page number on pressing arrow keys
        if event.keysym == "Right" and self.page < self.pages:
            self.page += 1
        if event.keysym == "Left" and self.page > 1:
            self.page -= 1
    
    def timerFired(self): 
        pass

    def redrawAll(self):
        #draw the photo corresponding to the page number
        self.photo = self.photoList[self.page - 1]        
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        #don't draw previous on the first page and next on the last page
        if self.page < self.pages:
            self.nextButton.draw(self)
        if self.page > 1:
            self.previousButton.draw(self)

HelpMenu = Instructions()

App = Chess()
App.run(1000, 700)