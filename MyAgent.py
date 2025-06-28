from Game2048 import *
import math
import time

class Player(BasePlayer):
    def _init_(self, timeLimit):
        BasePlayer._init_(self, timeLimit)

    def findMove(self, board):
        bestScore = float('-inf')
        bestMove = ''
        for move in board.actions():
            child, _ = board.result(move)
            v = self.expectimax(child, depth=3, isPlayer=False, alpha=float('-inf'), beta=float('inf'))
            if v > bestScore:
                bestScore = v
                bestMove = move
            if not self.timeRemaining():
                break
        if bestMove:
            self.setMove(bestMove)
        else:
            actions = board.actions()
            if actions:
                self.setMove(actions[0])

    def expectimax(self, state, depth, isPlayer, alpha, beta):
        if depth == 0 or state.gameOver() or not self.timeRemaining():
            return self.evaluate(state)

        actions = state.actions()
        if not actions:
            return self.evaluate(state)

        if isPlayer:
            best = float('-inf')
            for move in actions:
                child, _ = state.result(move)
                v = self.expectimax(child, depth-1, False, alpha, beta)
                best = max(best, v)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
                if not self.timeRemaining():
                    break
            return best
        else:
            value = 0
            ref_action = actions[0]
            for (g, p) in state.possibleResults(ref_action):
                v = self.expectimax(g, depth-1, True, alpha, beta)
                value += p * v
                if not self.timeRemaining():
                    break
            return value

    def evaluate(self, state):
        board = state._board
        empty_tiles = sum(1 for x in board if x == 0)
        max_tile = max(board)
        smoothness = self.smoothness(board)
        monotonicity = self.monotonicity(board)

        return (
            0.4 * empty_tiles +
            1.0 * math.log(2 ** max_tile) +
            0.1 * smoothness +
            1.0 * monotonicity
        )

    def smoothness(self, board):
        score = 0
        for r in range(4):
            for c in range(3):
                a = board[4*r + c]
                b = board[4*r + c + 1]
                if a and b:
                    score -= abs((2*a) - (2*b))
        for c in range(4):
            for r in range(3):
                a = board[4*r + c]
                b = board[4*(r+1) + c]
                if a and b:
                    score -= abs((2*a) - (2*b))
        return score

    def monotonicity(self, board):
        def score_line(line):
            inc = dec = 0
            for i in range(3):
                if line[i] > line[i+1]:
                    dec += line[i] - line[i+1]
                else:
                    inc += line[i+1] - line[i]
            return -min(inc, dec)

        total = 0
        for r in range(4):
            row = [board[4*r + c] for c in range(4)]
            total += score_line(row)

        for c in range(4):
            col = [board[4*r + c] for r in range(4)]
            total += score_line(col)

        return total
