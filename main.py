from termcolor import colored
from math import inf
import random


class Board:
	def __init__(self):
		self.board = [['_' for j in range(6)] for i in range(7)]

	def clone(self):
		clone = Board()
		for col in range(7):
			for row in range(6):
				clone.board[col][row] = self.board[col][row]
		return clone

	def to_string(self):
		# return '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
		board_string = '_____________________________\n'
		for row in range(6):
			for col in range(7):
				if self.board[col][row] == '_':
					board_string += '|___'
				else:
					board_string += '|_' + colored('●', 'red' if self.board[col][row] == 'X' else 'yellow') + '_'
			board_string += '|\n' if row < 5 else '|'
		return board_string

	def place_mark(self, marker, col):
		if col < 0 or col > 6:
			raise ValueError()
		for row in range(5, -1, -1):
			if self.board[col][row] == '_':
				self.board[col][row] = marker
				break
		return self.is_winner(marker)

	def legal_move(self, col):
		return self.board[col][0] == '_'

	def is_winner(self, marker):
		return self.check_lines(marker, 4) >= 1
	
	def check_lines(self, marker, n):
		directions = (((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 1), (2, 2), (3, 3)), ((0, 0), (-1, 1), (-2, 2), (-3, 3)))
		num_of_lines = 0
		for col in range(7):
			for row in range(6):
				for direction in directions:
					markers_list = []
					for i in range(4):
						try:
							current_col = col + direction[i][0]
							current_row = row + direction[i][1]
							if current_col < 0 or current_row < 0:
								raise IndexError 
							markers_list.append(self.board[current_col][current_row])
						except IndexError:
							break
					else: 
						if markers_list.count(marker) >= n and markers_list.count(marker) + markers_list.count('_') == 4:
							num_of_lines += 1

		return num_of_lines

	def is_draw(self):
		for col in range(7):
			if self.legal_move(col):
					return False
		return True
	
	def get_score(self, player):
		board_score = 0
		
		board_score += self.check_lines(player.marker, 2) * 2
		board_score += self.check_lines(player.marker, 3) * 5

		board_score += self.check_lines(player.opponent_marker, 2) * -2
		board_score += self.check_lines(player.opponent_marker, 3) * -100

		return board_score


class Player:
	def __init__(self, name, marker, opponent_marker):
		self.name = name
		self.marker = marker
		self.opponent_marker = opponent_marker

	def make_move(self, board):
		move = int(input(f'This is the current board, {self.name} please make a move 1-7\n')) - 1
		while True:
			if board.legal_move(move):
				return move
			else:
				move = int(input('Illegal move, please try again.\n')) - 1


class Random(Player):
	def make_move(self, board):
		from random import choice
		options = [_ for _ in range(7) if board.legal_move(_)]
		return choice(options)


class Computer(Player):
	def score_move(self, board, i, depth, alpha, beta, turn=True):
		new_board = board.clone()
		
		try:
			new_board.place_mark(self.marker if turn else self.opponent_marker, i)
		except ValueError:
			return None
		
		if new_board.is_winner(self.marker):
			return inf
		elif new_board.is_winner(self.opponent_marker):
			return -inf
		elif new_board.is_draw():
			return 0
		elif depth == 0:
			return new_board.get_score(self)
		else:
			options = []
			for i in range(7):
				if new_board.legal_move(i):
					test = self.score_move(new_board, i, depth - 1, alpha, beta, not turn)
					if i == 3:
						test += 4
					options.append(test)
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
			return min(options) if turn else max(options)

	def make_move(self, board):
		moves = []
		for i in range(7):
			if board.legal_move(i):
				moves.append((self.score_move(board, i, 4, -inf, inf), i))
		return sorted(moves)[-1][1]


turn = False
board = Board()
players = [Player('Bob', 'X', 'O'), Computer('Alice', 'O', 'X')]

while True:
	current_player = players[int(turn)]
	print(board.to_string())
	print('\n')
	move = current_player.make_move(board)
	is_winning = board.place_mark(current_player.marker, move)
	if is_winning or board.is_draw():
		break
	turn = not turn

if board.is_draw():
	print('No one wins:')
else:
	print(f'Congratulations {current_player.name}, you win:')
print(board.to_string())
