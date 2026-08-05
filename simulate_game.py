import chess
import chess.engine
import random

STOCKFISH_PATH = r"stockfish\stockfish-windows-x86-64-avx2.exe"

def simulate_game(elo_A, elo_B, time_limit=0.01, print_final_board=True):

    engine_A = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    engine_B = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    if random.random() < 0.5:
        white_player, white_elo, engine_white = "A", elo_A, engine_A
        black_player, black_elo, engine_black = "B", elo_B, engine_B
    else:
        white_player, white_elo, engine_white = "B", elo_B, engine_B
        black_player, black_elo, engine_black = "A", elo_A, engine_A

    engine_white.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
    engine_black.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})

    board = chess.Board()
    positions = [board.fen()]
    limit = chess.engine.Limit(time=time_limit)

    while not board.is_game_over():
        move = engine_white.play(board, limit).move if board.turn == chess.WHITE else engine_black.play(board, limit).move
        board.push(move)
        positions.append(board.fen())

    if print_final_board:
        print(board)

    outcome = board.outcome()
    winner_info = None
    numerical_result = 0.5

    if outcome.winner is not None:
        if outcome.winner:
            winner_info = f"Player {white_player} (White)"
            numerical_result = 1 if white_player == "A" else 0
        else:
            winner_info = f"Player {black_player} (Black)"
            numerical_result = 1 if black_player == "A" else 0

    engine_A.quit()
    engine_B.quit()

    return outcome.termination.name, winner_info, numerical_result, positions

if __name__ == "__main__":
    import sys
    import json

    # Default values
    elo_A = 2000
    elo_B = 1800
    time_limit = 0.05

    # Check if command-line arguments for ELOs were provided
    if len(sys.argv) > 2:
        elo_A = int(sys.argv[1])
        elo_B = int(sys.argv[2])
    elif len(sys.argv) == 2:
        print("Please provide both ELOs as arguments.")
        sys.exit(1)

    # Run the game
    termination, winner_info, numerical_result, positions = simulate_game(
        elo_A=elo_A, elo_B=elo_B, time_limit=time_limit, print_final_board=False
    )

    # Output JSON for notebook
    output = {
        "termination": termination,
        "winner_info": winner_info,
        "numerical_result": numerical_result,
        "positions": positions  # Final position in FEN
    }
    print(json.dumps(output))