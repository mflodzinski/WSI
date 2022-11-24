import itertools
from typing import Iterable, List, Optional
from game import Game
from move import Move
from player import Player
from state import State
from magic_square import heurestic_matrix, fillMatrix
import numpy as np

class Pick(Game):
    """Class that represents the Pick game"""
    FIRST_PLAYER_DEFAULT_CHAR = '1'
    SECOND_PLAYER_DEFAULT_CHAR = '2'

    def __init__(self, first_player: Player = None, second_player: Player = None, n: int = 3):
        """
        Initializes game.

        Parameters:
            first_player: the player that will go first (if None is passed, a player will be created)
            second_player: the player that will go second (if None is passed, a player will be created)
            n: the subset size of picked numbers that should sum up to aim value
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)
        state = PickState(self.first_player, self.second_player, n)
        super().__init__(state)

class PickMove(Move):
    """
    Class that represents a move in the PickMove game

    Variables:
        number: selected number (from 1 to n^2)
    """

    def __init__(self, number: int):
        self.number = number

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PickMove):
            return False
        return self.number == o.number


class PickState(State):
    """Class that represents a state in the PickState game"""

    def __init__(self,
                 current_player: Player, other_player: Player, n,
                 current_player_numbers: List[int] = None,
                 other_player_numbers: List[int] = None):
        """Creates the state. Do not call directly."""

        if current_player_numbers is None:
            current_player_numbers = []
        if other_player_numbers is None:
            other_player_numbers = []

        self.current_player_numbers = current_player_numbers
        self.other_player_numbers = other_player_numbers
        self.selected_numbers = set(self.current_player_numbers).union(self.other_player_numbers)
        self.n = n
        self.max_number = n ** 2
        self.aim_value = int((n ** 2 * (n ** 2 + 1)) / (2 * n))
        self.magic_square = fillMatrix(n)
        self.heurestic_square = heurestic_matrix(n)
        super().__init__(current_player, other_player)

    def get_moves(self) -> Iterable[PickMove]:
        return [PickMove(number) for number in range(1, self.max_number + 1) if number not in self.selected_numbers]

    def make_move(self, move: PickMove) -> 'PickState':
        if move.number > self.max_number or move.number in self.selected_numbers:
            raise ValueError("Invalid move")
        else:
            next_player = self._other_player
            next_player_numbers = self.other_player_numbers

            other_player = self._current_player
            other_player_numbers = self.current_player_numbers + [move.number]

        return PickState(
            next_player, other_player, self.n, next_player_numbers, other_player_numbers
        )

    def is_finished(self) -> bool:
        return self._check_if_sums_to_aim_value(self.current_player_numbers) or \
               self._check_if_sums_to_aim_value(self.other_player_numbers) or \
               len(self.selected_numbers) == self.max_number

    def get_winner(self) -> Optional[Player]:
        if not self.is_finished():
            return None
        if self._check_if_sums_to_aim_value(self.current_player_numbers):
            return self._current_player
        elif self._check_if_sums_to_aim_value(self.other_player_numbers):
            return self._other_player
        else:
            return None

    def __str__(self) -> str:
        return f"n: {self.n}, aim_value: {self.aim_value}" \
               f"\nCurrent player: {self._current_player.char}, Numbers: " \
               f"{'[]' if not self.current_player_numbers else sorted(self.current_player_numbers)}," \
               f"\nOther player: {self._other_player.char}, Numbers: " \
               f"{'[]' if not self.other_player_numbers else sorted(self.other_player_numbers)}"

    # below are helper methods for the public interface

    def _check_if_sums_to_aim_value(self, numbers: List[int]) -> bool:
        return self.aim_value in [sum(i) for i in itertools.combinations(numbers, self.n)]
            
    def static_evaluation(self, maximizingPlayer) -> int:
        if self.is_finished():
            if self.get_winner():
                if self.get_winner().char == '1':
                    return 10000
                elif self.get_winner().char == '2':
                    return -10000
                else:
                    raise Exception("asdasdas")
            else:
                return 0
        current_player_indexes, other_player_indexes = self.get_indexes_in_magic_square()
        current_player_corresponding_values = []
        for index in current_player_indexes:
            value = self.heurestic_square[index[0]][index[1]]
            current_player_corresponding_values.append(value)
            
        other_player_corresponding_values = []
        for index in other_player_indexes:
            value = self.heurestic_square[index[0]][index[1]]
            other_player_corresponding_values.append(value)
        
        score = sum(current_player_corresponding_values) - sum(other_player_corresponding_values)
        score = score if maximizingPlayer else -score
        return score

    def get_indexes_in_magic_square(self):
        current_player_indexes = []
        for i in self.current_player_numbers:
            index = np.where(np.array(self.magic_square) == i)
            if index[0].size == 0:
                break
            index = list(zip(index[0], index[1]))
            current_player_indexes.append(*index)
            
        other_player_indexes = []
        for i in self.other_player_numbers:
            index = np.where(np.array(self.magic_square) == i)
            if index[0].size == 0:
                break
            index = list(zip(index[0], index[1]))
            other_player_indexes.append(*index)

        return current_player_indexes, other_player_indexes

            
# game = Pick(n=3)
# game.make_move(PickMove(5))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))

# game.make_move(PickMove(1))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))

# game.make_move(PickMove(3))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))

# game.make_move(PickMove(7-1))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))

# game.make_move(PickMove(9))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))

# game.make_move(PickMove(8))
# char = int(game.state._current_player.char)-1
# print(game.state.static_evaluation(1 - char))