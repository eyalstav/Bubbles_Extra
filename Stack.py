import math

import Bubble
import consts
import random
import Screen

stack = []


def create(stack_size):
    global stack
    stack = []
    for i in range(stack_size):
        add_bubble(i)
    return stack


def update_location(game_state):
    if not game_state["mouse_angle"]: return
    topX = game_state["rotated_arrow"].get_rect(
        center=(consts.ARROW_MIDBOTTOM_X, consts.ARROW_MIDBOTTOM_Y)).x
    topY = game_state["rotated_arrow"].get_rect(
        center=(consts.ARROW_MIDBOTTOM_X, consts.ARROW_MIDBOTTOM_Y)).y
    rotation = (game_state["mouse_angle"]-90)/46
    radios = 100
    mid = (consts.ARROW_MIDBOTTOM_X - consts.BUBBLE_RADIUS,consts.ARROW_MIDBOTTOM_Y)


    X = mid[0] - (math.sin(rotation)*radios)+30
    Y = mid[1] - math.cos(rotation)*radios - 30
    c = 0
    for b in stack:
        b["center_x"] = X + c*50
        b["center_y"] = Y
        c+=1


def add_bubble(col):
    bubble_x = Bubble.calc_center_x(col, row=0,
                                    row_start=consts.STACK_LOCATION[0])
    stack.append(Bubble.create(bubble_x,
                               consts.STACK_LOCATION[1],
                               random.choice(consts.bubble_colors)))


def remove_first():
    bullet_bubble = stack.pop(0)

    for i in range(len(stack)):
        stack[i]["center_x"] = Bubble.calc_center_x(i, row=0,
                                                    row_start=
                                                    consts.STACK_LOCATION[0])
    return bullet_bubble


def get_length():
    return len(stack)


def draw():
    for bubble in stack:
        Screen.draw_bubble(bubble)

# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------


