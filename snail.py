#!/usr/bin/env python3

import pygame
from pygame.locals import *

import time
import os
import os.path
import random
import sys

TITLE="Snail"

WIDTH = 60
HIGHT = 40


FACTOR = 12

FPS = 8

player = []
wall = []
snake = []

wall_movable = []
snake_growing = []


BLUE   = (  0,  0,255)
GREEN  = (  0,255,  0)
DGREEN = ( 50,155, 50)
RED    = (255,  0,  0)

size = 20
not_full = 0


DIRECTION = {
        "RIGHT": ( 1, 0),
        "LEFT":  (-1, 0),
        "UP":    ( 0,-1),
        "DOWN":  ( 0, 1)
        }

# likelyness that snake will chnage direction
SNAKE_RANDOM = 7
SNAKE_MIN_L = 3
SNAKE_MAX_L = 10

# color, size, no_fill
obj_size = int(FACTOR / 2)
prop = {"player":  (RED,    obj_size, False),
        "snake":   (GREEN,  obj_size, False),
        "wall":    (BLUE,   obj_size, False),
        "wall_movable":    (BLUE,   obj_size, True),
        "snake_h": (DGREEN, obj_size, False)}

def test():
    global player
    global wall
    global snake
   
    global wall_movable
    global snake_growing
    player=[10,30]
    wall=[[1,3],[3,4],[5,6],[WIDTH-5,4],[WIDTH-5,12]]
    snake=[[[14,15],[14,16],[14,17],[15,17],[16,17],[17,17],[18,17]],
        [[26,21],[26,22],[26,23],[26,24],[26,25]],
        [[55,7],[55,8],[55,9]]
        ]

    SNAKE_POPULATION = 10
    SNAKE_MIN_L = 3
    SNAKE_MAX_L = 10

    wall_movable = [True,True,False,True,True]
    snake_growing = [False, False, 10]

    build_snakes(SNAKE_POPULATION, SNAKE_MIN_L)
    build_wall()


def build_wall():
    for x in [2, WIDTH-6, WIDTH-4]:
        for y in range(0,HIGHT):
            wall.append([x,y])
            wall_movable.append(False)
        
    for y in [int(HIGHT/2 -6), int(HIGHT/2 +6)]:
        for x in range(0,WIDTH):
            wall.append([x,y])
            wall_movable.append(True)


def build_snakes(SNAKE_POPULATION, SNAKE_MIN_L):
    for s in range(0, SNAKE_POPULATION):
        snake.append([[random.randint(0,WIDTH), random.randint(1,HIGHT)]])
        leng = random.randint(SNAKE_MIN_L, SNAKE_MIN_L)
        snake_growing.append(leng) 


def right(obj):
    return [obj[0] + 1, obj[1]]

def left(obj):
    return [obj[0] - 1, obj[1]]
    
def up(obj):
    return [obj[0], obj[1] -1]

def down(obj):
    return [obj[0], obj[1] +1]

def move_to(to, obj):
    if to == "RIGHT":
        return right(obj)
    elif to == "LEFT":
        return left(obj)
    elif to == "UP":
        return up(obj)
    elif to == "DOWN":
        return down(obj)
    else:
        raise ValueError("can't move_to obj:", obj, "to:", to)


def collision(new_head):
    ## return True on collision
    x = new_head[0]
    y = new_head[1]
    if y < 0 or x < 0 or x > WIDTH or y > HIGHT:
        return True
    elif new_head in wall:
        return True
    elif any(new_head in s for s in snake):
        # snake2snake collision
        return True
    else:
        return False


def opposite(direction):
    if direction == "UP":
        return "DOWN"
    if direction == "DOWN":
        return "UP"
    if direction == "RIGHT":
        return "LEFT"
    if direction == "LEFT":
        return "RIGHT"
    raise("bad direction, no opposite", direction)


def get_current_direction(snake):
    ### retourns random direction is snake len is one
    ### else returns the direction the snake is pointed
    ### directions are UP, DOWN, RIGHT, LEFT
    if len(snake) < 2:
        direction = random.sample(list(DIRECTION),1)[0]
    else:
        head, neck = snake[0], snake[1]
        change = (head[0] - neck[0], head[1] - neck[1])
        direction = [d for d in DIRECTION.items() if d[1] == change ][0][0]
    return direction


def random_change(direction):
    ### makes snake tourn to its left or right with the possibillity of 1/SNAKE_RANDOM
    if random.randint(0,SNAKE_RANDOM) == 0:
        if direction == "UP" or direction == "DOWN":
            direction = random.choice(["RIGHT","LEFT"])
        else:
            direction = random.choice(["UP","DOWN"])
    return direction


def mk_movement_plan(head):
    all_pos = ["UP", "DOWN", "RIGHT", "LEFT"]
    possible = []
    for p in all_pos:
        new_pos = move_to(p, head)
        if not collision(new_pos):
            possible.append(p)
    random.shuffle(possible)
    return possible + ["TURN"]


def snake_step(direc, i):
    if direc == "TURN":
        snake[i] = snake[i][::-1]
    else:
        snake[i].insert(0, move_to(direc, snake[i][0]))
        #print("iiii:",i)
        if snake_growing[i] > 0:
            snake_growing[i] -=1
        else:
            snake[i].pop()


def move_snake():
    for i, this in enumerate(snake):
        #print("in move_snake. this:",this,"i:",i )
        head = this[0]

        current_direction = get_current_direction(this)
        current_direction = random_change(current_direction)
        new_head = move_to(current_direction, head)
        if collision(new_head):
            ### try othere movements
            movement_plan = mk_movement_plan(head)
            current_direction = movement_plan[0]
        snake_step(current_direction, i)


def game_over():
    print("game over, you are snake food!")
    time.sleep(1)
    sys.exit()

def game_win():
    print("congratulations. you winn. go buy your selve a cake")
    time.sleep(2)
    sys.exit()


def cut_snake(cut):
    for i, s in enumerate(snake):
        for ii, ss in enumerate(s):
            if cut == ss:
                if ii == 0:
                    #print("CUT kill--  i:",i,"ii:",ii,"s:",s,"ss:",ss)
                    del snake[i]
                    del snake_growing[i]
                else:
                    #print("CUT cut--  i:",i,"ii:",ii,"s:",s,"ss:",ss)
                    #print("cutting snake[i]:", snake[i], "to:", snake[i][:i])
                    snake[i] = snake[i][:ii]
                #print("snakes:")
                #for i, s in enumerate(snake):
                #    print(s)
                break


def push_wall(player, brick):
    ### the palyer is trying to walk from start to step
    ### pushing wawai the ston laying on step furter onto "to"
    direction = get_current_direction([brick,player])
    new_brick = move_to(direction, brick)
    if new_brick in wall:
        return player
    if any(new_brick in s for s in snake):
        cut_snake(new_brick)
    
    brick_number = wall.index(brick)
    wall[brick_number] = new_brick
    return brick


def move_player(key):
    global player
    for sn in snake:
        if player in sn:
            return game_over()
    new_player = player
    if key == K_RIGHT:
        new_player = right( player)
    elif key == K_UP:
        new_player = up( player)
    elif key == K_DOWN:
        new_player = down( player)
    elif key == K_LEFT:
        new_player = left( player)

    if new_player in wall:
        hit = wall.index(new_player)
        if wall_movable[hit]:
            new_player = push_wall(player,new_player)
        else:
            # wall not movable, everything stays
            new_player = player
    player = new_player

    if len(snake) == 0:
        ### all snakes dead. you win!
        game_win()



def draw_obj(obj, pos):
    #print("draw_obj:",pos)
    x = pos[0] * FACTOR
    y = pos[1] * FACTOR
    color, size, not_full = prop[obj]
    pygame.draw.circle(screen, color, (x, y), size, not_full)


def draw_player():
    #print("player:",player)
    draw_obj("player",player)


def draw_wall():
    for i, brick in enumerate(wall):
        if wall_movable[i]:
            draw_obj("wall_movable", brick)
        else:
            draw_obj("wall", brick)


def draw_snake():
    for one in snake:
        for body_part in one[1:]:
            draw_obj("snake", body_part)
        draw_obj("snake_h",one[0]) # head in dgreen


def display(str):
    screen.fill((159, 182, 205)) 
    draw_wall()
    draw_snake()
    draw_player()
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)
    pygame.display.update()


def handle_input():
    key_press = pygame.event.get(KEYDOWN)
    if len(key_press) == 0:
        return False

    last = key_press[-1]
    if last.key == K_ESCAPE:
        sys.exit("escape key pressed, exiting")
    return last.key


def parse_level(content):
    if not len(content) == HIGHT:
        sys.exit("error, quitting. level file has has number of lines.\n\
                expected %d lines. %d found." % (HIGHT, len(content)))
    for i, line in enumerate(content):
        if not len(line) == WIDTH:
            #print("LLLAST LINE:",line,":", len(line))
            sys.exit("error, quitting. level file has line with bad lenght.\n\
                    in line %d. expected %d char. %d found." % (i, WIDTH, len(line)))

    global player
    global wall
    global snake
    global wall_movable
    global snake_growing

    player = [[i, player.index("P")] for i, player in enumerate(content) if "P" in player ][0]

    for y, line in enumerate(content):
        for x, char in enumerate(line):
            if char == "P":
                player = [x,y]
            elif char == "W":
                wall.append([x,y])
                wall_movable.append(False)
            elif char == "V":
                wall.append([x,y])
                wall_movable.append(True)
            elif char == "H":
                snake.append([[x,y]])
                snake_growing.append(random.randint(SNAKE_MIN_L, SNAKE_MAX_L))
    
    print("player:",player)
    print("wall:",wall)
    print("snakheads:",snake)
    print("level loaded.")


def write_level_file(level_s, name):

    if os.path.exists(name):
        sys.exit("quitting. cant generate level: %s. File exists allready" % name)

    with open(name, mode="wt", encoding="utf-8") as level_file:
        level_file.write('\n'.join(level_s))

    #if not write_level(level_s, name):
    #    raise("error writing level:",name)
    print("level created and saved in file:", name)


def generate_level(name):
    SNAKE_COUNT = 20 
    WALL_COUNT = 230
    VWALL_COUNT = 230

    SNAKEHEAD = ['H'] * SNAKE_COUNT
    WALL = ['W'] *  WALL_COUNT
    VWALL = ['V'] * VWALL_COUNT
    PLAYER = ['P'] * 1
    OUTERWALL = 2 * (HIGHT + WIDTH) - 4
    print("OUT",OUTERWALL)
    VOID_COUNT = WIDTH * HIGHT - SNAKE_COUNT - WALL_COUNT - VWALL_COUNT - 1 - OUTERWALL
    VOID = [" "] * VOID_COUNT

    level = SNAKEHEAD + WALL + VWALL + VOID + PLAYER
    random.shuffle(level)

    ## make sure player is not on outer wall

    level_s = []
    print("LENNN:",len(level))

    for i in range(0,len(level), WIDTH-2):
        if i == 0:
            level_s.append("W" * WIDTH)
            print("...")
        level_s.append("W" + "".join(level[i:i+WIDTH-2]) + "W")
    level_s.append("W" * WIDTH)

#    for i in range(0,len(level), WIDTH-2):
#        if i == 0 or i == HIGHT - 1:
#            level_s.append("W" * WIDTH)
#        else:
#            level_s.append("W" + "".join(level[i:i+WIDTH]) + "W")

    if not name:
        print("in memory creat mode", level_s)
        return level_s
    else:
        print("writing generated level to file:",name)
        ## gen level and wirte to file name
        write_level_file(level_s, name)


def init_game(game_type, level=False ):
    if game_type == "test":
        test()
    elif game_type == "random":
        level = generate_level(False)
        parse_level(level)
    elif game_type == "level":
        if os.path.isfile(level):
            file_content = [line.rstrip('\n') for line in open(level)]
            parse_level(file_content)
        else:
            sys.exit("error, file not found:" + level)

def usage():
    print(sys.argv[0], " [--level <level_file> or --genlevel <level_file> or --test]")
    sys.exit()


def game_setup():
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH * FACTOR - FACTOR , HIGHT * FACTOR - FACTOR) )
    pygame.display.set_caption(TITLE)
    font = pygame.font.Font(None, 17)

    if len(sys.argv) == 1:
        print("running in random game mode mode:")
        init_game("random")

    elif len(sys.argv) == 2:
        if sys.argv[1] == "--test":
            print("running in test mode:")
            init_game("test")
        else:
            usage()

    elif len(sys.argv) == 3:
        if sys.argv[1] == "--genlevel":
            generate_level(sys.argv[2])
            sys.exit()
        elif sys.argv[1] == "--level":
            level = sys.argv[2]
            print("loading level:", level)
            init_game("level",level)
        else:
            usage()

    return font, screen



if __name__ == "__main__":

    font, screen = game_setup()
    frame = -1
    while True:
        frame += 1
        time.sleep(1 / FPS)
        move_player(handle_input())
        move_snake()
        display(str(frame))
        pygame.event.clear()
    
        
