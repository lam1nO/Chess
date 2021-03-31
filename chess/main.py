import copy

class Color(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Empty(object):
    color = Color.EMPTY
    points = 0
    name = 'Empty'
    def get_moves(self, board, x, y):
        return []

    def __repr__(self):
        return ' '


class ChessMan(object):
    IMG = None

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.IMG[0 if self.color == Color.WHITE else 1]


class Pawn(ChessMan):
    IMG = ('♟', '♙')
    name = 'Pawn'
    points = 1
    def get_moves(self, board, x, y):
        moves = []
        if self.color == Color.BLACK and y < 7 and board.get_color(x, y+1) == Color.EMPTY:
            moves.append([x, y+1])
            if y == 1 and board.get_color(x, y+2) == Color.EMPTY:
                moves.append([x, y+2])
            if x + 1 <= 7 and y + 1 <= 7 and board.get_color(x+1,y+1) == Color.WHITE:
                moves.append([x+1,y+1]) 
            if x - 1 >= 0 and y + 1 <= 7 and board.get_color(x-1,y+1) == Color.WHITE:
                moves.append([x-1,y+1]) 
         
        if self.color == Color.WHITE and y > 0 and board.get_color(x, y-1) == Color.EMPTY:
            moves.append([x, y-1])
            if y == 6 and board.get_color(x, y-2) == Color.EMPTY:
                moves.append([x, y-2])
            if x+1 <= 7 and y - 1 >= 0 and board.get_color(x+1,y-1) == Color.BLACK:
                moves.append([x+1,y-1]) 
            if x-1 >= 0 and y - 1 >= 0 and board.get_color(x-1,y-1) == Color.BLACK:
                moves.append([x-1,y-1]) 

        # На проходе
        
        len_his = len(board.history_of_moves)
        if (len_his == 0):
            return moves
        
        fr = [board.history_of_moves[len_his - 1][1][0], board.history_of_moves[len_his - 1][1][1]]
        if (board.board[fr[1]][fr[0]].name == 'Pawn'):
            if ( abs (board.history_of_moves[len_his - 1][0][1] - board.history_of_moves[len_his - 1][1][1]) == 2):
                if (abs (board.history_of_moves[len_his - 1][0][0] - x) == 1 and board.history_of_moves[len_his - 1][1][1] == y ):
                    moves.append([board.history_of_moves[len_his - 1][0][0], (board.history_of_moves[len_his - 1][0][1] + board.history_of_moves[len_his - 1][1][1]) // 2 ])

        return moves


class King(ChessMan):
    IMG = ('♚', '♔')
    name = 'King'
    points = 100
    isMoved = False
    def get_moves(self, board, x, y):
        moves = []
        moves.append([x, y+1])
        moves.append([x+1, y+1])
        moves.append([x+1, y])
        moves.append([x+1, y-1])
        moves.append([x-1, y-1])
        moves.append([x-1, y])
        moves.append([x, y-1])
        moves.append([x-1, y+1])
        i = 0
        while i < len (moves):
            move = moves[i]
            if (move[0] > 7) or (move[0] < 0) or (move[1] > 7) or (move[1] < 0) or (board.get_color(move[0], move[1]) == board.get_color(x,y)):
                moves.pop(i)
                i -= 1
            i += 1
        
        # CASTLE
        if self.isMoved:
            return moves
        i = 1
        while True:
            if x+i > 7:
                break
            if x != 4:
                break
            if board.isChecked(x+1, y, board.get_color(x,y)) or board.isChecked(x+2,y, board.get_color(x,y)):
                break
            if board.get_color(x+i, y) == 0:
                i += 1
                continue
            else: 
                if board.board[y][x+i].name == Rook(board.get_color(x,y)).name and board.get_color(x, y) == board.get_color(x+i, y):
                    if not board.board[y][x+i].isMoved:
                        moves.append([x+2, y])
                    else:
                        break
                else:
                    break
            i += 1

        i = 1
        while True:
            if x-i < 0:
                break
            if x != 4:
                break
            if board.isChecked(x-1, y, board.get_color(x,y)) or board.isChecked(x-2,y, board.get_color(x,y)):
                break
            if board.get_color(x-i, y) == 0:
                i += 1
                continue
            else: 
                if board.board[y][x-i].name == Rook(board.get_color(x,y)).name and board.get_color(x, y) == board.get_color(x-i, y):
                    if not board.board[y][x-i].isMoved:
                        moves.append([x-2, y])
                    else:
                        break
                else:
                    break
            i += 1

        i = 0
        while i < len(moves):
            move = moves[i]
            if board.isChecked(move[0], move[1], board.get_color(x,y)):
                moves.pop(i)
                i -= 1
            i += 1
        return moves
    
    def isChecked(self, board, x, y):
        kingColor = board.get_color(x, y)
        were = board.board[y][x]
        board.board[y][x] = Bishop(kingColor)
        bishopMoves = Bishop(kingColor).get_moves(board, x,y)
        
        board.board[y][x] = Rook(kingColor)
        rookMoves = Rook(kingColor).get_moves(board, x, y)


        board.board[y][x] = Knight(kingColor)
        knightMoves = Knight(kingColor).get_moves(board, x, y)
        
        pawnMoves = []
        if (kingColor == 1):
            pawnMoves = [[x+1,y+1],[x-1,y+1]]
            if x-1 < 0:
                pawnMoves.pop(1)
            if x+1 > 7:
                pawnMoves.pop(0)
            if y+1 > 7:
                pawnMoves.clear()
        if (kingColor == 2):
            pawnMoves = [[x+1,y-1],[x-1,y-1]]
            if x-1 < 0:
                pawnMoves.pop(1)
            if x+1 > 7:
                pawnMoves.pop(0)
            if y-1 < 0:
                pawnMoves.clear()
        
        # bishopMoves
        i = 0
        while i < len (bishopMoves):
            move = bishopMoves[i]
            if board.get_color(move[0], move[1]) == Color.EMPTY or board.board[move[1]][move[0]].name != 'Bishop' and board.board[move[1]][move[0]].name != 'Queen':
                bishopMoves.pop(i)
                i -= 1
            i += 1

        # knightMoves
        i = 0
        while i < len (knightMoves):
            move = knightMoves[i]
            if board.get_color(move[0], move[1]) == Color.EMPTY or board.board[move[1]][move[0]].name != 'Knight':
                knightMoves.pop(i)
                i -= 1
            i += 1

        # rookMoves
        i = 0
        while i < len (rookMoves):
            move = rookMoves[i]
            if board.get_color(move[0], move[1]) == Color.EMPTY or board.board[move[1]][move[0]].name != 'Rook' and board.board[move[1]][move[0]].name != 'Queen':
                rookMoves.pop(i)
                i -= 1
            i += 1

        # pawnMoves
        i = 0
        while i < len (pawnMoves):
            move = pawnMoves[i]
            if board.board[move[1]][move[0]].name != 'Pawn':
                pawnMoves.pop(i)
                i -= 1
            elif board.get_color(move[0], move[1]) == kingColor:
                pawnMoves.pop(i)
                i -= 1
            i += 1

        board.board[y][x] = were
        if len(bishopMoves) + len(rookMoves) + len(knightMoves) + len(pawnMoves) > 0:
            return True
        return False


    def isMate(self, board, color):
        k = 0
        for i in board.board:
            for j in i:
                x = k // 8
                y = k % 8
                if board.get_color(y, x) == color:
                    if not len(board.get_moves(y, x, 0) ) == 0:
                        return False
                k += 1
        return True

class Knight(ChessMan):
    IMG = ('♞', '♘')
    name = 'Knight'
    points = 3
    def get_moves(self, board, x, y): 
        moves = []
        moves.append([x+1, y+2])
        moves.append([x+2, y+1])
        moves.append([x-1, y+2])
        moves.append([x+1, y-2])
        moves.append([x-1, y-2])
        moves.append([x+2, y-1])
        moves.append([x-2, y+1])
        moves.append([x-2, y-1])
        i = 0
        while i < len (moves):
            move = moves[i]
            if (move[0] > 7) or (move[0] < 0) or (move[1] > 7) or (move[1] < 0) or (board.get_color(move[0], move[1]) == board.get_color(x,y)):
                moves.pop(i)
                i -= 1
            i += 1
        return moves 
        
class Bishop(ChessMan):
    IMG = ('♝', '♗')
    points = 3
    name = 'Bishop'
    def get_moves(self, board, x, y):
        moves = []
        i = 1
        while True:
            if x+i > 7 or y+i > 7:
                break
            elif (board.get_color(x+i, y+i) == board.get_color(x,y)):
                break
            elif (board.get_color(x+i, y+i) != Color.EMPTY):
                moves.append([x+i, y+i])
                break
            else:
                moves.append([x+i, y+i])
                i += 1
        i = 1
        while True:
            if x-i < 0 or y-i < 0:
                break
            elif (board.get_color(x-i, y-i) == board.get_color(x,y)):
                break
            elif (board.get_color(x-i, y-i) != Color.EMPTY):
                moves.append([x-i, y-i])
                break
            else:
                moves.append([x-i, y-i])
                i += 1
        i = 1
        while True:
            if x+i > 7 or y-i < 0:
                break
            elif (board.get_color(x+i, y-i) == board.get_color(x,y)):
                break
            elif (board.get_color(x+i, y-i) != Color.EMPTY):
                moves.append([x+i, y-i])
                break
            else:
                moves.append([x+i, y-i])
                i += 1
        i = 1
        while True:
            if x-i < 0 or y+i > 7:
                break
            elif (board.get_color(x-i, y+i) == board.get_color(x,y)):
                break
            elif (board.get_color(x-i, y+i) != Color.EMPTY):
                moves.append([x-i, y+i])
                break
            else:
                moves.append([x-i, y+i])
                i += 1
        return moves

class Rook(ChessMan):
    IMG = ('♜', '♖')
    points = 5
    name = 'Rook'
    isMoved = False
    def get_moves(self, board, x, y):
        moves = []
        i = 1
        while True:
            if (x+i > 7):
                break
            elif (board.get_color(x+i, y) == board.get_color(x,y)):
                break
            elif (board.get_color(x+i, y) != Color.EMPTY):
                moves.append([x+i, y])
                break
            else:
                moves.append([x+i, y])
                i += 1
        i = 1
        while True:
            if (y+i > 7):
                break
            elif (board.get_color(x, y+i) == board.get_color(x,y)):
                break
            elif (board.get_color(x, y+i) != Color.EMPTY):
                moves.append([x, y+i])
                break
            else:
                moves.append([x, y+i])
                i += 1
        i = 1
        while True:
            if (x-i < 0):
                break
            elif (board.get_color(x-i, y) == board.get_color(x,y)):
                break
            elif (board.get_color(x-i, y) != Color.EMPTY):
                moves.append([x-i, y])
                break
            else:
                moves.append([x-i, y])
                i += 1
        i = 1
        while True:
            if (y-i < 0):
                break
            elif (board.get_color(x, y-i) == board.get_color(x,y)):
                break
            elif (board.get_color(x, y-i) != Color.EMPTY):
                moves.append([x, y-i])
                break
            else:
                moves.append([x, y-i])
                i += 1
        return moves

class Queen(ChessMan):
    IMG = ('♛', '♕')
    name = 'Queen'
    points = 8
    def get_moves(self, board, x, y):
        return Rook.get_moves(self, board, x, y) + Bishop.get_moves(self, board, x, y)

class Board(object):
    history_of_moves = [] # [[x_from,y_from,Piece_from], [x_to, y_to, Piece_to]]
    Kings = [[4, 0], [4, 7]] # black, white
    def __init__(self):
        self.board = [[Empty()] * 8 for y in range(8)]
        
        # PAWNS
        for y in range (8):
            self.board[1][y] = Pawn(Color.BLACK)
        
        for y in range (8):
            self.board[6][y] = Pawn(Color.WHITE)
        

        # KNIGHTS
        self.board[0][1] = Knight(Color.BLACK)
        self.board[0][6] = Knight(Color.BLACK)
        self.board[7][1] = Knight(Color.WHITE)
        self.board[7][6] = Knight(Color.WHITE)
        self.board[6][7] = Pawn(Color.WHITE)
        
        # KINGS
        self.board[0][4] = King(Color.BLACK)
        self.board[7][4] = King(Color.WHITE)


        # BISHOPS
        self.board[0][5] = Bishop(Color.BLACK)
        self.board[0][2] = Bishop(Color.BLACK)
        self.board[7][5] = Bishop(Color.WHITE)
        self.board[7][2] = Bishop(Color.WHITE)

        # ROOKS
        self.board[0][0] = Rook(Color.BLACK)
        self.board[0][7] = Rook(Color.BLACK)
        self.board[7][7] = Rook(Color.WHITE)
        self.board[7][0] = Rook(Color.WHITE)

        # QUEENS
        self.board[0][3] = Queen(Color.BLACK)
        self.board[7][3] = Queen(Color.WHITE)


    def get_color(self, x, y):
        return self.board[y][x].color

    def get_moves(self, x, y, from_where):
        moves = self.board[y][x].get_moves(self, x, y)        

        color = self.get_color(x, y)
        color -= 1 
        if (self.isChecked(self.Kings[color][0], self.Kings[color][1], color + 1)):
            i = 0
            while i < len(moves):
                move = moves[i]
                move_to = self.board[move[1]][move[0]]
                to_x, to_y = move[0], move[1]
                move_from = self.board[y][x]
                self.move([x, y], [move[0],move[1]])
                if (self.isChecked(self.Kings[color][0], self.Kings[color][1], color + 1)):
                    moves.pop(i)
                    i -= 1
                self.board[y][x] = move_from
                self.board[to_y][to_x] = move_to
                i += 1
                
        if (from_where):
            move_color = [44, 46]
            colors = [40, 41]
            res = ''
            i = 0
            c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            print ('   ', end='')
            for x in range (8):
                print ('' + c[x], end=' ')
            print ()
            for y in range(8):
                res += str(8 - y) + '  '
                for x in range (8):
                    if ([x, y] in moves):
                        res += set_color(move_color[i]) + str(self.board[y][x]) + ' '
                    else: 
                        res += set_color(colors[i]) + str(self.board[y][x]) + ' '
                    i = 1 - i
                res += set_color(40) + "" + str(8 - y) + '\n'
                i = 1 - i
            res += '   A B C D E F G H '
            print (res)
        return moves
        

    def isMate(self, color):
        return self.board[ self.Kings[color - 1][1] ][ self.Kings[color - 1][0] ].isMate(self, color) 

    def move(self, xy_from, xy_to):
        points = 0
        points += self.board[xy_to[1]][xy_to[0]].points
        
        if (self.board[xy_from[1]][xy_from[0]] == King(Color.WHITE) or Rook(Color.WHITE) or King(Color.BLACK) or Rook(Color.BLACK)):
            self.board[xy_from[1]][xy_from[0]].isMoved = True
        
        # kingMoved
        if self.board[xy_from[1]][xy_from[0]].name == 'King':
            self.Kings[self.get_color(xy_from[0], xy_from[1]) - 1] = [xy_to[0], xy_to[1]]


        self.history_of_moves.append([[xy_from[0], xy_from[1], self.board[xy_from[1]][xy_from[0]]],[xy_to[0], xy_to[1], self.board[xy_to[1]][xy_to[0]]]])
        

        


        # special pawn
        if (self.board[xy_from[1]][xy_from[0]].name == 'Pawn'):
            if (xy_from[0] != xy_to[0]):
                # takes
                if self.board[xy_to[1]][xy_to[0]].name == 'Empty':
                    self.board[xy_from[1]][xy_to[0]] = Empty()
                    points += 1

        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Empty()

        if self.isMate (1 if self.get_color(xy_to[0], xy_to[1]) == 2 else 2):
            print ('Мат,', 'Белые' if self.get_color( xy_to[0], xy_to[1] ) == 2 else 'Черные', 'Выиграли')
        
        return points

    def __str__(self):
        colors = [40, 41]
        res = ''
        i = 0
        c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        print ('   ', end='')
        for x in range (8):
            print ('' + c[x], end=' ')
        print ()
        for y in range(8):
            res += str(8 - y) + '  '
            for x in range (8):
                res += set_color(colors[i]) + str(self.board[y][x]) + ' '
                i = 1 - i
            res += set_color(40) + " " + str(8 - y) + '\n'
            i = 1 - i
        res += '   A B C D E F G H '
        return res
    
    def isChecked(self, x, y, color):
        were = self.board[y][x]
        self.board[y][x] = King(color)
        res = self.board[y][x].isChecked(self, x, y)
        self.board[y][x] = were
        return res
        
def set_color(color): return '\033[%sm' % color 

def Game():
    b = Board()
    print (b.isChecked(b.Kings[1][0], b.Kings[1][1], 2))
    turn = 2
    WHITES = 0
    BLACKS = 0
    print ('Game started! Good luck!')
    while True:
        print (b)
        if (turn == 2):
            print('Ход белых. Выберите фигуру')
        else:
            print('Ход черных. Выберите фигуру')
        move = input()
        
        # ERRORS
        if (len(move) != 2):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        if move[1] < chr(49) or move[1] > chr(56):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        move = move.upper()
        if move[0] < chr(65) or move[0] > chr(72):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        
        letters = {
            'A' : 0,
            'B' : 1,
            'C' : 2,
            'D' : 3,
            'E' : 4,
            'F' : 5,
            'G' : 6,
            'H' : 7

        }
        x,y = letters[move[0]], int(move[1])
        y = 8-y

        if (b.get_color(x,y) != turn):
            print ("ERROR")
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        
        moves = b.get_moves(x, y, 1)
        print ('Выбери куда ею сходишь')
        move = input()
        if (len(move) != 2):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        if move[1] < chr(49) or move[1] > chr(56):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        move = move.upper()
        if move[0] < chr(65) or move[0] > chr(72):
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue
        x1,y1 = letters[move[0]], int(move[1])
        y1 = 8-y1

        if not [x1, y1] in moves:
            print ('ERROR')
            print ('Нажмите ENTER, чтобы продолжить')
            a = input()
            continue

        b.move([x,y], [x1,y1])
        turn = 1 if turn == 2 else 2

Game()