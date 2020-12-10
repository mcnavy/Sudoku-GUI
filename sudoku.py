board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
import pygame
import time
import copy

class Sudoku:

	def __init__(self,board,width,height):

		self.width = width
		self.height = height
		self.original_board = copy.deepcopy(board)
		self.board = copy.deepcopy(board)
		self.size = 9
		self.cell_size = self.width // self.size
		self.original = [[self.board[i][j] !=0 for j in range(self.size)] for i in range(self.size)]
		self.selected = None
	def click(self,pos):
		x,y = pos[0],pos[1]

		if x < self.width and y < self.height:
			x,y = x // self.cell_size, y // self.cell_size

			self.selected = (y*self.cell_size,x*self.cell_size)
			return (x,y)


	def can_place_value(self,row,col,value):
		for number in self.board[row]:
			if number == value:
				return False
		for idx in range(self.size):
			if self.board[idx][col] == value:
				return False
		box_x, box_y = col // 3, row // 3

		for r in range(box_y*3,box_y*3+3):
			for c in range(box_x*3,box_x*3+3):
				if self.board[r][c] == value:
					return False
		return True
	def solve_from_cell(self,row,col):	
		if col == self.size:
			col = 0
			row +=1
			if row == self.size:
				return True
		empty = 0

		if self.board[row][col] != empty:
			return self.solve_from_cell(row,col+1)	
		for value in range(1,10):

			if self.can_place_value(row,col,value):
				self.board[row][col] = value
				if self.solve_from_cell(row,col+1):
					return True
				self.board[row][col] = empty
		return False
	def solve(self):
		self.solve_from_cell(0,0)
	def make_grid(self,WIN):
		for i in range(self.size+1):
			if i % 3 == 0 and i!=0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(WIN,(0,0,0),(0,i*self.cell_size),(self.width,i*self.cell_size),thick)
			pygame.draw.line(WIN,(0,0,0),(i*self.cell_size,0),(i*self.cell_size,self.height),thick)
	def draw_board(self,WIN):
		font = pygame.font.SysFont('arial',self.cell_size-10)
		for y in range(self.size):
			for x in range(self.size):
				if self.board[y][x] != 0:
					text = font.render(str(self.board[y][x]),True,(0,0,0))
					WIN.blit(text,(x*self.cell_size+10,y*self.cell_size))
		if self.selected:
			pygame.draw.rect(WIN,(255,0,0),(self.selected[1],self.selected[0],self.cell_size,self.cell_size),3)
	def place_value(self,x,y,value):
		if x < self.width and y < self.height:

			x,y = x // self.cell_size, y // self.cell_size
			if self.can_place_value(y,x,value) and not self.original[y][x]:
				self.board[y][x] = value
	def run(self):
		key = None
		run = True
		pygame.init()
		clock = pygame.time.Clock()
		bg_color = (255,255,255)
		WIN = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption('Sudoku')
		while run:
			WIN.fill(bg_color)

			self.make_grid(WIN)
			self.draw_board(WIN)
			clock.tick(10)			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					
				if event.type == pygame.MOUSEBUTTONUP:
					x,y = pygame.mouse.get_pos() 
					self.click((x,y))
					
					
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						key = 1
					if event.key == pygame.K_2:
						key = 2
					if event.key == pygame.K_3:
						key = 3
					if event.key == pygame.K_4:
						key = 4
					if event.key == pygame.K_5:
						key = 5
					if event.key == pygame.K_6:
						key = 6
					if event.key == pygame.K_7:
						key = 7
					if event.key == pygame.K_8:
						key = 8
					if event.key == pygame.K_9:
						key = 9
					if event.key == pygame.K_SPACE:
						print('')
						self.board = self.original_board
						self.solve()
			if self.selected and key != None:
				self.place_value(x,y,key)
				key = None
			pygame.display.update()
			


						

					
game = Sudoku(board,540,540)
game.run()
pygame.quit()