"""
An implementation of Stonehenge.

"""
from typing import Any
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                          to make a move.
        :type p1_starts: bool
        """
        self.length = int(input("Enter the side length of the board: "))
        self.current_state = StonehengeState(p1_starts, board(self.length))

    def get_instructions(self):
        """
        Return the instructions for this Game.

        :return: The instructions for this Game.
        :rtype: str
        """
        instructions0 = "Players take turns claiming cells. When a player captures "
        instructions1 = "at least half of the cells in a ley-line, then the player "
        instructions2 = "captures that ley-line. The first player to capture at least "
        instructions3 = "half of the ley-lines is the winner. "
        instructions = "A ley-line, once claimed, cannot be taken by the other player."

        return (instructions0 + "\n" + instructions1 + "\n" + instructions2 + "\n" +
                instructions3 + "\n" + instructions)

    def is_over(self, state):
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        list1 = []
        list2 = []
        lines_list = [horizontal(self.length, state.board),
                      top_left(self.length, state.board),
                      top_right(self.length, state.board)]
        for element in lines_list:
            for element1 in element[:-1]:
                if element1[0] == '1':
                    list1.append(1)
                elif element1[0] == '2':
                    list2.append(2)
        if len(list1) >= (len(lines_list[0])-1)*1.5:
            result = True
        elif len(list2) >= (len(lines_list[0])-1)*1.5:
            result = True
        else:
            result = False
        return result

    def is_winner(self, player):
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        :param player: The player to check.
        :type player: str
        :return: Whether player has won or not.
        :rtype: bool
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string):
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.

        :param string:
        :type string:
        :return:
        :rtype:
        """
        if string.strip().isdigit():
            return -1

        return string.strip().upper()


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, board: str) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.board = board
        self.length = side_length(self.board)
        self.ley_lines = [horizontal(self.length, self.board),
                          top_left(self.length, self.board),
                          top_right(self.length, self.board)]
        self.lst = self.board.split("\n")

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return self.board

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        moves = []
        for move in self.board:
            if move.isalpha():
                moves.append(move)
        return moves

    def make_move(self, move: Any) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.
        """

        for ley_line2 in self.ley_lines:
            for ley_line1 in ley_line2[:-1]:
                l_index = 0
                p1_count = 0
                p2_count = 0
                for element in ley_line1:
                    if element == move:
                        if self.get_current_player_name() == "p1":
                            ley_line1[l_index] = '1'
                        else:
                            ley_line1[l_index] = '2'
                    else:
                        l_index += 1
                if ley_line1[0] == "@":
                    for num in ley_line1:
                        if num == '1':
                            p1_count += 1
                            if p1_count >= (len(ley_line1) - 1) * 0.5:
                                ley_line1[0] = '1'
                        elif num == '2':
                            p2_count += 1
                            if p2_count >= (len(ley_line1) - 1) * 0.5:
                                ley_line1[0] = '2'
            cells = 3
            if ley_line2[-1] == 1:
                count = 0
                row_index = 2
                str_index = (self.length*2) - 2
            elif ley_line2[-1] == 2:
                count = 0
                row_index = (self.length*2) - 2
                str_index = 6
                for i in range(self.length):
                    str_index += 4
            else:
                count = 0
                row_index = (self.length*2) + 4
                str_index = 8
            temp_str = str_index
            ley_line = 0
            temp_row = row_index
            for a in range(self.length + 1):
                str_index = temp_str
                ll_index = 0
                row_index = temp_row
                for j in range(cells):
                    element = self.lst[row_index][str_index]
                    if element != ley_line2[ley_line][ll_index]:
                        self.lst[row_index] = self.lst[row_index][:str_index] + str(ley_line2[ley_line][ll_index]) + self.lst[row_index][str_index + 1:]
                    if ley_line2[-1] == 1:
                        str_index += 4
                    elif ley_line2[-1] == 2:
                        row_index += 2
                        str_index -= 2
                    else:
                        row_index -= 2
                        str_index -= 2
                    ll_index += 1
                if ley_line2[-1] == 1:
                    temp_row += 2
                    if count == self.length - 1:
                        cells -= 1
                        temp_str += 2
                    else:
                        cells += 1
                        temp_str -= 2
                        count += 1
                elif ley_line2[-1] == 2:
                    if count == (self.length - 1):
                        cells -= 1
                        temp_str -= 4
                    else:
                        temp_str -= 2
                        cells += 1
                        count += 1
                        temp_row -= 2
                else:
                    if count == (self.length - 1):
                        cells -= 1
                        temp_str += 2
                        temp_row -= 2
                    else:
                        temp_str += 4
                        count += 1
                        cells += 1
                ley_line += 1
        new_board = "\n".join(self.lst)
        new_state = StonehengeState(not self.p1_turn, new_board)
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1's Turn: {} - Board: {}".format(self.p1_turn,
                                                  self.board)


alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
space = "  "


def board(side_length):
    alpha_index = 0
    cells = 2
    m = side_length
    mid_rows = ""
    row_count = 1
    char_row1 = space*(m+2) + "@   @" + "\n" + space*(m+1) + " /   /" + "\n"
    for i in range(side_length):
        row = ""
        for j in range(cells):
            row += alpha[alpha_index] + " - "
            alpha_index += 1
        row = space*(side_length-1) + "@ - " + row[:-3] + "   @" + "\n"
        char_rows = space*side_length + " " + "/ \ "*cells + "/" + "\n"
        if row_count == m:
            mid_rows += row[:-4] + "\n" + "     " + char_rows[5:-2] + "\n"
        else:
            mid_rows += row + char_rows
            row_count += 1
        side_length -= 1
        cells += 1
    row = ""
    for a in range(m):
        row += alpha[alpha_index] + " - "
        alpha_index += 1
    row = "  " + "@ - " + row[:-3] + "   @" + "\n"
    char_row3 = "       " + "\   "*m + "\n" + "        " + "@   "*m
    return char_row1 + mid_rows + row + char_row3

# horizontal ley lines


def horizontal(side_length, b):
    lst = b.split("\n")
    row_index, cells = 2, 3
    str_index = (side_length*2) - 2
    temp_str = str_index
    horizontal_ley_lines = []
    for i in range(side_length + 1):
        ley_line = []
        str_index = temp_str
        for j in range(cells):
            element = lst[row_index][str_index]
            ley_line.append(element)
            str_index += 4
        row_index += 2
        if row_index == (side_length*2) + 2:
            cells -= 1
            temp_str += 2
        else:
            cells += 1
            temp_str -= 2
        horizontal_ley_lines.append(ley_line)
    return horizontal_ley_lines + [1]


# top left ley-lines
def top_left(side_length, b):
    lst = b.split("\n")
    cells, count = 3, 0
    row_index = (side_length*2) - 2
    str_index = 6
    for i in range(side_length):
        str_index += 4
    temp_str, temp_row = str_index, row_index
    topleft_ley_lines = []
    for j in range(side_length + 1):
        ley_line = []
        str_index = temp_str
        row_index = temp_row
        for i in range(cells):
            element = lst[row_index][str_index]
            ley_line.append(element)
            row_index += 2
            str_index -= 2
        if count == (side_length - 1):
            cells -= 1
            temp_str -= 4
        else:
            temp_str -= 2
            cells += 1
            count += 1
            temp_row -= 2
        topleft_ley_lines.append(ley_line)
    return topleft_ley_lines + [2]

# top right ley-lines


def top_right(side_length, b):
    lst = b.split("\n")
    cells, count = 3, 0
    row_index = (side_length*2) + 4
    str_index = 8
    temp_row, temp_str = row_index, str_index
    topright_ley_lines = []
    for i in range(side_length + 1):
        ley_line = []
        row_index = temp_row
        str_index = temp_str
        for i in range(cells):
            element = lst[row_index][str_index]
            ley_line.append(element)
            row_index -= 2
            str_index -= 2
        if count == (side_length - 1):
            cells -= 1
            temp_str += 2
            temp_row -= 2
        else:
            temp_str += 4
            count += 1
            cells += 1
        topright_ley_lines.append(ley_line)
    return topright_ley_lines + [3]


def side_length(m):
    size = len(m.split("\n"))
    if size == 15:
        result = 5
    elif size == 13:
        result = 4
    elif size == 11:
        result = 3
    elif size == 9:
        result = 2
    else:
        result = 1
    return result


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
