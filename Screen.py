import Stack
import consts
import pygame
import math
import BubblesGrid

screen = pygame.display.set_mode(
        (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))


def draw_bubble(bubble):
    screen.blit(bubble["color"],(bubble["center_x"]-bubble["radius"],bubble["center_y"]-bubble["radius"]))


def draw_bubbles_popping(bubbles_popping):
    for bubble in bubbles_popping:
        draw_bubble(bubble)


def calc_mouse_angle(mouse_pos):
    x_diff = mouse_pos[0] - consts.ARROW_MIDBOTTOM_X
    y_diff = consts.ARROW_MIDBOTTOM_Y - mouse_pos[1]
    angle = math.degrees(math.atan2(y_diff, x_diff))
    return angle


def create_arrow(arrow_img):
    arrow = pygame.image.load(arrow_img)
    sized_arrow = pygame.transform.scale(arrow, (
        consts.ARROW_WIDTH, consts.ARROW_HEIGHT))

    # Create a box to put the arrow in, so that the rotation will be around
    # it's bottom (the box's center)
    arrow_box = pygame.Surface(
            (consts.ARROW_WIDTH, consts.ARROW_HEIGHT * 2), )
    arrow_box.fill(consts.BACKGROUND_COLOR)
    arrow_box.blit(sized_arrow, (0, 0))

    return arrow_box


def draw_arrow(arrow):
    rotated_arrow_rect = arrow.get_rect(
            center=(consts.ARROW_MIDBOTTOM_X, consts.ARROW_MIDBOTTOM_Y))
    screen.blit(arrow, rotated_arrow_rect)

frames = [pygame.image.load("lion-0001.png"),pygame.image.load("lion-0002.png"),pygame.image.load("lion-0003.png")]
frame = 0
counter = 0
def draw_shoot_animation():
    global  frame
    if counter % 10 == 0:
        frame+=1
    if frame > 2: frame = 0

    arrow = frames[frame]
    sized_arrow = pygame.transform.scale(arrow, (
        consts.ARROW_WIDTH, consts.ARROW_HEIGHT))

    # Create a box to put the arrow in, so that the rotation will be around
    # it's bottom (the box's center)
    arrow_box = pygame.Surface(
            (consts.ARROW_WIDTH, consts.ARROW_HEIGHT * 2), )

    draw_arrow(arrow_box)

def draw_border():
    line_y = consts.NUM_OF_LINES_LOSE * consts.BUBBLE_RADIUS * 2 - (
            consts.NUM_OF_LINES_LOSE - 1) * consts.ROWS_OVERLAP
    pygame.draw.line(screen, consts.BORDER_COLOR, start_pos=(0, line_y),
                     end_pos=(consts.WINDOW_WIDTH, line_y))


##########MINE#############
def draw_score():
    message = "SCORE: " + str(consts.score)
    draw_message(message, consts.TURNS_FONT_SIZE, consts.TURNS_COLOR, (10,consts.TURNS_LOCATION[1]-50))

    message = "HIGHEST SCORE: " + str(consts.highest_score)
    draw_message(message, consts.TURNS_FONT_SIZE, consts.TURNS_COLOR, (10, consts.TURNS_LOCATION[1] - 80))

def draw_turns(num_of_turns):
    message = consts.TURNS_TEXT + str(num_of_turns)
    draw_message(message, consts.TURNS_FONT_SIZE, consts.TURNS_COLOR,
                 consts.TURNS_LOCATION)


def draw_lose_message():
    draw_message(consts.LOSE_MESSAGE, consts.LOSE_FONT_SIZE,
                 consts.LOSE_COLOR, consts.LOSE_LOCATION)


def draw_win_message():
    draw_message(consts.WIN_MESSAGE, consts.WIN_FONT_SIZE,
                 consts.WIN_COLOR, consts.WIN_LOCATION)


def draw_message(message, font_size, color, location):
    font = pygame.font.SysFont(consts.FONT_NAME, font_size)
    text_img = font.render(message, True, color)
    screen.blit(text_img, location)


def draw_game(game_state):

    screen.fill(consts.BACKGROUND_COLOR)
    draw_arrow(game_state["rotated_arrow"])

    if game_state["is_bubble_fired"]:
        draw_bubble(game_state["bullet_bubble"])

    BubblesGrid.draw()
    draw_border()
    draw_turns(game_state["turns_left_to_add_row"])
    ##MINE##
    draw_score()
    Stack.draw()

    if len(game_state["bubbles_popping"]):
        BubblesGrid.animate_bubbles_pop(game_state["bubbles_popping"])
        draw_bubbles_popping(game_state["bubbles_popping"])

    elif game_state["state"] == consts.LOSE_STATE:
        draw_lose_message()
        pygame.display.flip()
        pygame.time.wait(1000*3)#3 seconds
        game_state["state"] = consts.RUNNING_STATE


    elif game_state["state"] == consts.WIN_STATE:
        draw_win_message()
        pygame.display.flip()
        pygame.time.wait(1000 * 3)  # 3 seconds
        game_state["state"] = consts.RUNNING_STATE

    pygame.display.flip()


################SRYYYYYYYYYYY####################
#################################################

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

run = True
chosen_list = []
easy_list = [pygame.image.load("balls/r.png"),pygame.image.load("balls/g.png"),pygame.image.load("balls/b.png")]
def easy():
    print("easy")
    global run
    global chosen_list
    consts.bubble_colors = easy_list.copy()
    chosen_list = easy_list
    run = False
med_list = [pygame.image.load("balls/violet2.png"), pygame.image.load("balls/green2.png"), pygame.image.load("balls/blue2.png"), pygame.image.load("balls/orange2.png")]
def med():
    global run
    consts.bubble_colors = med_list.copy()
    run = False
    global chosen_list
    chosen_list = med_list
hard_list = [pygame.image.load("balls/1.png"), pygame.image.load("balls/2.png"), pygame.image.load("balls/3.png"), pygame.image.load("balls/4.png"), pygame.image.load("balls/5.png")]
def hard():
    global run
    consts.bubble_colors = hard_list.copy()
    global chosen_list
    chosen_list = hard_list
    run = False

btns = []
btns.append(Button(30, 455, 200, 50, 'EASY', easy))
btns.append(Button(260, 455, 200, 50, 'MEDIUM', med))
btns.append(Button(490, 455, 200, 50, 'HARD', hard))
def Start_Screen()->bool:
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False

        bg = pygame.image.load("balls/background4.png")
        screen.blit(bg,(0,0))

        for btn in btns:
            btn.process()

        pygame.display.flip()
    return True
