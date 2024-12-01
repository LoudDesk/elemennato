def count2d(arr, value):
    summ = 0
    for line in arr:
        for cell in line:
            if cell==value:
                summ += 1
    return summ


class Cell:
    def __init__(self, board, y, x):
        self.board = board
        self.y = y
        self.x = x
        self.node = document.createElement('div')
        self.board.node.appendChild(self.node)
        self.node.cell = self
        self.team = 0
        self.selected = False
        self.locked = False
        
        self.node.onmouseover = self.onmouseover
        self.node.onmouseout = self.onmouseout
        self.node.onclick = self.onclick
    
    def neighbours(self):
        cells = self.board.cells
        n = [ [None,None,None],[None,None,None],[None,None,None], ]
        for y in [ -1, 0, +1 ]:
            for x in [ -1, 0, +1 ]:
                nx = self.x+x
                ny = self.y+y
                if nx>=0 and nx<=self.board.SIZE-1 and ny>=0 and ny<=self.board.SIZE-1:
                    #print(ny, nx)
                    n[y+1][x+1] = cells[ny][nx].team
        n[1][1] = None
        #print(self.team, n, count2d(n, self.team))
        return n

    def set_color(self, color):
        self.node.style.backgroundColor = color

    def onmouseover(self, event):
        #Verfärbt die Zelle, auf dem der Cursor ist
        if self.team == 0:
            self.locked = False
        if self.locked == False:
            if self.team == 0:
                self.set_color('yellow')
            elif self.team == 1:
                self.set_color('orange')
            elif self.team == 2:
                self.set_color('green')
    
    def onmouseout(self, event):
        #Verfärbt die Zelle, sobald der Cursor weg ist
        if self.team == 0:
            self.set_color('white')
        elif self.team == 1:
            if self.locked == False:
                self.set_color('red')
            else:
                self.set_color('#800')
        elif self.team == 2:
            if self.locked == False:
                self.set_color('blue')
            else:
                self.set_color('#008')
        
        #Verfärbt die markierte Zelle
        if self.team == 1 and self.selected == True:
            self.set_color('orange')
        elif self.team == 2 and self.selected == True:
            self.set_color('green')
    
    def onclick(self, event):
        #Ändert Team der Zelle(nur am Anfang)
        if game.state == 0:
            self.team += 1
            if self.team > 2:
                self.team = 0
        
        #print(self.locked)
        if game.state == 1:
            #Wählt Zelle aus
            if not self.team == 0:
                #print([self.x, self.y], game.has_moved)
                if not [self.x, self.y] == game.has_moved:
                    if self.locked == False:
                        if self.selected == False and self.team == game.turn[0]:
                            for j in game.board.cells:
                                for i in j:
                                    i.selected = False
                                    i.node.onmouseout()
                            self.selected = True
                        elif self.selected == True:
                            self.selected = False
            
            #Setzt Zelle auf leere Nachbarzelle
            elif self.team == 0:
                for j in game.board.cells:
                        for i in j:
                            if i.selected == True:
                                if i.x in [self.x+1, self.x, self.x-1] and i.y in [self.y+1, self.y, self.y-1]:
                                    #Ändert das Team der angeklickten Zelle zu 1 oder 2, und das Team der markierten Zelle zu 0
                                    i.selected = False
                                    self.team = i.team
                                    i.team = 0
                                    i.locked = False
                                    game.turn[1] += 1
                                    if game.turn[1] >= 2:
                                        if game.turn[0] == 1:
                                            game.turn[0] = 2
                                            game.node = document.querySelector('body')
                                            game.node.style.background = "lightblue"
                                        elif game.turn[0] == 2:
                                            game.turn[0] = 1
                                            game.node = document.querySelector('body')
                                            game.node.style.background = "pink"
                                        game.turn[1] = 0
                                        game.end_turn()
                                        #Markiert die Zelle als bereits bewegt
                                    game.has_moved = [self.x, self.y]
                                    i.node.onmouseout()
                                
                                elif [i.x, i.y] == [self.x, self.y-2]:
                                    print("N")
                                    if not i.team == game.board.cells[self.y-1][self.x].team and not 0 == game.board.cells[self.y-1][self.x].team:
                                        #Ändert das Team der angeklickten Zelle zu 1 oder 2, und das Team der markierten Zelle zu 0
                                        i.selected = False
                                        self.team = i.team
                                        i.team = 0
                                        i.locked = False
                                        game.turn[1] += 1
                                        if game.turn[1] >= 2:
                                            if game.turn[0] == 1:
                                                game.turn[0] = 2
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "lightblue"
                                            elif game.turn[0] == 2:
                                                game.turn[0] = 1
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "pink"
                                            game.turn[1] = 0
                                            game.end_turn()
                                            #Markiert die Zelle als bereits bewegt
                                        game.has_moved = [self.x, self.y]
                                        game.board.cells[self.y-1][self.x].team = 0
                                        game.board.cells[self.y-1][self.x].set_color('white')
                                        i.node.onmouseout()
                                        
                                elif [i.x, i.y] == [self.x+2, self.y]:
                                    print("O")
                                    if not i.team == game.board.cells[self.y][self.x+1].team and not 0 == game.board.cells[self.y][self.x+1].team:
                                        #Ändert das Team der angeklickten Zelle zu 1 oder 2, und das Team der markierten Zelle zu 0
                                        i.selected = False
                                        self.team = i.team
                                        i.team = 0
                                        i.locked = False
                                        game.turn[1] += 1
                                        if game.turn[1] >= 2:
                                            if game.turn[0] == 1:
                                                game.turn[0] = 2
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "lightblue"
                                            elif game.turn[0] == 2:
                                                game.turn[0] = 1
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "pink"
                                            game.turn[1] = 0
                                            game.end_turn()
                                            #Markiert die Zelle als bereits bewegt
                                        game.has_moved = [self.x, self.y]
                                        game.board.cells[self.y][self.x+1].team = 0
                                        game.board.cells[self.y][self.x+1].set_color('white')
                                        i.node.onmouseout()
                                        
                                elif [i.x, i.y] == [self.x, self.y+2]:
                                    print("S")
                                    if not i.team == game.board.cells[self.y+1][self.x].team and not 0 == game.board.cells[self.y+1][self.x].team:
                                        #Ändert das Team der angeklickten Zelle zu 1 oder 2, und das Team der markierten Zelle zu 0
                                        i.selected = False
                                        self.team = i.team
                                        i.team = 0
                                        i.locked = False
                                        game.turn[1] += 1
                                        if game.turn[1] >= 2:
                                            if game.turn[0] == 1:
                                                game.turn[0] = 2
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "lightblue"
                                            elif game.turn[0] == 2:
                                                game.turn[0] = 1
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "pink"
                                            game.turn[1] = 0
                                            game.end_turn()
                                            #Markiert die Zelle als bereits bewegt
                                        game.has_moved = [self.x, self.y]
                                        game.board.cells[self.y+1][self.x].team = 0
                                        game.board.cells[self.y+1][self.x].set_color('white')
                                        i.node.onmouseout()
                                        
                                elif [i.x, i.y] == [self.x-2, self.y]:
                                    print("W")
                                    if not i.team == game.board.cells[self.y][self.x-1].team and not 0 == game.board.cells[self.y][self.x-1].team:
                                        #Ändert das Team der angeklickten Zelle zu 1 oder 2, und das Team der markierten Zelle zu 0
                                        i.selected = False
                                        self.team = i.team
                                        i.team = 0
                                        i.locked = False
                                        game.turn[1] += 1
                                        if game.turn[1] >= 2:
                                            if game.turn[0] == 1:
                                                game.turn[0] = 2
                                                game.node = document.querySelector('body')
                                                game.node.style.background = f"lightblue"
                                            elif game.turn[0] == 2:
                                                game.turn[0] = 1
                                                game.node = document.querySelector('body')
                                                game.node.style.background = "pink"
                                            game.turn[1] = 0
                                            game.end_turn()
                                            #Markiert die Zelle als bereits bewegt
                                        game.has_moved = [self.x, self.y]
                                        game.board.cells[self.y][self.x-1].team = 0
                                        game.board.cells[self.y][self.x-1].set_color('white')
                                        i.node.onmouseout()

#Das Brett
class Board:
    SIZE = 32
    
    def __init__(self):
        self.node = document.querySelector('body')
        self.node.style.background = f"lightgray"
        
        self.node = document.querySelector('#board')
        self.node.style.gridTemplateColumns = f"repeat({self.SIZE}, 1fr)"

        self.cells = []
        for y in range(self.SIZE):
            row = []
            for x in range(self.SIZE):
                row.append( Cell(self, y, x) )
            self.cells.append(row)

class Game:
    def __init__(self):
        self.board = Board()
        #Der StartGameButton
        self.button_start_game = document.querySelector("#start_game")
        self.button_start_game.onclick = self.on_start_game 
        self.state = 0
        #turn[0]: Team, turn[1]: number of troops moved
        self.has_moved = None
        self.turn = [0, 0]
    
    def on_start_game(self, event):
        if self.state == 0:
            self.state = 1
            self.turn = [1, 0]
            game.node = document.querySelector('body')
            game.node.style.background = "pink"
        print(self.state)
    
    def end_turn(self):
        print("end_turn")
        for line in self.board.cells:
            for cell in line:
                if not cell.team == 0:
                    #print(i.x)
                    if count2d(cell.neighbours(), cell.team) < 1:
                        cell.team = 0
                        cell.locked = False
                        cell.set_color("white")
                        
                    if cell.team == 1:
                        if count2d(cell.neighbours(), 2) >= 4:
                            cell.team = 0
                            cell.locked = False
                            cell.set_color("white")
                            
                        elif count2d(cell.neighbours(), 2) == 3:
                            cell.locked = True
                            cell.set_color('#800')
                        
                        else:
                            cell.locked = False
                            cell.set_color('red')
                    elif cell.team == 2:
                        if count2d(cell.neighbours(), 1) >= 4:
                            cell.team = 0
                            cell.locked = False
                            cell.set_color("white")
                        
                        elif count2d(cell.neighbours(), 1) == 3:
                            cell.locked = True
                            cell.set_color('#008')
                        
                        else:
                            cell.locked = False
                            cell.set_color('blue')

    def run(self):
        print("running…")

game = Game()
game.run()
