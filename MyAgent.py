from Game2048 import *
import random
import time

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)

    def findMove(self, board):
        bestMove = None
        actions = board.actions()
        if not actions:
            self.setMove(None)
            return

        depth = 1
        while self.timeRemaining():
            currentBestScore = -1e10
            currentBestMove = bestMove if bestMove is not None else actions[0]

            for move in actions:
                if not self.timeRemaining():
                    break

                nextState = board.move(move)
                if nextState._board == board._board:
                    continue

                score = self.expectimax(nextState, depth, False)
                
                if score > currentBestScore:
                    currentBestScore = score
                    currentBestMove = move
            
            if self.timeRemaining():
                bestMove = currentBestMove
                self.setMove(bestMove)
            
            depth += 1

    def expectimax(self, board, depth, isMaxPlayer):
        if depth == 0 or board.gameOver():
            return self.heuristic(board)
        
        if isMaxPlayer:
            best_val = -1e10
            for move in board.actions():
                nextState = board.move(move)
                best_val = max(best_val, self.expectimax(nextState, depth - 1, False))
            return best_val
        else:
            total_val = 0
            possible_tiles = board.possibleTiles()
            if not possible_tiles:
                return self.heuristic(board)
            
            for pos, tile_val in possible_tiles:
                child_board = board.addTile(pos, tile_val)
                total_val += self.expectimax(child_board, depth - 1, True)

            return total_val / len(possible_tiles)

    def heuristic(self, board):
        smoothness = 0
        for i in range(4):
            for j in range(3):
                val1_h = board.getTile(i, j)
                val2_h = board.getTile(i, j + 1)
                if val1_h > 0 and val2_h > 0:
                    smoothness -= abs(val1_h - val2_h)
                
                val1_v = board.getTile(j, i)
                val2_v = board.getTile(j + 1, i)
                if val1_v > 0 and val2_v > 0:
                    smoothness -= abs(val1_v - val2_v)

        mono_bonus = 0
        for i in range(4):
            row = [board.getTile(i, j) for j in range(4)]
            col = [board.getTile(j, i) for j in range(4)]
            
            is_mono_row = all(row[k] >= row[k+1] for k in range(3)) or all(row[k] <= row[k+1] for k in range(3))
            if is_mono_row:
                mono_bonus += 150

            is_mono_col = all(col[k] >= col[k+1] for k in range(3)) or all(col[k] <= col[k+1] for k in range(3))
            if is_mono_col:
                mono_bonus += 150

        empty_tiles = 0
        for i in range(16):
            if board._board[i] == 0:
                empty_tiles += 1

        max_tile = 0
        for tile in board._board:
            if tile > max_tile:
                max_tile = tile

        corner_bonus = 0
        if board.getTile(0, 0) == max_tile:
            corner_bonus = max_tile * 40000.0

        final_score = (
            smoothness * 1.0 +
            mono_bonus * 1.0 +
            empty_tiles * 270.0 +
            max_tile * 1.0 +
            corner_bonus
        )
                           
        return final_score
