import sys
import random
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util

UPPER = 0
COLLISION = {"green": 1, "red": 2}


class ecoli:
    def __init__(self, pos, le, r, color, space, grow_rate):
        self.exist_body = pymunk.Body()
        self.exist_body.position = pos
        p1 = (le / 2 * np.sin(r), le / 2 * np.cos(r))
        p2 = (-le / 2 * np.sin(r), -le / 2 * np.cos(r))
        self.cell_body = pymunk.Segment(self.exist_body, p1, p2, 10)
        self.pos = pos
        self.space = space
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
        if self.le > 50:
            div_check = 0.5
            if random.randint(0, 100) < div_check * 100:
                return self.division()
            else:
                self.update(self.exist_body.position, self.le * (1 + self.grow_rate), self.r)
                return "growing"
        else:
            self.update(self.exist_body.position, self.le * (1 + self.grow_rate), self.r)
            return "growing"

    def division(self):
        global UPPER
        if UPPER < 300:
            le = self.le
            r = self.r
            x = self.pos[0]
            y = self.pos[1]
            p1 = (x + le / 4 * np.sin(r), y + le / 4 * np.cos(r))
            p2 = (x - le / 4 * np.sin(r), y - le / 4 * np.cos(r))
            e1 = ecoli(p1, le / 2.5, r + random.random(), self.color, self.space, self.grow_rate)
            e2 = ecoli(p2, le / 2.5, r + random.random(), self.color, self.space, self.grow_rate)
            return [e1, e2]
        else:
            return "stop"


class ebox():
    def __init__(self, space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.position = (0, 0)
        r = 5
        self.bottom = pymunk.Segment(self.body, (0, 600), (1200, 600), r)
        self.top = pymunk.Segment(self.body, (0, 0), (1200, 0), r)
        self.left = pymunk.Segment(self.body, (0, 0), (0, 600), r)
        self.right = pymunk.Segment(self.body, (1200, 0), (1200, 600), r)
        space.add(self.body, self.top, self.bottom, self.left, self.right)


def col_process(arbiter, space, data):
    for i in range(len(arbiter.shapes)):
        if arbiter.shapes[i].collision_type == COLLISION["red"]:
            arbiter.shapes[i].color = (200, 200, 0, 255)

    return True


def main():
    global UPPER
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("大肠杆菌基因水平转移演示")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    eco = []
    circles = []
    rgh = space.add_collision_handler(COLLISION["red"], COLLISION["green"])
    rgh.begin = col_process
    frame = ebox(space)
    e1 = ecoli((500, 300), 10, 2 * np.pi * random.random(), (0, 200, 0, 255), space, 0.005)
    e2 = ecoli((700, 300), 10, np.pi / 6, (200, 0, 0, 255), space, 0.005)
    c1 = ecoli((400, 400), 5, 0, (0, 0, 200, 255), space, 0)
    c2 = ecoli((400, 500), 5, 0, (0, 0, 200, 255), space, 0)
    circles.append(c1)
    circles.append(c2)
    eco.append(e1)
    eco.append(e2)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    n = 0
    while True:
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
    main()
