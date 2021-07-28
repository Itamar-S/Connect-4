# Importing the colored function from the termcolor libery for multicolored board
# Then importing the choice function from the random libery for the Random player
# Finally importing the inf const from the math library for the Alpha Beta Pruning (to economize the maximum and minimum score calculation)
from termcolor import colored
from random import choice
from math import inf


class Board:
	"""
	A class used to represent a board
	
	...

	Methods
	-------
	clone()
		Returns a copy of the board
	to_string()
		Returns the board as a multicolored string
	place_mark(marker, col)
		Placing a marker in the board at the given column
	legal_move(col)
		Returns a boolean value indicating whether the move is legal
	is_winner(marker)
		Returns a boolean value indicating whether the given marker is a winner
	check_lines(marker, n)
		Returns the number of lines that complex from the given marker in length of n
	is_draw()
		Returns a boolean value indicating whether there is a tie
	get_score(player)
		Returns an integer value indicating the score of the board for the given player
	"""

	def __init__(self):
		"""The constructor method creates an empty board using list comprehension"""
		self.board = [['_' for j in range(6)] for i in range(7)]

	def clone(self):
		"""The clone method returns a copy of the board"""
		# Creating a new empty Board object
		clone = Board()
		# Using a nested loop every cell in the new board accepts the value of the original board's cell
		for col in range(7):
			for row in range(6):
				clone.board[col][row] = self.board[col][row]
		return clone

	def to_string(self):
		"""Returns a string representation of the board"""
		# Creating the top row of the board
		board_string = '_____________________________\n'
		# Using nested loop for every row the loop going through all the columns
		for row in range(6):
			for col in range(7):
				if self.board[col][row] == '_':
					"""In case the cell is empty
					
					If the cell is empty (represented by a underscore)
					we add to the board_string a vertical bar, a starting underscore,
					the empty cell's sign (another underscore) and a ending underscore.
					"""
					board_string += '|___'
				else:
					"""
					Otherwise we add to the board_string a vertical bar, a starting underscore,
					a circle ('●') that colored (with the colored function)
					in red if the marker is 'X' else yellow
					and a ending underscore.
					"""
					board_string += '|_' + colored('●', 'red' if self.board[col][row] == 'X' else 'yellow') + '_'
			# In the end of every row we add to the board_string a vertical bar
			# and a new line sign ('\n') except if it is the last row.
			board_string += '|\n' if row < 5 else '|'
		return board_string

	def place_mark(self, marker, col):
		"""Adding to the given column the given marker.

		Parameters
        ----------
		marker : str
			The marker that will be placed
		col : int
			The column to which the marker will be added
		
		Raises
        ------
		ValueError
			If the given column is not in the range of 0-6.
		
		Returns
    	-------
		boolean
			a boolean value indicating if the marker's owner winned
		"""

		if col < 0 or col > 6:
			raise ValueError()
		# The lopp is going from the bottom of the column to the to the top
		for row in range(5, -1, -1):
			# For every cell in column, if the cell is empty we set his value to the given marker and break the loop 
			if self.board[col][row] == '_':
				self.board[col][row] = marker
				break
		return self.is_winner(marker)

	def legal_move(self, col):
		"""Check if there is an empty cell in the given column

		Parameters
        ----------
		col : int
			The column that need to check legality

		Returns
    	-------
		boolean
			a boolean value indicating if there is an empty cell in the given column
		"""

		# The method checks by checking the top cell in column, if it is empty, the move is legal.
		return self.board[col][0] == '_'

	def is_winner(self, marker):
		"""Checks if the given marker is a winner
		
		Parameters
        ----------
		marker : str
			The marker that we check to see if he is a winner

		Returns
    	-------
		boolean
			a boolean value indicating if the given marker is a winner
		"""

		# The method checks using the check_lines method (that count lines),
		# that get the given marker and 4 (the length of a winning streak).
		return self.check_lines(marker, 4)

	def check_lines(self, marker, n):
		"""Checks the number of lines of a given marker in length of n

		Parameters
        ----------
		marker : str
			The marker that will be checked in the method
		n: int
			The length of the lines that will search
		
		Raises
        ------
		IndexError
			If the search index is negative.
		
		Returns
    	-------
		int
			the number of lines found of the given marker in length of n
		"""

		# Creating a nested tuple of four directions (right, down, right-down, left-down)
		directions = (((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 1), (2, 2), (3, 3)), ((0, 0), (-1, 1), (-2, 2), (-3, 3)))
		num_of_lines = 0
		# Using a nested loop that iterates over all the cells
		for col in range(7):
			for row in range(6):
				# For every cell in the board, we are going through all the directions
				for direction in directions:
					# We creating a list of the cells in the current direction 
					markers_list = []
					# For every cell in the direction, we are adding it to the list
					for i in range(4):
						try:
							current_col = col + direction[i][0]
							current_row = row + direction[i][1]
							# If the cell is negative, we exit from the loop
							if current_col < 0 or current_row < 0:
								raise IndexError 
							markers_list.append(self.board[current_col][current_row])
						except IndexError:
							# If the cell index is invalid (e.g. column 9), we exit from the loop
							break
					else:
						"""Checking list of cells

						If all the cells are valid, we check the number of given marker apparitions,
						if the number of apparitions is equal to n 
						and there isn't any opponent marker in the list
						we add to the num_of_lines variable one.
						"""
						if markers_list.count(marker) == n and markers_list.count(marker) + markers_list.count('_') == 4:
							num_of_lines += 1

		return num_of_lines

	def is_draw(self):
		"""Checks if there is a legal move in the board

		Returns
    	-------
		boolean
			returns a boolean value indicating whether there is a legal move in the board
		"""

		# Using a loop the method checks if there is a legal move in the board
		for col in range(7):
			if self.legal_move(col):
					return False
		return True
	
	def get_score(self, player):
		"""Returns the score of the board for a given player

		Parameters
        ----------
		player : Player
			The player that will receive the score of the board for him

		Returns
    	-------
		int
			an integer value representing the score of the board for the given player
		"""

		board_score = 0

		# Adding two points for every line in length of 2, of the given player
		board_score += self.check_lines(player.marker, 2) * 2
		# Adding five points for every line in length of 3, of the given player
		board_score += self.check_lines(player.marker, 3) * 5

		# Subtract two points for every line in length of 2, of the opponent player
		board_score += self.check_lines(player.opponent_marker, 2) * -2
		# Subtract hundred points for every line in length of 3, of the opponent player
		board_score += self.check_lines(player.opponent_marker, 3) * -100

		return board_score


class Player:
	"""
	A class used to represent a player

	...

	Attributes
	----------
	name : str
		the name of the player
	marker : str
		the marker of the player
	opponent_marker : str
		the marker of the opponent player

	Methods
	-------
	make_move(board)
		Asking the player to make a legal move
	"""
	def __init__(self, name, marker, opponent_marker):
		"""
        Parameters
        ----------
        name : str
			the name of the player
		marker : str
			the marker of the player
		opponent_marker : str
			the marker of the opponent player
        """

		self.name = name
		self.marker = marker
		self.opponent_marker = opponent_marker

		def make_move(self, board):
			"""Asks the player to make a move

			Parameters
			----------
			board : Board
				the current board

			Returns
			-------
			int
				the column that the player selected
			"""

			# Asking the player to make a move
			move = input(f'This is the current board, {self.name} please make a move 1-7\n')
			# If the player wrote AI, so the computer helps him in the game
			if move.lower() == 'ai':
				# We creates a temporary computer object to do a move for the player
				computer_player = Computer(self.name, self.marker, self.opponent_marker)
				return computer_player.make_move(board)
			else:
				# Otherwise, we return the move that the human player wrote
				move = int(move) - 1
			while True:
				# If the move is legal, so the method returns it.
				if board.legal_move(move):
					return move
				# Otherwise, the method asks the player again, until he returns a valid answer.
				else:
					# Like before, the method asks the player to make a move, and the player can answer 'AI'
					move = input('Illegal move, please try again.\n')
					if move.lower() == 'ai':
						computer_player = Computer(self.name, self.marker, self.opponent_marker)
						return computer_player.make_move(board)
					else:
						move = int(move) - 1


class Random(Player):
	"""
	A class used to represent a player that make random moves (inheritor the Player object)

	...

	Attributes
	----------
	name : str
		the name of the random player
	marker : str
		the marker of the random player
	opponent_marker : str
		the marker of the opponent player

	Methods
	-------
	make_move(board)
		Make a random move using the choice function from the random library
	"""

	def __init__(self, name, marker, opponent_marker):
		"""
		Parameters
        ----------
        name : str
			the name of the player
		marker : str
			the marker of the player
		opponent_marker : str
			the marker of the opponent player
		"""

		Player.__init__(self, name, marker, opponent_marker)

	def make_move(self, board):
		"""Choosing a random move

		Parameters
        ----------
		board : Board
			the current board
		"""
		options = [_ for _ in range(7) if board.legal_move(_)]
		return choice(options)


class Computer(Player):
	"""
	A class used to represent a computer player (inheritor the Player object)

	...

	Parameters
	----------
	name : str
		the name of the player
	marker : str
		the marker of the player
	opponent_marker : str
		the marker of the opponent player
	"""

	def __init__(self, name, marker, opponent_marker):
		"""
		Parameters
        ----------
        name : str
			the name of the player
		marker : str
			the marker of the player
		opponent_marker : str
			the marker of the opponent player
		"""

		Player.__init__(self, name, marker, opponent_marker)

	def score_move(self, board, i, depth, alpha, beta, turn=True):
		"""Returns the score of given move

		Parameters
        ----------
        board : Board
			the current board
		i : int
			the column that will placed a marker into it
		depth : int
			The number of moves the computer will think ahead
		alpha : int, float
			The minimum score that achieved
		beta : int, float
			The minimum score that achieved
		turn : boolean, optional
			the current player (True mean current player and False mean opponent player)
		
		Returns
    	-------
		intger
			a intger value indicating the score of the board for the current player
		"""

		# Creating a copy of the board
		new_board = board.clone()
		
		# Place a mark at column i in the board clone
		new_board.place_mark(self.marker if turn else self.opponent_marker, i)
		
		# Checking winning and tie
		if new_board.is_winner(self.marker):
			return inf
		elif new_board.is_winner(self.opponent_marker):
			return -inf
		elif new_board.is_draw():
			return 0
		# If the depth is 0, the method return a score of the board
		elif depth == 0:
			return new_board.get_score(self)
		else:
			# Otherwise, the method think move ahead
			
			# The method creates a list of possible moves
			options = []
			# The method iterates over all the columns
			for i in range(7):
				if new_board.legal_move(i):
					# Just if the move is legal the method add to the options list the score of the move
					# In the recursive call the depth is subtract by one and the turn flips over
					test = self.score_move(new_board, i, depth - 1, alpha, beta, not turn)
					# If the move is in the middle column, we add to the score 4 points
					if i == 3:
						test += 4
					options.append(test)
					# Alpha Beta Pruning
					if not turn:
						if max(options) >= beta:
							return max(options)
						if max(options) > alpha:
							alpha = max(options)
					else:
						if min(options) <= alpha:
							return min(options)
						if min(options) < beta:
							beta = min(options)
			# Returns the minimum score if turn, otherwise returns the maximum score
			return min(options) if turn else max(options)

	def make_move(self, board):
		"""Searches for the best move
		
		Parameters
        ----------
        board : Board
			the current board
		
		Returns
    	-------
		int
			the column that gives the maximum score
		"""

		# Creating a possible moves list
		moves = []
		# Iterating all the columns
		for i in range(7):
			if board.legal_move(i):
				# If the move is legal, then we add a tuple of the score of the move 
				# and the column to the moves list
				if i == 3:
					# If the column is the middle column, we add 4 points to the score
					moves.append((self.score_move(board, i, 4, -inf, inf) + 4, i))
				else:
					moves.append((self.score_move(board, i, 4, -inf, inf), i))
		# By sorting the list we get a list that sorted from the lowest to highest score
		# then we choose the the highest score column
		return sorted(moves)[-1][1]


def main():
	"""The main function that runs the game"""
	# Setting the first player
	turn = False
	# Creating a board object
	board = Board()
	# Creating a list of players
	players = [Player('Bob', 'X', 'O'), Computer('Alice', 'O', 'X')]

	while True:
		# Setting the current player using the turn variable
		current_player = players[int(turn)]
		# Prints the board as a string
		print(board.to_string())
		print('\n')
		# The current player makes a move
		move = current_player.make_move(board)
		# Place a mark in the board
		is_winning = board.place_mark(current_player.marker, move)
		# If someone won or there is a tie, then the game is over (using break, to exit the loop)
		if is_winning or board.is_draw():
			break
		# The turn variable flips over
		turn = not turn

	# When the game is over, if nobody winned (there is a tie)
	if board.is_draw():
		print('No one wins:')
	# Otherwise, we prints a message saying who did winned
	else:
		print(f'Congratulations {current_player.name}, you win:')
	# Finally, we print the final board
	print(board.to_string())


if __name__ == "__main__":
	main()
