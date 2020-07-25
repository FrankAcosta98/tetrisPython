import pygame as pg
import random as rand

screen_h = 700
screen_w = 800
# 10x20 grid tetris
grid_h = 600
grid_w = 300
block_s = 30

topLeft_x = (screen_w - grid_w) // 2
topLeft_y = screen_h - grid_h


"""pg.init()
screen = pg.display.set_mode((screen_h, screen_w))
"""
# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....'],
      ]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
          (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.rot = 0


def create_grid(locked_positions={}):
    grid = [[(20, 20, 20) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    position = []
    format = shape.shape[shape.rot % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                position.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(position):
        position[i] = (pos[0]-2, pos[1]-4)

    return position


def valid_space(shape, grid):
    acceptPos = [[(j, i)for j in range(10)if grid[i][j] == (20, 20, 20)]
                 for i in range(20)]
    acceptPos = [j for sublist in acceptPos for j in sublist]
    form = convert_shape_format(shape)

    for pos in form:
        if pos not in acceptPos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, colors
    return Piece(5, -1, rand.choice(shapes))



def draw_grid(surface, grid):
    for i in range(len(grid)):
        pg.draw.line(surface, (80, 80, 80), (topLeft_x, topLeft_y +
                                                i*block_s), (topLeft_x+grid_w, topLeft_y+i*block_s))
        for j in range(len(grid[i])+1):
            pg.draw.line(surface, (100, 100, 100), (topLeft_x+j*block_s,
                                                    topLeft_y), (topLeft_x+j*block_s, topLeft_y+grid_h))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (20, 20, 20) not in row:
            inc += 1
            idx = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < idx:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    pg.font.init()
    font = pg.font.SysFont('He´s Dead Jim', 30)
    label = font.render('Next', 1, (212, 212, 212))
    format = shape.shape[shape.rot % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                pg.draw.rect(surface, shape.color, (topLeft_x+350+j *
                                                    block_s, topLeft_y+30+i*block_s, block_s, block_s), 0)
    surface.blit(label, (topLeft_x+390, topLeft_y-20))


def draw_hold(shape, surface, hold):
    pg.font.init()
    font = pg.font.SysFont('He´s Dead Jim', 30)
    label = font.render('Hold', 1, (212, 212, 212))
    format = shape.shape[shape.rot % len(shape.shape)]
    if hold:
        for i, line in enumerate(format):
            row = list(line)
            for j, col in enumerate(row):
                if col == '0':
                    pg.draw.rect(surface, shape.color, (topLeft_x-180+j *
                                                        block_s, topLeft_y+30+i*block_s, block_s, block_s), 0)
    surface.blit(label, (topLeft_x-130, topLeft_y-20))


def draw_window(surface, grid, score=0):
    surface.fill((15, 15, 15))
    pg.font.init()
    font = pg.font.SysFont('He´s Dead Jim', 60)
    label = font.render('Tetris Chido', 1, (0, 95, 120))
    surface.blit(label, (int(topLeft_x+grid_w/2-(label.get_width()/2)), 30))
    font = pg.font.SysFont('He´s Dead Jim', 20)
    label = font.render('Score: '+ str(score), 1, (147, 204, 19))
    surface.blit(label, (int(topLeft_x+grid_w/2-(label.get_width()/2)), 10))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pg.draw.rect(
                surface, grid[i][j], (topLeft_x + j * 30, topLeft_y + i * 30, 30, 30), 0)
    draw_grid(surface, grid)
    pg.draw.rect(surface, (250, 250, 250), (topLeft_x,
                                            topLeft_y, grid_w, grid_h), 4)


def draw_loose(surface, grid, score):
    pg.font.init()
    font = pg.font.SysFont('He´s Dead Jim', 80)
    label = font.render('Fallaste ', 1, (255, 20, 20))
    surface.blit(label, (int(topLeft_x+grid_w/2-(label.get_width()/2)), 350))
    label = font.render('Score: ' + str(score), 1, (255, 20, 20))
    surface.blit(label, (int(topLeft_x+grid_w/2-(label.get_width()/2)), 450))


def draw_start(surface):
    pg.font.init()
    font = pg.font.SysFont('He´s Dead Jim', 90)
    label = font.render('Dale espacio ', 1, (0, 95, 120))
    surface.blit(label, (int(topLeft_x+grid_w/2-(label.get_width()/2)), 350))


def main(window):
    locked_position = {}
    grid = create_grid(locked_position)
    change_piece = False
    hold = False
    changed = False
    hold_piece = get_shape()
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pg.time.Clock()
    fallTime = 0
    fallSpd = 0.27
    levelTime = 0
    score = 0

    while run:
        grid = create_grid(locked_position)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()
        if levelTime / 1000 > 503:
            levelTime = 0
            if fallSpd > 0.12:
                fallSpd -= 0.0005

        if fallTime / 1000 > fallSpd:
            fallTime = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
                changed = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pg.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pg.K_UP:
                    current_piece.rot += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rot -= 1
                if event.key == pg.K_c:
                    tmp = current_piece
                    if (hold):
                        current_piece = hold_piece
                        hold_piece = tmp
                        current_piece.x = 5
                        current_piece.y = -1
                    else:
                        hold_piece = current_piece
                        current_piece = next_piece
                        hold = True
                    changed = True
                if event.key == pg.K_SPACE:
                    for i in range(len(grid)):
                        if grid[i][current_piece.x] != (20, 20, 20):
                            current_piece.y = i
                            break
                        else:
                            current_piece.y = 20

        shapePos = convert_shape_format(current_piece)
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                locked_position[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score +=clear_rows(grid, locked_position)*100

        draw_window(window, grid,score)
        draw_next_shape(next_piece, window)
        draw_hold(hold_piece, window, hold)
        pg.display.update()

        if check_lost(locked_position):
            draw_loose(window,grid,score)
            pg.display.update()
            pg.time.delay(5000)
            run = False


def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_start(window)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=False
            if event.type==pg.KEYDOWN:
                main(window)
    pg.display.quit()


window = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption('Tetris Chido')
main_menu(window)  # start game
