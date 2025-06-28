from Game2048 import *
import random

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)

    def findMove(self, board):
        moves = self.moveOrder(board)
        bestMove = moves[0]
        bestScore = float('-inf')
        for move in moves:
            score = self.expectimax(board.move(move), 4)
            if score > bestScore:
                bestScore = score
                bestMove = move
        self.setMove(bestMove)

    def expectimax(self, board, depth, isMax=True):
        if depth == 0 or board.gameOver():
            return self.heuristic(board)
        if isMax:
            return max(self.expectimax(board.move(move), depth - 1, False) for move in board.actions())
        else:
            total = 0
            possible = board.possibleTiles()
            for (pos, tile) in possible:
                child = board.addTile(pos, tile)
                total += self.expectimax(child, depth - 1, True)
            return total / len(possible) if possible else 0

    def heuristic(self, board):
        score = board.getScore()
        empty = sum(1 for i in range(4) for j in range(4) if board.getTile(i,j)==0)
        maxTile = max(board.getTile(i,j) for i in range(4) for j in range(4))
        monotonicity = 0
        for i in range(4):
            for j in range(3):
                if board.getTile(i,j) >= board.getTile(i,j+1):
                    monotonicity += 1
                if board.getTile(j,i) >= board.getTile(j+1,i):
                    monotonicity +=1
        cornerBonus = board.getTile(0,0) * 300
        return score + empty * 150 + maxTile * 300 + monotonicity * 100 + cornerBonus

    def moveOrder(self, board):
        moves = board.actions()
        moves.sort(reverse=True)
        return moves
