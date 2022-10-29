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
        "head": "all-seeing",  # Battlesnake Head
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
    is_move_risky = {"up": True, "down": True, "left": True, "right": True}

    # Prevent Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of head
    my_neck = game_state["you"]["body"][1]  # Coordinates of "neck"
    my_length = game_state["you"]["length"]
    
    my_id = game_state["you"]["id"] # Id of snake
    
    # Next move for each direction
    next_move_left = [my_head["x"] - 1, my_head["y"]]
    next_move_right = [my_head["x"] + 1, my_head["y"]]
    next_move_up = [my_head["x"], my_head["y"] + 1]
    next_move_down = [my_head["x"], my_head["y"] - 1]

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        is_move_risky["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        is_move_risky["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        is_move_risky["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        is_move_risky["up"] = False

    # Prevent Battlesnake from moving out of bounds
    board_width = game_state['board']['width'] - 1
    board_height = game_state['board']['height'] - 1

    if my_head["y"] == board_height:  # Head is under border, don't move up
        is_move_safe["up"] = False
        is_move_risky["up"] = False

    if my_head["y"] == 0:  # Head is above border, don't move down
        is_move_safe["down"] = False
        is_move_risky["down"] = False

    if my_head["x"] == board_width:  # Head is left of border, don't move right
        is_move_safe["right"] = False
        is_move_risky["right"] = False
    
    if my_head["x"] == 0:  # Head is right of border, don't move left
        is_move_safe["left"] = False
        is_move_risky["left"] = False

    # Prevent Battlesnake from colliding with itself and other Battlesnakes
    snakes = game_state['board']['snakes']

    for snake in snakes:
        for Bodypart in snake['body']:
            tempBp = [Bodypart["x"], Bodypart["y"]]
            if next_move_left == tempBp: # Body is left of head, don't move left
                is_move_safe["left"] = False
                is_move_risky["left"] = False

            if next_move_right == tempBp: # Body is right of head, don't move right
                is_move_safe["right"] = False
                is_move_risky["right"] = False

            if next_move_up == tempBp: # Body is above head, don't move up
                is_move_safe["up"] = False
                is_move_risky["up"] = False
            
            if next_move_down == tempBp: # Body is under head, don't move down
                is_move_safe["down"] = False
                is_move_risky["down"] = False

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)

    # Check if the next move is risky from other opponents
    op_next_move = []
    snake_ids = []
    for ekans in snakes:
        if ekans['id'] != my_id:
            snake_ids.append(ekans)
    for opponent in snake_ids:    
        Opponenthead = opponent['head']
        op_next_move_left = [Opponenthead["x"] - 1, Opponenthead["y"]]
        op_next_move_right = [Opponenthead["x"] + 1, Opponenthead["y"]]
        op_next_move_up = [Opponenthead["x"], Opponenthead["y"] + 1]
        op_next_move_down = [Opponenthead["x"], Opponenthead["y"] - 1]
        op_next_move.append(op_next_move_left)
        op_next_move.append(op_next_move_right)
        op_next_move.append(op_next_move_up)
        op_next_move.append(op_next_move_down)

        for s in snake_ids:
            OpponentLength = s["length"]
            if my_length <= OpponentLength:
                for OpponentMovement in op_next_move:
                    if OpponentMovement == next_move_left:
                        is_move_safe["left"] = False
                        is_move_risky["left"] = True
                    if OpponentMovement == next_move_right:
                        is_move_safe["right"] = False
                        is_move_risky["right"] = True
                    if OpponentMovement == next_move_up:
                        is_move_safe["up"] = False
                        is_move_risky["up"] = True
                    if OpponentMovement == next_move_down:
                        is_move_safe["down"] = False
                        is_move_risky["down"] = True

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    
    # Are there any risky moves left?
    risky_moves = []
    for move, isRisky in is_move_risky.items():
        if isRisky:
            risky_moves.append(move)

    food = game_state['board']['food']
    ClosestFood = []
    ClosestDistanceToFood = 99
    for foodObject in food:
        TempDistanceToFood = abs(foodObject["x"] - my_head["x"]) + abs(foodObject["y"] - my_head["y"])
        if TempDistanceToFood < ClosestDistanceToFood:
            ClosestDistanceToFood = TempDistanceToFood
            ClosestFood = foodObject
   
    lowestop = []
    distancetoop = 99
    for f_op in snake_ids:
        fight_op = f_op['head']
        tempdistancetoop = abs(fight_op["x"] - my_head["x"]) + abs(fight_op["y"] - my_head["y"])
        if tempdistancetoop < distancetoop:
            distancetoop = tempdistancetoop
            lowestop = fight_op

        for s_op in snake_ids:
            op_length = s_op["length"]
            if my_length <= op_length:
                if len(safe_moves) != 0:
                    if my_head["x"] > ClosestFood["x"] and is_move_safe["left"]:
                        next_move = "left"
                    elif my_head["x"] < ClosestFood["x"] and is_move_safe["right"]:
                        next_move = "right"
                    elif my_head["y"] < ClosestFood["y"] and is_move_safe["up"]:
                        next_move = "up"
                    elif my_head["y"] > ClosestFood["y"] and is_move_safe["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(safe_moves)
                elif len(risky_moves) != 0:
                    if my_head["x"] > ClosestFood["x"] and is_move_risky["left"]:
                        next_move = "left"
                    elif my_head["x"] < ClosestFood["x"] and is_move_risky["right"]:
                        next_move = "right"
                    elif my_head["y"] < ClosestFood["y"] and is_move_risky["up"]:
                        next_move = "up"
                    elif my_head["y"] > ClosestFood["y"] and is_move_risky["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(risky_moves)
                else:
                    print(f"MOVE {game_state['turn']}: No safe moves detected!\nMoving randomly!")
                    next_move = random.choice(risky_moves)
            else:
                if len(safe_moves) != 0:
                    if my_head["x"] > lowestop["x"] and is_move_safe["left"]:
                        next_move = "left"
                    elif my_head["x"] < lowestop["x"] and is_move_safe["right"]:
                        next_move = "right"
                    elif my_head["y"] < lowestop["y"] and is_move_safe["up"]:
                        next_move = "up"
                    elif my_head["y"] > lowestop["y"] and is_move_safe["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(safe_moves)
                elif len(risky_moves) != 0:
                    if my_head["x"] > lowestop["x"] and is_move_risky["left"]:
                        next_move = "left"
                    elif my_head["x"] < lowestop["x"] and is_move_risky["right"]:
                        next_move = "right"
                    elif my_head["y"] < lowestop["y"] and is_move_risky["up"]:
                        next_move = "up"
                    elif my_head["y"] > lowestop["y"] and is_move_risky["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(risky_moves)
                else:
                    print(f"MOVE {game_state['turn']}: No safe moves detected!\nMoving randomly!")
                    next_move = random.choice(risky_moves)

# Movement
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
