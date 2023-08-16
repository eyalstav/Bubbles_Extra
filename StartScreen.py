





import sys
import pygame
import consts
pygame.init()
font = pygame.font.SysFont('Arial', 40)

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


RED = pygame.image.load("balls/red.png")
GREEN = pygame.image.load("balls/green.png")
BLUE = pygame.image.load("balls/blue.png")
ORANGE = pygame.image.load("balls/orange.png")
VIOLET = pygame.image.load("balls/violet.png")

screen = pygame.display.set_mode(
        (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))
run = True
def easy():
    global run
    consts.BUBBLE_START_COLORS = [RED,GREEN,BLUE]
    run = False

def med():
    global run
    consts.BUBBLE_START_COLORS = [RED, GREEN, BLUE, ORANGE]
    run = False

def hard():
    global run
    consts.BUBBLE_START_COLORS = [RED, GREEN, BLUE, ORANGE, VIOLET]
    run = False

btns = []
btns.append(Button(30, 455, 200, 50, 'EASY', easy))
btns.append(Button(260, 455, 200, 50, 'MEDIUM', med))
btns.append(Button(490, 455, 200, 50, 'HARD', hard))
def Start_Screen(screen):
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bg = pygame.image.load("balls/background.png")
        screen.blit(bg,(0,0))

        for btn in btns:
            btn.process()

        pygame.display.flip()
