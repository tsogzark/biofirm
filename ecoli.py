import sys
import csv
import random
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util

UPPER = 0
COLLISION = {"green": 1, "red": 2}


class ecoli:
    def __init__(self, pos, le, r, color, space, grow_rate, radius, id):
        self.exist_body = pymunk.Body()
        self.exist_body.position = pos
        p1 = (le / 2 * np.sin(r), le / 2 * np.cos(r))
        p2 = (-le / 2 * np.sin(r), -le / 2 * np.cos(r))
        self.cell_body = pymunk.Segment(self.exist_body, p1, p2, radius)
        self.id = id
        self.pos = pos
        self.space = space
        self.radius = radius
        self.color = color
        self.grow_rate = grow_rate
        if color[0] != 0:
            self.cell_body.collision_type = COLLISION["red"]
        if color[1] != 0:
            self.cell_body.collision_type = COLLISION["green"]
        self.r = r
        self.le = le
        self.cell_body.friction = 100
        self.cell_body.mass = 8
        self.cell_body.color = color

        space.add(self.exist_body, self.cell_body)

    def update(self, pos, le, r):
        self.pos = pos
        self.r = r
        self.le = le
        self.exist_body.position = pos
        p1 = (le / 2 * np.sin(r), le / 2 * np.cos(r))
        p2 = (-le / 2 * np.sin(r), -le / 2 * np.cos(r))
        self.cell_body.unsafe_set_endpoints(p1, p2)

    def live(self):
        global UPPER
        if self.le > 50 and random.random() > 0.5:
            return self.division()
        else:
            if UPPER < 500:
                self.update(self.exist_body.position, self.le * (1 + self.grow_rate), self.r)
            return "growing"

    def division(self):
        global UPPER
        global eco
        if UPPER < 500:
            le = self.le
            r = self.r
            x = self.pos[0]
            y = self.pos[1]
            p1 = (x + le / 4 * np.sin(r), y + le / 4 * np.cos(r))
            p2 = (x - le / 4 * np.sin(r), y - le / 4 * np.cos(r))
            e1 = ecoli(p1, le / 2.5, r + random.random(), self.color, self.space, self.grow_rate, self.radius, self.id)
            e2 = ecoli(p2, le / 2.5, r + random.random(), self.color, self.space, self.grow_rate, self.radius, len(eco) + 1)
            return [e1, e2]
        else:
            return "stop"


class ebox():
    def __init__(self, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.position = (0, 0)
        r = 5
        self.bottom = pymunk.Segment(self.body, (0, 800), (800, 800), r)
        self.top = pymunk.Segment(self.body, (0, 0), (800, 0), r)
        self.left = pymunk.Segment(self.body, (0, 0), (0, 800), r)
        self.right = pymunk.Segment(self.body, (800, 0), (800, 800), r)
        space.add(self.body, self.top, self.bottom, self.left, self.right)


def col_process(arbiter, space, data):
    global eco
    for i in range(len(arbiter.shapes)):
        if arbiter.shapes[i].collision_type == COLLISION["red"]:
            if random.random() > 0.9:
                arbiter.shapes[i].color = (200, 200, 0, 255)
                for e in eco:
                    if e.cell_body == arbiter.shapes[i]:
                        e.color = (200, 200, 0, 255)

    return True


def main():
    global UPPER
    global eco
    global circles
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("大肠杆菌基因水平转移演示")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    rgh = space.add_collision_handler(COLLISION["red"], COLLISION["green"])
    rgh.begin = col_process
    frame = ebox(space)
    ecoli_init_pos_green = (np.random.randint(1, 80, size=[20, 2]))
    ecoli_init_pos_red = np.random.randint(1, 80, size=[20, 2])
    ps_init_pos = np.random.randint(1, 80, size=[200, 2])
    for pos in ecoli_init_pos_green:
        pos = tuple(10 * pos)
        eco.append(ecoli(pos, 10, 2 * np.pi * random.random(), (0, 200, 0, 255), space, 0.005, 10, len(eco) + 1))
    for pos in ecoli_init_pos_red:
        pos = tuple(10 * pos)
        eco.append(ecoli(pos, 10, 2 * np.pi * random.random(), (200, 0, 0, 255), space, 0.005, 10, len(eco) + 1))
    for pos in ps_init_pos:
        pos = tuple(10 * pos)
        circles.append(ecoli(pos, 5, 0, (0, 0, 200, 255), space, 0, 5, len(eco) + 1))
    # e1 = ecoli((500, 300), 10, 2 * np.pi * random.random(), (0, 200, 0, 255), space, 0.005, 10)
    # e2 = ecoli((700, 300), 10, np.pi / 6, (200, 0, 0, 255), space, 0.005, 10)
    # c1 = ecoli((400, 400), 5, 0, (0, 0, 200, 255), space, 0, 5)
    # c2 = ecoli((400, 500), 5, 0, (0, 0, 200, 255), space, 0, 5)
    # circles.append(c1)
    # circles.append(c2)
    # eco.append(e1)
    # eco.append(e2)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    n = 0
    red_e = 0
    green_e = 0
    yellow_e = 0
    eco_ids = []
    while True:
        for e in eco:
            if e.color == (200, 0, 0, 255) and not e.id in eco_ids:
                red_e += 1
                eco_ids.append(e.id)
            if e.color == (0, 200, 0, 255) and not e.id in eco_ids:
                green_e += 1
                eco_ids.append(e.id)
            if e.color == (200, 200, 0, 255) and not e.id in eco_ids:
                yellow_e += 1
                eco_ids.append(e.id)
        print("total:%d,red:%d,green:%d,yellow:%d" % (len(eco),red_e, green_e, yellow_e))
        UPPER = len(eco)
        n += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        for i in range(len(eco)):
            re1 = eco[i].live()
            if re1 != "growing" and re1 != "stop":
                space.remove(eco[i].exist_body, eco[i].cell_body)
                del eco[i]
                eco += re1

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    eco = []
    circles = []
    main()
