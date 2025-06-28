import randomAdd commentMore actions
from Game2048 import *

class Player(BasePlayer):
	def __init__(self, timeLimit):
		BasePlayer.__init__(self, timeLimit)
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)

	def findMove(self, board):
		bestScore = -1000
		bestMove = ''
		
		for a in board.actions():
			print('Testing', a)
			m = board.move(a)
			if m.getScore() > bestScore:
				bestScore = m.getScore()
				bestMove = a
				
		self.setMove(bestMove)
		
    def findMove(self, board):
        moves = board.actions()
        bestMove = moves[0]
        bestScore = -1

        for move in moves:
            nextState = board.move(move)
            score = self.expectimax(nextState, 2)
            if score > bestScore:
                bestScore = score
                bestMove = move

        self.setMove(bestMove)

    def expectimax(self, board, depth):
        if depth == 0 or board.gameOver():
            return board.getScore()

        moves = board.actions()
        total = 0
        for move in moves:
            nextState = board.move(move)
            total += self.expectimax(nextState, depth -1)

        if moves:
            return total / len(moves)
        else:
            return 0
