import pygame
from pygame.locals import *

from game import Game
from network import Network

width = 620
height = 620
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")

horizontalPadding = 150
verticalPadding = 150
innerSpaces = 10
squareWidth = 100
squareHeight = 100
roles = ["X", "O"]
someBeauty = int(squareWidth / 10)  # :3


def drawMove(win, row, column, piece):

    radius = int(squareWidth / 2)
    centerX = int(horizontalPadding + innerSpaces +(squareWidth/2) + (squareWidth + innerSpaces)*column)
    centerY = int(verticalPadding + innerSpaces + (squareHeight/2) + (squareHeight + innerSpaces)*row)

    if (piece == "O"):
        pygame.draw.circle(win, (244, 179, 147), (centerX, centerY), int(radius * 0.9), 2)
    else:
        pygame.draw.line(win, (169, 251, 195), (centerX - radius + someBeauty, centerY - radius + someBeauty), (centerX + radius - someBeauty, centerY + radius - someBeauty), 2)
        pygame.draw.line(win, (169, 251, 195), (centerX + radius - someBeauty, centerY - radius + someBeauty), (centerX - radius + someBeauty, centerY + radius - someBeauty), 2)

def drawWinningLine(win, cell1, cell2):
    print("hello")


def redrawWindow(win, game, p):
    win.fill((255, 255, 255))

    if not (game.connected()):
        drawPreview(win)
    else:
        drawGrid(win, game)
        drawPlayer(win, p)
        drawScore(win, game, p)
        drawStatus(win, game, p)
    pygame.display.update()


def drawPreview(win):
    font = pygame.font.Font(None, 80)
    text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

def drawGrid(win, game):
    for row in range(3):
        for column in range(3):
            pygame.draw.rect(win, (18, 19, 15), [(innerSpaces + squareWidth) * column + innerSpaces + horizontalPadding,
                                                (innerSpaces + squareHeight) * row + innerSpaces + verticalPadding,
                                                squareWidth, squareHeight])
            if game.grid[row][column] == 0:
                drawMove(win, row, column, "X")
            elif game.grid[row][column] == 1:
                drawMove(win, row, column, "O")

def drawStatus(win, game, p):

    if(game.isThereWinner() and game.winner == p):
        message = "Victory"
    elif (game.isThereWinner() and game.winner != p):
        message = "Defeat"
    elif not game.isThereAFreeSpace():
        message = "Draw"
    else:
        if (p == game.currentPlayer):
            message = "It's your turn"
        else:
            message = "Opponents turn"

    font = pygame.font.Font(None, 50)
    text = font.render(message, 1, (10, 10, 10))
    win.blit(text, (horizontalPadding/2, height - verticalPadding/2))
    pygame.display.update()
    if game.isThereWinner() or not game.isThereAFreeSpace():
        pygame.time.delay(2000)

def drawPlayer(win, p):
    font = pygame.font.Font(None, 32)
    text = font.render("You are: " + roles[p], 1, (255, 0, 0), True)
    win.blit(text, (horizontalPadding / 4 - text.get_width() / 4, verticalPadding / 2 - text.get_height() / 2))

def drawScore(win, game, p):
    if p == 0:
        v = str(game.wins[0])
        l = str(game.wins[1])
    else:
        v = str(game.wins[1])
        l = str(game.wins[0])

    font = pygame.font.Font(None, 32)
    text1 = font.render("Wins: " + v, 1, (255, 0, 0), True)
    win.blit(text1, (horizontalPadding / 4 - text1.get_width() / 4, verticalPadding + squareHeight/2*1 - text1.get_height() / 2))
    text2 = font.render("Loses: " + l, 1, (255, 0, 0), True)
    win.blit(text2, (horizontalPadding / 4 - text2.get_width() / 4, verticalPadding + squareHeight / 2 *3 - text2.get_height() / 2 + innerSpaces))

def getRowAndColomnFromMousePosition(pos):
    posX = pos[0]
    posY = pos[1]

    block = squareWidth + innerSpaces

    for i in range(3):
        for j in range(3):
            if((posX >= horizontalPadding + i*block and posX <= horizontalPadding + i*block + squareWidth)
                    and (posY >= verticalPadding + j*block and posY <= verticalPadding + j*block + squareHeight)):
                return(str(j) + str(i))





def main():
    n = Network()
    run = True
    clock = pygame.time.Clock()

    player = int(n.getP())
    print("You are the player: " + str(player))

    while (run):

        clock.tick(60)

        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        redrawWindow(win, game, player)

        if game.connected() and not game.isGameNotEnded():
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break



        for event in pygame.event.get():
            if event.type is QUIT:
                run = False
            elif event.type is MOUSEBUTTONDOWN:
                if game.isGameNotEnded() and game.connected() and game.currentPlayer == player:
                    try:
                        n.send(getRowAndColomnFromMousePosition(pygame.mouse.get_pos()))
                    except:
                        pass






def menu_screen():
    run = True
    clock = pygame.time.Clock()
    pygame.init()

    while run:
        clock.tick(60)
        win.fill((255, 255, 255))
        font1 = pygame.font.Font(None, 60)
        text = font1.render("Click to Play!", 1, (255, 0, 0), True)
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

menu_screen()