
import pygame, random, sys
from card import Card
from pygame.locals import *


#---------- Main Constants ----------#
FPS          = 60
WINDOW_X     = 640
WINDOW_Y     = 480
BOARD_X      = 8
BOARD_Y      = 4
CELLSIZE     = 60
CELL_MARGIN  = 10
X_MARGIN = int((WINDOW_X - (BOARD_X * (CELLSIZE + CELL_MARGIN))) / 2)
Y_MARGIN = int((WINDOW_Y - (BOARD_Y * (CELLSIZE + CELL_MARGIN))) / 2)

assert (BOARD_X * BOARD_Y) % 2 == 0, "Board must have even number of boxes in order to complete game."

DONUT   = 'donut'
SQUARE  = 'square'
DIAMOND = 'diamond'
CIRCLE  = 'oval'


#---------- Colors ----------#
FONT        = ( 89, 171, 227)  # Picton Blue
BACKGROUND  = ( 44,  62,  80)  
BOARD       = ( 82, 179, 217)
BOARDSHADOW = ( 41, 128, 185)
HIDDEN      = ( 75, 119, 190)
CARDSHADOW  = ( 44,  62,  80)  
HIGHLIGHT   = (236, 240, 241)  # Cloud White

COLOR_1    = ( 39, 174,  96)  # Nephritis Green
TINT_1     = ( 46, 204, 113)
COLOR_2    = (241, 196,  15)  # Sunflower Yellow
TINT_2     = (243, 156,  18)
COLOR_3    = ( 52, 152, 219)  # Peter River Blue
TINT_3     = ( 41, 128, 185)
COLOR_4    = (231,  76,  60)  # Alizarin Red
TINT_4     = (192,  57,  43)


#---------- List Constants ----------#
SHAPE_LIST = (DONUT, SQUARE, DIAMOND, CIRCLE)
COLOR_LIST = (COLOR_1, COLOR_2, COLOR_3, COLOR_4)

assert len(SHAPE_LIST) * len(COLOR_LIST) * 2 == (BOARD_X * BOARD_Y), "Board options must match board size."


#---------- Pygame init ----------#
pygame.init()
DISPLAY = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('Memory')

#---------- Fonts ----------#
fontObj = pygame.font.Font('OpenSans-Regular.ttf', 32)
textSurfaceObj = fontObj.render('Memory', True, FONT, BACKGROUND)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = ((WINDOW_X / 2), 20)



class Game:
    #---------- Board Creation/Updating ----------#
    def createIconList(self):
        icon_list = []
        for color in COLOR_LIST:
            for shape in SHAPE_LIST:
                icon_list.append((shape, color))

        icon_list *= 2
        random.shuffle(icon_list)
        return icon_list


    def createBoard(self, icons):
        board = []
        for x in range(BOARD_X):
            column = []
            for y in range(BOARD_Y):
                card = Card(x, y, icons)
                column.append(card)
                del icons[0]
            board.append(column)
        pygame.draw.rect(DISPLAY, BOARDSHADOW, [X_MARGIN / 2, Y_MARGIN / 2, WINDOW_X - X_MARGIN, WINDOW_Y - Y_MARGIN + 6])
        pygame.draw.rect(DISPLAY, BOARD, [X_MARGIN / 2, Y_MARGIN / 2, WINDOW_X - X_MARGIN, WINDOW_Y - Y_MARGIN])
        return board


    def updateBoard(self, board):
        for card in Card.instances:
            if card.mode == 0:
                self.drawCard(card, HIDDEN)
            elif card.mode == 1:
                self.drawCard(card, HIGHLIGHT)
            elif card.mode == 2:
                self.drawCard(card, card.color)
                self.drawCardIcon(card)



    #---------- Card Creation/Updating ----------#
    def drawCard(self, card, color):
        pygame.draw.rect(DISPLAY, CARDSHADOW, [(CELL_MARGIN + CELLSIZE) * card.x + X_MARGIN + (CELL_MARGIN / 2), (CELL_MARGIN + CELLSIZE) * card.y + Y_MARGIN + (CELL_MARGIN / 2), CELLSIZE, CELLSIZE])
        card.rect = pygame.draw.rect(DISPLAY, color, [(CELL_MARGIN + CELLSIZE) * card.x + X_MARGIN + (CELL_MARGIN / 2), (CELL_MARGIN + CELLSIZE) * card.y + Y_MARGIN + (CELL_MARGIN / 2) - 1, CELLSIZE, CELLSIZE - 3])


    def leftTopCoords(self, card):
        left = int((CELL_MARGIN + CELLSIZE) * card.x + X_MARGIN + (CELL_MARGIN / 2))
        top = int((CELL_MARGIN + CELLSIZE) * card.y + Y_MARGIN + (CELL_MARGIN / 2))
        return (left, top)


    def drawCardIcon(self, card):
        if card.color == COLOR_1:
            tint = TINT_1
        elif card.color == COLOR_2:
            tint = TINT_2
        elif card.color == COLOR_3:
            tint = TINT_3
        elif card.color == COLOR_4:
            tint = TINT_4

        half = int(CELLSIZE * 0.5)
        quarter = int(CELLSIZE * 0.25)
        left, top = self.leftTopCoords(card)
        if card.icon == DONUT:
            pygame.draw.circle(DISPLAY, tint, (left + half, top + half - 2), half - 10)
            pygame.draw.circle(DISPLAY, card.color, (left + half, top + half - 2), quarter - 2)
        elif card.icon == SQUARE:
            pygame.draw.rect(DISPLAY, tint, (left + quarter, top + quarter - 2, CELLSIZE - half, CELLSIZE - half))
        elif card.icon == DIAMOND:
            pygame.draw.polygon(DISPLAY, tint, ((left + half, top + 6), (left + CELLSIZE - 10, top + half - 4), (left + half, top + CELLSIZE - 14), (left + 10, top + half - 4)))
        elif card.icon == CIRCLE:
            pygame.draw.circle(DISPLAY, tint, (left + half, top + half - 2), half - 10)

    def hideCard(self, card, clock):
        for coverage in range(0, 57, 2):
            pygame.draw.rect(DISPLAY, HIDDEN, [(CELL_MARGIN + CELLSIZE) * card.x + X_MARGIN + (CELL_MARGIN / 2), (CELL_MARGIN + CELLSIZE) * card.y + Y_MARGIN + (CELL_MARGIN / 2), CELLSIZE, coverage])
            pygame.display.flip()
            clock.tick(FPS)
        card.mode = 0




    #---------- Guessing ----------#
    def checkGuess(self):
        first = Card.guesses[0]
        second = Card.guesses[1]
        if first.color == second.color and first.icon == second.icon:
            Card.correct.append(first)
            Card.correct.append(second)
            del Card.guesses[:]
        else:
            for card in Card.guesses:
                card.mode = 0
            del Card.guesses[:]


def main():
    clock = pygame.time.Clock()

    creating_board = True
    while creating_board:
        DISPLAY.fill(BACKGROUND)
        game = Game()
        icons = game.createIconList()
        board = game.createBoard(icons)
        game.updateBoard(board)
        creating_board = False

    for card in Card.instances:
        game.hideCard(card, clock)
        pygame.display.flip()
        clock.tick(FPS)

    guesses = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                for card in Card.instances:
                    if card.mode != 2:
                        if card.rect.collidepoint(mouse_x, mouse_y):
                            card.mode = 1
                        else:
                            card.mode = 0

            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if guesses < 2:
                    for card in Card.instances:
                        if card.rect.collidepoint(mouse_x, mouse_y) and card not in Card.correct:
                            guesses += 1
                            card.revealCard()
                            pygame.display.flip()
                            clock.tick(FPS)

        if guesses == 2:
            game.checkGuess()
            guesses = 0

        game.updateBoard(board)
        DISPLAY.blit(textSurfaceObj, textRectObj)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()