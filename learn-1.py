import sys
import random
import pygame
import pymunk
import pymunk.pygame_util
random.seed(1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 900.0)

    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        space.step(1/50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)


def add_ball(space):
    mass = 3
    radius = 25
    body = pymunk.Body()
    x = random.randint(120, 300)
    y = random.randint(120, 300)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.friction = 1
    space.add(body, shape)
    return shape


if __name__ == '__main__':
    main()
