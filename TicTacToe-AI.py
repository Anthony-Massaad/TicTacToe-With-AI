import pygame
from enum import Enum

class Color(Enum):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)


class Move(Enum):
	PLAYER_X = "X"
	PLAYER_O = "O"


def render_board_status(display, board, font, square_size):
	for i in range(3):
		for j in range(3):
			if board[i][j] is not None:
				text = font.render(board[i][j], True, Color.BLACK.value) 
				display.blit(text, (j*square_size + 25, i*square_size - 10))


def draw_board(display, game_width, game_height, square_size):
	for i in range(4):
		pygame.draw.line(display, Color.BLACK.value, (1, i * square_size),  (game_width, i * square_size), 3)
		pygame.draw.line(display, Color.BLACK.value, (i*square_size, 1), (i*square_size, game_height), 3)


def draw(display, game_width, game_height, square_size, board, font):
	display.fill(Color.WHITE.value)
	draw_board(display, game_width, game_height, square_size)
	render_board_status(display, board, font, square_size)
	pygame.display.update()
	pygame.time.delay(30)


def checkEquals(a, b, c):
	return a == b and b == c and a is not None


def checkWinner(board):
	winner = None
	#Horizontal
	for i in range(3):
		if checkEquals(board[i][0], board[i][1], board[i][2]):
			winner = board[i][0]            

	#verticals
	for i in range(3):
		if checkEquals(board[0][i], board[1][i], board[2][i]):
			winner = board[0][i]           

	#diagonals 
	if checkEquals(board[0][0], board[1][1], board[2][2]):
		winner = board[0][0]

	if checkEquals(board[2][0], board[1][1], board[0][2]):
		winner = board[2][0]

	#checking for empty slots
	slots = 0
	for row in range(3):
		for col in range(3):
			if board[row][col] is not None:
				slots += 1

	if slots == 9 and winner is None:
		return 'Tie'

	return winner


def best_move(board, scores):
	bestScore = -10000
	move = None
	for rows in range(3):
		for cols in range(3):
			if board[rows][cols] is None:
				board[rows][cols] = Move.PLAYER_O.value
				score = minimax(board, scores, 0, -10000, 10000, False)
				board[rows][cols] = None
				if score > bestScore:
					bestScore = score
					move = (rows, cols)
	return move


def minimax(board, scores, depth, alpha, beta, maximizing):
	win = checkWinner(board)
	if win is not None:
		return scores[win]
	if maximizing:
		bestScore = -10000
		for i in range(3):
			for j in range(3):
				if board[i][j] is None:
					board[i][j] = Move.PLAYER_O.value
					score = minimax(board, scores, depth + 1, bestScore, beta, False)
					board[i][j] = None
					bestScore = max(score, bestScore)   
					if beta <= bestScore:
						break
	else: 
		bestScore = 10000
		for i in range(3):
			for j in range(3):
				if board[i][j] is None:
					board[i][j] = Move.PLAYER_X.value
					score = minimax(board, scores, depth + 1, alpha, bestScore, True)
					board[i][j] = None
					bestScore = min(bestScore, score)
					if bestScore <= alpha:
						break
	return bestScore


if __name__ == "__main__":
	pygame.init()
	GAME_WIDTH = 384
	GAME_HEIGHT = 384
	DISPLAY = pygame.display.set_mode((GAME_WIDTH+2, GAME_HEIGHT+2))
	FONT = pygame.font.SysFont('Arial', 128)
	pygame.display.set_caption("TicTacToe With AI")
	SCORES = {'X': -1, 'O': 1, 'Tie': 0}
	run = True
	board = [
		[None, None, None],
		[None, None, None],
		[None, None, None]
	]
	SQUARE_SIZE = GAME_WIDTH // 3
	player_turn = False 
	
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN and player_turn and checkWinner(board) is None:
				m_x, m_y = pygame.mouse.get_pos()
				row =  m_y // SQUARE_SIZE
				col =  m_x // SQUARE_SIZE
				for i in range(3):
					for j in range(3):
						if i == row and j == col:
							if board[i][j] is None:
								board[i][j] = Move.PLAYER_X.value
								player_turn = not player_turn

		draw(DISPLAY, GAME_WIDTH, GAME_HEIGHT, SQUARE_SIZE, board, FONT)

		if not player_turn and checkWinner(board) is None:
			row, col = best_move(board, SCORES)
			board[row][col] = Move.PLAYER_O.value 
			player_turn = not player_turn
	
	pygame.quit()
