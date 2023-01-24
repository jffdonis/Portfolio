import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()

class direction(Enum): #creates constants for our direction
    LEFT = 1
    RIGHT = 2 
    UP = 3
    DOWN = 4

coor = namedtuple('coor', ('x', 'y')) #named tuple for coordinates

#colors
HEIGHT = 480
WIDTH = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (182, 245, 66)
GREEN2 = (116, 171, 15)

font = pygame.font.Font('arial.ttf', 25)
BLOCK_SIZE = 20 #size of each block where the snake can move to
SPEED = 10

class SnakeGame:
    def __init__(self, w = 640, h = 480):
        self.h = h #height  
        self.w = w #width

        self.display = pygame.display.set_mode((self.w, self.h)) #creates the display
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock() #controls the speed of the game

        self.direction = direction.RIGHT #The snake moves to the right from the start
        self.head = coor(self.w / 2, self.h / 2)
        #create a snake of 3 blocks long
        self.snake = [self.head, coor(self.head.x - BLOCK_SIZE, self.head.y), coor(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.apple = None
        self.placeApple()


    #places apple in random x and y coordinates
    def placeApple(self):
        x = random.randint(0, int(self.w / BLOCK_SIZE - 1)) * BLOCK_SIZE
        y = random.randint(0, int(self.h / BLOCK_SIZE - 1)) * BLOCK_SIZE
        self.apple = coor(x, y)
        if (self.apple in self.snake):
            self.placeApple()
    
    def move(self, direct):
        x = self.head.x
        y = self.head.y

        if (direct == direction.RIGHT):
            x += BLOCK_SIZE
        if (direct == direction.LEFT):
            x -= BLOCK_SIZE
        if (direct == direction.UP):
            y -= BLOCK_SIZE
        if (direct == direction.DOWN):
            y += BLOCK_SIZE    
        
        self.head = coor(x, y)
    
    def collision(self):
        #collision with walls 
        if (self.head.x >= self.w or self.head.x < 0 or self.head.y >= self.h or self.head.y < 0): #we substract BLOCK_SIZE to make sure that the snake doesn't go out of bounds
            return True
        #collision with itself
        if (self.head in self.snake[1:]):
            return True
        
        return False

    def playMove(self):
        #get the input
        for step in pygame.event.get():
            if (step.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (step.type == pygame.KEYDOWN):
                if (step.key == pygame.K_RIGHT and self.direction != direction.LEFT):
                    self.direction = direction.RIGHT
                elif (step.key == pygame.K_LEFT and self.direction != direction.RIGHT):
                    self.direction = direction.LEFT
                elif (step.key == pygame.K_DOWN and self.direction != direction.UP):
                    self.direction = direction.DOWN
                elif (step.key == pygame.K_UP and self.direction != direction.DOWN):
                    self.direction = direction.UP
        #move snake
        self.move(self.direction) 
        self.snake.insert(0, self.head) #insert new head

        gameOver = False
        if (self.collision()):
            gameOver = True
            return gameOver, self.score

        #check if snake reached an apple
        if (self.head == self.apple):
            self.score += 1
            self.placeApple()
        else: #if not apple reached we remove the current tail, so snakes moves without growing
            self.snake.pop()

        self.updateUI()
        self.clock.tick(SPEED)

        return gameOver, self.score

    #UI
    def updateUI(self):
        self.display.fill(BLACK) #sets background color

        #draws the snake
        for block in self.snake:
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(block.x + 4, block.y + 4, 12, 12))

        #draws the apple
        pygame.draw.rect(self.display, RED, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))

        #adds a score board
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame()

    gameLoop = True

    while (gameLoop):
        gameOver, score = game.playMove()

        if (gameOver):
            game_over_text = font.render("GAME OVER", True, WHITE)
            final_score = font.render("Your Final Score is: " + str(score), True, WHITE)
            play_again = font.render("Press \"C\" to continue or \"Q\" to quit", True, WHITE)
            display = pygame.display.set_mode((640, 480))
            display.fill(BLACK)
            display.blit(game_over_text, ((WIDTH/2) - (game_over_text.get_width() / 2), (HEIGHT/2 - (final_score.get_height() * 2))))
            display.blit(final_score, ((WIDTH/2) - (final_score.get_width() / 2), (HEIGHT/2 - (final_score.get_height() / 1.5))))
            display.blit(play_again, ((WIDTH/2) - (play_again.get_width() / 2), (HEIGHT/2 - (play_again.get_height() - final_score.get_height() * 2))))
            pygame.display.update()
            
            for step in pygame.event.get():
                if (step.type == pygame.QUIT):
                    pygame.quit()
                    quit()

                if (step.type == pygame.KEYDOWN):
                    if (step.key == pygame.K_c):
                        game = SnakeGame()
                        break
                    if (step.key == pygame.K_q):
                        gameLoop = False
                        break
        
    pygame.quit()