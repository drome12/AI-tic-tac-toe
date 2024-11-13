from tictactoe import TicTacToe
import math
import random
import time


def minimax(board, depth, maximizing_player, ai_player):
    if ai_player == 'X':
        opponent = 'O'
    else: opponent = 'X' 

    # checking base cases 
    # ai win, positive score returned
    if board.current_winner == ai_player:
        return {'position': None, 'score': 1 * depth}
    # ai's opponent win, returning negative score
    elif board.current_winner == opponent:
        return {'position': None, 'score': -1 * depth}
    # tie case, 0 returned
    elif board.empty_squares_available() == 0:
        return {'position': None, 'score': 0}

    if maximizing_player: # maximizing ai's game

        curr_move = None # the best move is none to start
        curr_score = -1000 # low val for best score to start
        
        for move in board.available_moves(): # iterating through all moves
            # making a move
            board.make_move(move, ai_player)
            # recursive call with minimized players turn
            recursive_result = minimax(board, depth - 1, False, ai_player)
            board.board[move] = ' '  # restoring board by undoing move
            board.current_winner = None #setting winner to none 
            #updating best score and position when better score found
            if recursive_result['score'] > curr_score:
                curr_move = move
                curr_score = recursive_result['score']
        return {'position': curr_move, 'score': curr_score} # returning best move/score
    else: # opponents turn, minimize

        curr_move = None # None again for best move to start
        curr_score = 1000 # now high value to start
        
        for move in board.available_moves():
            board.make_move(move, opponent)
            # now recursing on maximized player 
            recursive_result = minimax(board, depth-1, True, ai_player) 
            board.board[move] = ' '  
            board.current_winner = None 
            if recursive_result['score'] < curr_score:
                curr_move = move
                curr_score = recursive_result['score']
        return {'position': curr_move, 'score': curr_score}



def minimax_with_alpha_beta(board, depth, alpha, beta, maximizing_player, ai_player):
    if ai_player == 'X':
        opponent = 'O'
    else: opponent = 'X' 

    # checking base cases 
   
    if board.current_winner == ai_player:
        return {'position': None, 'score': 1 * depth}
    
    elif board.current_winner == opponent:
        return {'position': None, 'score': -1 * depth}
    
    elif board.empty_squares_available() == 0:
        return {'position': None, 'score': 0}
    
    if maximizing_player:

        curr_move = None
        curr_score = -1000
        
        for move in board.available_moves():
            board.make_move(move, ai_player)
            # recursing, seting new alpha and beta vals, minimize player's turn
            recursive_result = minimax_with_alpha_beta(board, depth-1, alpha, beta, False, ai_player)
            board.board[move] = ' '  
            board.current_winner = None
            if recursive_result['score'] > curr_score:
                curr_move = move
                curr_score = recursive_result['score']
                # higher score found, update alpha
            if recursive_result['score'] > alpha:
                alpha = recursive_result['score']
            if beta <= alpha: break # if alpha greater than or equal to beta stop evaluating      
        return {'position': curr_move, 'score': curr_score}
    else:
        
        curr_move = None
        curr_score = 1000

        for move in board.available_moves():
            board.make_move(move, opponent)
            # max players turn
            recursive_result = minimax_with_alpha_beta(board, depth-1, alpha, beta, True, ai_player)
            board.board[move] = ' '  
            board.current_winner = None
            if recursive_result['score'] < curr_score:
                curr_move = move
                curr_score = recursive_result['score']               
                # lower score found, update beta
            if recursive_result['score'] < beta:
                beta = recursive_result['score']
            if beta <= alpha: break      
        return {'position': curr_move, 'score': curr_score}

    




def play_game_human_moves_first():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    letter = 'X'  # Human player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI's turn
            square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_ai_moves_first():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    first_move = True

    letter = 'O'  # AI player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI's turn
            if first_move:
                square = random.randint(0, 8)
                first_move = False
            else:
                square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_human_vs_human():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    letter = 'O'  # Human (O) player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # Human (O)'s turn
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

                if square is None:
                    print("\nGame is a draw!")
                    break
                game.make_move(square, letter)
                print(f"\nAI (O) chooses square {square + 1}")
        else:
            valid_square = False
            while not valid_square:
                square = input(f"\n{letter}'s turn. Input move (1-9): ")
                try:
                    square = int(square) - 1
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    game.make_move(square, letter)
                except ValueError:
                    print("\nInvalid square. Try again.")

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")

def play_game_ai_vs_ai():

    game = TicTacToe()
    print("\nInitial Board:")
    game.print_board()

    first_move = True

    letter = 'O'  # AI (O) player starts first.
    while game.empty_squares_available():
        if letter == 'O':  # AI (O)'s turn
            if first_move:
                square = random.randint(0, 8)
                first_move = False
            else:
                square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (O) chooses square {square + 1}")
            time.sleep(0.75)
        else:
            square = minimax_with_alpha_beta(game, len(game.available_moves()), -math.inf, math.inf, True, 'O')['position']
            if square is None:
                print("\nGame is a draw!")
                break
            game.make_move(square, letter)
            print(f"\nAI (X) chooses square {square + 1}")
            time.sleep(0.75)

        game.print_board()

        if game.current_winner:
            print(f"\n{letter} wins!")
            break

        letter = 'O' if letter == 'X' else 'X'  # Switch turns.
    else:
        print("\nIt's a draw!")


if __name__ == '__main__':

    print("""
Modes of play available:

    hh: Hooman vs. hooman
    ha: Hooman vs. AI
    ah: AI vs. Hooman - AI makes first move
    aa: AI vs. AI""")

    valid_move = False
    while not valid_move:
        mode = input("\nEnter preferred mode of play (e.g., aa): ")
        try:
            if mode not in ["hh", "ha", "ah", "aa"]:
                raise ValueError
            valid_move = True
            if mode == "hh":
                play_game_human_vs_human()
            elif mode == "ha":
                play_game_human_moves_first()
            elif mode == "ah":
                play_game_ai_moves_first()
            else:
                play_game_ai_vs_ai()
        except ValueError:
            print("\nInvalid option entered. Try again.")

