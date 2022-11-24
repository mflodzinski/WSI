from Pick import *
from random import randint, shuffle

def alhpabeta(state : PickState, depth : int, alpha : int, beta : int, maximizingPlayer : bool):
    if depth == 0 or state.is_finished():
        return state.static_evaluation(maximizingPlayer), None
    
    if maximizingPlayer:
        maxEval = float('-inf')
        bestMove = None
        moves = state.get_moves()
        shuffle(moves)
        for move in moves:
            child = state.make_move(move)
            eval,_ = alhpabeta(child, depth - 1, alpha, beta, False)
            if eval > maxEval:
                maxEval = eval
                bestMove = move
 
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestMove
    
    else:
        minEval = float('inf')
        worstMove = None
        moves = state.get_moves()
        shuffle(moves)
        for move in moves:
            child = state.make_move(move)
            eval,_ = alhpabeta(child, depth - 1, alpha, beta , True)
            if eval < minEval:
                minEval = eval
                worstMove = move 
                    
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, worstMove

def get_player_input(state : PickState) -> 'PickMove':
    possible_moves = [move.number for move in state.get_moves()]
    move = input(f"Possible moves: {possible_moves}\nYour move: ")
    while(int(move) not in possible_moves):
        move = input("Please enter correct value\nYour move: ")
    return PickMove(int(move))
    
def make_computer_move(state : PickState, depth : int) -> 'PickMove':
    _, best_move = alhpabeta(state, depth, float('-inf'), float('inf'), False)
    return best_move
    
def lets_play(n : int, depth : int):
    game = Pick(n = n)
    while(not game.state.is_finished()):
        
        human_move = get_player_input(game.state)
        game.make_move(human_move)
        if game.state.is_finished():
            break
        computer_move = make_computer_move(game.state, depth)
        game.make_move(computer_move)
        print(f"Computer move: {computer_move.number}")
    if game.get_winner():
        print(game.get_winner().char)
    else:
        print("Draw!")
    return


def two_computers_game(n, depths):
    game = Pick(n = n)
    player = 0

    while not game.state.is_finished():
        eval, move = alhpabeta(game.state, depths[player], float('-inf'), float('inf'), not player)
        print(f"player: {player+1}, eval: {eval}, move: {move.number}")
        game.make_move(move)
        player = 1 - player
        
    if game.state.get_winner() != None:
        print("Winner: ", game.state.get_winner().char + "\n")
        return int(game.state.get_winner().char)
        
    else:
        print("Draw!\n")
        return 0
        
def test(n, depths, iterations):
    res = [0, 0, 0] # [draw, firstP_wins, secondP_wins]
    for i in range(iterations):
        index = two_computers_game(n, depths)
        res[index] += 1
    print(res)
    return res
        
if __name__ == "__main__":
    #res = test(4, [3,1], 50)
    #lets_play(n=3, depth=3)
    res = test(4, [4, 2], 20)
    #res = test(4, [1,3], 50)
    #res = test(4, [2,1], 50)
    #res = test(4, [2,2], 50)
