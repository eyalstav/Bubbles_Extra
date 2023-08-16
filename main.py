import pygame
import BubblesGrid
import Bubble
import Stack
import Screen
import consts

state = {
    "original_arrow": Screen.create_arrow(consts.ARROW_IMG),
    "rotated_arrow": None,
    "is_bubble_fired": False,
    "bubbles_popping": [],
    "turns_left_to_add_row": consts.NUM_OF_TURNS_TO_ADD_ROW,
    "is_window_open": True,
    "state": consts.RUNNING_STATE,
    "bullet_bubble": None,
    "bubble_direction": None,
    "mouse_angle": None
}

state["rotated_arrow"] = state["original_arrow"]

run = True
def main():
    pygame.init()

    Screen.Start_Screen()


    while state["is_window_open"]:
        run = True
        BubblesGrid.create()
        Stack.create(consts.STACK_SIZE)
        while run:
            if not state["is_window_open"]:
                break
            handle_user_events()
            Stack.update_location(state)

            if state["is_bubble_fired"]:
                Screen.draw_shoot_animation()

                move_bubble()

                if Bubble.should_stop(BubblesGrid.bubbles_grid,
                                      state["bullet_bubble"]):
                    Screen.frame =0
                    Screen.counter=0
                    state["is_bubble_fired"] = False

                    new_bubble_location = BubblesGrid.find_bubble_location_in_grid(
                            state["bullet_bubble"])
                    BubblesGrid.put_bubble_in_grid(state["bullet_bubble"],
                                                   new_bubble_location)

                    same_color_cluster = BubblesGrid.get_same_color_cluster(
                            new_bubble_location,
                            state["bullet_bubble"]["color"],
                            [])

                    if BubblesGrid.should_bubbles_pop(same_color_cluster):
                        state["bubbles_popping"] = \
                            BubblesGrid.pop_bubbles(same_color_cluster)

                    # The counter counts only if bubbles weren't popped
                    else:
                        state["turns_left_to_add_row"] -= 1
                        consts.score += 1

                        if state["turns_left_to_add_row"] == 0:
                            BubblesGrid.add_new_line()

                            # Reseting the counter
                            state["turns_left_to_add_row"] = \
                                consts.NUM_OF_TURNS_TO_ADD_ROW

                    remove_isolated_bubbles()
                    BubblesGrid.set_one_empty_line()
                    remove_extinct_colors(consts.bubble_colors)
                    Stack.add_bubble(Stack.get_length())

                    if is_lose():
                        state["state"] = consts.LOSE_STATE
                        BubblesGrid.bubbles_grid = []
                        Stack.stack = []
                        consts.bubble_colors = Screen.chosen_list.copy()
                        run = False
                    elif is_win():
                        state["state"] = consts.WIN_STATE
                        BubblesGrid.bubbles_grid = []
                        Stack.stack = []
                        if consts.score < consts.highest_score or consts.highest_score == 0:
                            consts.highest_score = consts.score
                        consts.bubble_colors = Screen.chosen_list.copy()
                        run = False

            Screen.draw_game(state)

font = pygame.font.SysFont('Arial', 40)
def handle_user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["is_window_open"] = False
            global run
            run = False


        elif state["state"] != consts.RUNNING_STATE:
            continue

        if event.type == pygame.MOUSEMOTION:
            rotate_arrow()

        elif event.type == pygame.MOUSEBUTTONDOWN and \
                not state["is_bubble_fired"] and \
                not state["bubbles_popping"]:
            fire_bubble()


def rotate_arrow():
    state["mouse_angle"] = Screen.calc_mouse_angle(pygame.mouse.get_pos())
    state["rotated_arrow"] = pygame.transform.rotate(state["original_arrow"],
                                                     state["mouse_angle"] - 90)


def fire_bubble():
    state["is_bubble_fired"] = True
    state["bubble_direction"] = \
        Bubble.calc_direction(state["mouse_angle"])
    state["bullet_bubble"] = Stack.remove_first()


def move_bubble():
    Bubble.move_in_direction(state["bullet_bubble"], state["bubble_direction"])

    if Bubble.is_colliding_with_wall(state["bullet_bubble"]):
        state["bubble_direction"] = (state["bubble_direction"][0] * (-1),
                                     state["bubble_direction"][1])


def remove_isolated_bubbles():
    isolated_bubbles_locations = BubblesGrid.find_isolated_bubbles()

    if len(isolated_bubbles_locations) > 0:
        state["bubbles_popping"] += \
            BubblesGrid.pop_bubbles(isolated_bubbles_locations)


# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------

def remove_extinct_colors(bubble_colors:list):
    #loop through all the bubbles and stack
    #add them to a list and see if there is something missing
    colors = []
    for row in BubblesGrid.bubbles_grid:
        for b in row:
            if b["color"] != 'EMPTY' and b["color"] not in colors:
                colors.append(b["color"])
    for b in Stack.stack:
        colors.append(b["color"])

    #make diffrent list so we dont get err
    remove = []
    for color in bubble_colors:
        if color not in colors:
            remove.append(color)
    #remove them
    for c in remove:
        bubble_colors.remove(c)

def is_lose():
    max = consts.NUM_OF_LINES_LOSE
    l = 0
    for row in BubblesGrid.bubbles_grid:
        for b in row:
            if b["color"] != "EMPTY":
                if l < BubblesGrid.bubbles_grid.index(row):
                    l = BubblesGrid.bubbles_grid.index(row)
    if l >= max:
        return True
    return False


def is_win():
    win = True
    for i in BubblesGrid.bubbles_grid:
        for j in i:
            if j["color"] != "EMPTY": win = False
    return win

# -----------------------------------------------------------------------------
# ------------------------------your code end----------------------------------
# -----------------------------------------------------------------------------

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
