# -*- coding: utf-8 -*-

"""Command line program for solving Sudoku puzzles."""

import time
from typing import List


class Board:
    """Resembles a Sudoku board."""

    def __init__(self, board: List[List[int]]) -> None:
        """Initialize a Sudoku board.
        
        :param board: A 9x9 grid of integers. Use 0 for empty cells.
        :type board: List[List[int]]
        """
        # check if board is a 9x9 grid
        assert len(board) == 9, 'board must have 9 rows'
        assert all(len(row) == 9 for row in board), 'each row must have 9 columns'

        # check if all values are between 0 and 9
        assert all(0 <= value <= 9 for row in board for value in row), 'values must be between 0 and 9'

        self._board = board

    def __str__(self) -> str:
        """Return a string representation of the board.
        
        :return: A string representation of the board.
        :rtype: str
        """
        # print with a '|' separator every 3 columns, and a '-' separator every 3 rows
        rows = []
        for i, row in enumerate(self._board):
            if i % 3 == 0 and i != 0:
                rows.append('-' * 21)
            
            formatted_row = ' | '.join(
                ' '.join(str(value) if value != 0 else '.' for value in row[j:j + 3])
                for j in range(0, 9, 3)
            )

            rows.append(formatted_row)
            
        
        return '\n'.join(rows)
    
    def is_valid(self) -> bool:
        """Check if the board is valid.
        
        :return: True if the board is valid, False otherwise.
        :rtype: bool
        """
        return (
            self._is_valid_rows() 
            and self._is_valid_columns() 
            and self._is_valid_squares()
        )
    
    def _is_valid_rows(self) -> bool:
        """Check if all rows are valid.
        
        :return: True if all rows are valid, False otherwise.
        :rtype: bool
        """
        return all(self._is_valid(row) for row in self._board)
    
    def _is_valid_columns(self) -> bool:
        """Check if all columns are valid.
        
        :return: True if all columns are valid, False otherwise.
        :rtype: bool
        """
        return all(self._is_valid(column) for column in self._get_columns())
    
    def _is_valid_squares(self) -> bool:
        """Check if all squares are valid.
        
        :return: True if all squares are valid, False otherwise.
        :rtype: bool
        """
        return all(self._is_valid(square) for square in self._get_squares())
    
    def _is_valid(self, values: List[int]) -> bool:
        """Check if a list of values is valid.
        
        :param values: A list of integers.
        :type values: List[int]
        :return: True if the list of values is valid, False otherwise.
        :rtype: bool
        """
        non_zero_values = [value for value in values if value != 0]
        return len(set(non_zero_values)) == len(non_zero_values)
    
    def _get_columns(self) -> List[List[int]]:
        """Return a list of columns.
        
        :return: A list of columns.
        :rtype: List[List[int]]
        """
        return [[row[i] for row in self._board] for i in range(9)]
    
    def _get_squares(self) -> List[List[int]]:
        """Return a list of squares.
        
        :return: A list of squares.
        :rtype: List[List[int]]
        """
        return [
            [
                self._board[i + k][j + l] 
                for k in range(3) 
                for l in range(3)
            ] 
            for i in range(0, 9, 3) 
            for j in range(0, 9, 3)
        ]
    
    def set_value(self, row: int, column: int, value: int) -> None:
        """Set a value on the board.
        
        :param row: The row index.
        :type row: int
        :param column: The column index.
        :type column: int
        :param value: The value to set.
        :type value: int
        """
        self._board[row][column] = value

    def get_value(self, row: int, column: int) -> int:
        """Get a value from the board.
        
        :param row: The row index.
        :type row: int
        :param column: The column index.
        :type column: int
        :return: The value at the specified cell.
        :rtype: int
        """
        return self._board[row][column]

    def is_finished(self) -> bool:
        """Check if the board is finished.
        
        :return: True if the board is finished, False otherwise.
        :rtype: bool
        """
        return (
            all(value != 0 for row in self._board for value in row)
            and self.is_valid()
        )
    
    def valid_values(self, row: int, column: int) -> List[int]:
        """Return a list of valid values for a cell.
        
        :param row: The row index.
        :type row: int
        :param column: The column index.
        :type column: int
        :return: A list of valid values for the cell.
        :rtype: List[int]
        """
        original_value = self.get_value(row, column)

        valid_values = []
        for value in range(1, 10):
            self.set_value(row, column, value)
            if self.is_valid():
                valid_values.append(value)
        
        self.set_value(row, column, original_value)

        return valid_values
    

def solve(board: Board) -> Board:
    """Solve a Sudoku board.
    
    :param board: A Sudoku board.
    :type board: Board
    :return: A solved Sudoku board.
    :rtype: Board

    .. note:: This function uses a backtracking algorithm. 
    .. note:: This function modifies the input board in place.
    """
    if board.is_finished():
        return board
    
    for row in range(9):
        for column in range(9):
            if board.get_value(row, column) == 0:
                for value in board.valid_values(row, column):
                    board.set_value(row, column, value)
                    if solve(board):
                        return board
                    board.set_value(row, column, 0)
                
                return None
                


def main() -> None:
    """Main function."""
    board = Board([
        [0, 0, 7, 0, 8, 0, 4, 0, 2],
        [0, 0, 9, 0, 5, 0, 0, 0, 0],
        [0, 8, 0, 0, 7, 4, 5, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 1, 0, 0, 5, 0, 2, 0],
        [4, 9, 0, 8, 0, 7, 0, 5, 0],
        [7, 3, 4, 5, 1, 6, 2, 9, 8],
        [0, 0, 6, 0, 2, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert board.is_valid(), 'initial board is not valid'

    print('Initial board:')
    print(board)

    start_time = time.time()
    solve(board)
    end_time = time.time()

    print(f'\nSolved board (in {end_time - start_time:.2f} seconds):')
    print(board)


if __name__ == '__main__':
    main()
