# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "duartolass",  # Battlesnake Username
        "color": "#FF8A29",  # Battlesnake Color
        "head": "nr-rocket",  # Battlesnake Head nr-rocket
        "tail": "nr-booster",  # Battlesnake Tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # Prevent Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of head
    my_neck = game_state["you"]["body"][1]  # Coordinates of "neck"

    
    # Next move for each direction
    next_move_left = [my_head["x"] - 1, my_head["y"]]
    next_move_right = [my_head["x"] + 1, my_head["y"]]
    next_move_up = [my_head["x"], my_head["y"] + 1]
    next_move_down = [my_head["x"], my_head["y"] - 1]

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent Battlesnake from moving out of bounds
    board_width = game_state['board']['width'] - 1
    board_height = game_state['board']['height'] - 1

    if my_head["y"] == board_height:  # Head is under border, don't move up
        is_move_safe["up"] = False

    if my_head["y"] == 0:  # Head is above border, don't move down
        is_move_safe["down"] = False

    if my_head["x"] == board_width:  # Head is left of border, don't move right
        is_move_safe["right"] = False
    
    if my_head["x"] == 0:  # Head is right of border, don't move left
        is_move_safe["left"] = False

    # Prevent Battlesnake from colliding with itself and other Battlesnakes
    snakes = game_state['board']['snakes']

    for snake in snakes:
        for Bodypart in snake['body']:
            tempBp = [Bodypart["x"], Bodypart["y"]]
            if next_move_left == tempBp: # Body is left of head, don't move left
                is_move_safe["left"] = False

            if next_move_right == tempBp: # Body is right of head, don't move right
                is_move_safe["right"] = False

            if next_move_up == tempBp: # Body is above head, don't move up
                is_move_safe["up"] = False
            
            if next_move_down == tempBp: # Body is under head, don't move down
                is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    ClosestFood = []
    DistanceToFood = 100 # Big number so it's replaced by a smaller number later
    for foodObject in food:
        TempDistanceToFood = abs(foodObject["x"] - my_head["x"]) + abs(foodObject["y"] - my_head("y")) # calculates which fruit object is closest to head
        if TempDistanceToFood < DistanceToFood: # If the current distance to food object is smaller than the previously closest food object, then replace it with the new one saved in temp
            DistanceToFood = TempDistanceToFood # Sets the newly calculated distance as the smallest Distance to food
            ClosestFood = foodObject # sets the current array foodObject as the Closest Food.
            
    if my_head["x"] > ClosestFood["x"]: # Check if the head is to the right of the closest food
        if is_move_safe["left"]: # checks if the the next left move is safe
            next_move = ["left"] # moves to the left
    if my_head["x"] < ClosestFood["x"]: # Check if the head is to the left of the closest food
        if is_move_safe["right"]: # checks if the the next right move is safe
            next_move = ["right"] # moves to the right
    if my_head["y"] > ClosestFood["y"]: # Check if the head is above the closest food
        if is_move_safe["down"]: # checks if the the next down move is safe
            next_move = ["down"] # moves down
    if my_head["y"] > ClosestFood["y"]: # Check if the head is under the closest food
        if is_move_safe["up"]: # checks if the the next up move is safe
            next_move = ["up"] # moves up

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
