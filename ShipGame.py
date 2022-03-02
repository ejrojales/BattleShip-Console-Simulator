# Author: Emmanuel Rojales
# Github Username: ejrojales
# Date: 2/28/2022
# Description:

class Grid:
    """Represents a player to be added to the ShipGame class."""

    def __init__(self, name):
        """Initializes a player with a name and two grids, one for placing ships and one for keeping track of hits
        and sunk ships. """

        self._name = name
        self._ship_placements = []
        self._num_of_ships = 0
        self._primary_grid = [[" ", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["A"], ["B"], ["C"], ["D"], ["E"], ["F"], ["G"],
                              ["H"], ["I"], ["J"]]
        for i in range(1 ,11):
            for y in range(10):
                self._primary_grid[i].append(" ")
        # self._tracking_grid = [[" ", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["A"], ["B"], ["C"], ["D"], ["E"], ["F"], ["G"],
        #                        ["H"], ["I"], ["J"]]
        # for i in range(1 ,11):
        #     for y in range(10):
        #         self._tracking_grid[i].append(" ")

    # def get_primary_grid(self):
    #     """Return the player's grid with ships placed on it."""
    #
    #     return self._primary_grid

    # def get_tracking_grid(self):
    #     """Return the grid with a record of hits and sunk ships."""
    #
    #     return self._tracking_grid

    def set_ships(self, length, position, orientation):
        """
        Places a ship on a player's primary grid. Call's the Player object's set_primary_grid().

        :param (int) length: Length of ship.
        :param (str) position: Coordinate on board closest to A1 to place the ship.
        :param (str) orientation: Either 'R' or "C". Determines the orientation of the ship.
        :return: False if ship length less than 2, overlaps a previously placed ship, or ship is out of bounds of grid.
                 True otherwise.
        """

        if length < 2 or length > 10:
            return False

        character = position[:1]
        letter = 0
        num = int(position[1:])

        for row in range(1, 11):
            if character in self._primary_grid[row]:
                letter = row
                break

        if orientation == 'C':
            # Check if there is an overlapping ship or will go out of bounds.
            temp_letter = letter
            for cell in range(length):
                if "X" in self._primary_grid[temp_letter][num]:
                    return False
                if temp_letter == 10 and length - cell > 1:
                    return False
                temp_letter += 1

            self._num_of_ships += 1
            self._ship_placements.append([])
            # Place ship
            for ship in range(length):
                self._primary_grid[letter][num] = "X"
                letter += 1
                self._ship_placements[len(self._ship_placements) - 1].append(f"{character}{num}")
                character = ord(character)
                character += 1
                character = chr(character)
            return True
        elif orientation == 'R':
            # Check if there is an overlapping ship or will go out of bounds.
            temp_num = num
            for cell in range(length):
                if "X" in self._primary_grid[letter][temp_num]:
                    return False
                if temp_num == 10 and length - cell > 1:
                    return False
                temp_num += 1

            # Place ship
            self._num_of_ships += 1
            self._ship_placements.append([])
            for ship in range(length):
                self._primary_grid[letter][num] = "X"
                self._ship_placements[len(self._ship_placements) - 1].append(f"{character}{num}")
                num += 1
            return True

    def set_primary_grid(self, position):
        """
        Updates the player's primary grid to reflect a hit on a ship.

        :param (str) position: The coordinate on the grid.
        :return:
        """

        character = position[:1]
        letter = 0
        num = int(position[1:])

        for row in range(1, 11):
            if character in self._primary_grid[row]:
                letter = row
                break

        if self._primary_grid[letter][num] == "X":
            self._primary_grid[letter][num] = " "

            for ship in self._ship_placements:
                if position in ship:
                    ship.remove(position)
                if len(ship) == 0:
                    self._ship_placements.remove(ship)
                    self._num_of_ships -= 1

    def get_num_of_ships(self):
        """Return the number of ships a player has left."""

        return self._num_of_ships

    def display_grid(self):
        for row in self._primary_grid:
            for col in row:
                print(col, end=" ")
            print()


class ShipGame:
    """Represents the Battleship Game."""

    def __init__(self):
        """
        Initializes the game with two players, 'first' and 'second'. Both players have empty grids. The game state
        is initialized to "UNFINISHED".
        """
        self._players = {
            'first': Grid('first'),
            'second': Grid('second')
        }
        self._current_turn = 'first'
        self._current_state = 'UNFINISHED'

    def place_ship(self, player, length, position, orientation):
        """
        Places a ship on a player's primary grid. Call's the Player object's set_primary_grid().

        :param (str) player: Either 'first' or 'second'.
        :param (int) length: Length of ship.
        :param (str) position: Coordinate on board closest to A1 to place the ship.
        :param (str) orientation: Either 'R' or "C". Determines the orientation of the ship.
        :return: False if ship length less than 2, overlaps a previously placed ship, or ship is out of bounds of grid.
                 True otherwise.
        """

        return self._players[player].set_ships(length, position, orientation)

    def get_current_state(self):
        """"""

        return self._current_state

    def fire_torpedo(self, turn, position):
        """

        :param (str) turn: Either 'first' or 'second'.
        :param (str) position: A coordinate on the grid.
        :return: False if not the player's turn or if the game has already been won. True otherwise.
        """

        if turn != self._current_turn or self._current_state != 'UNFINISHED':
            return False
        else:

            winner = None

            for player in self._players:
                if player != turn:
                    self._current_turn = player
                    self._players[player].set_primary_grid(position)
                    if self._players[player].get_num_of_ships() == 0:
                        winner = turn

            if winner == 'first':
                self._current_state = 'FIRST_WON'
            elif winner == 'second':
                self._current_state = 'SECOND_WON'

            return True

    def get_num_ships_remaining(self, player):
        """
        Return the total number of times a player has successfully called place_ship().

        :param (str) player: Either 'first' or 'second'.
        :return (int): The total number of ships placed.
        """

        return self._players[player].get_num_of_ships()
