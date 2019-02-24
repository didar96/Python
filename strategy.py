"""
A module for strategies.

"""
from typing import Any


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
