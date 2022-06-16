import sys
import random
import pygame
import pymunk
import pymunk.pygame_util
random.seed(1)


def add_static_L(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255, 0), 5)
    l2 = pymunk.Segment(body, (-150, 0), (-150, -50), 5)
    l1.friction = 1
    l2.friction = 1

    space.add(body, l1, l2)
    return l1, l2


def add_ball(space):
    mass = 3
    radius = 25
    body = pymunk.Body()  # 1
    x = random.randint(120, 300)
    y = random.randint(120, 300)
    body.position = x, y  # 2
    shape = pymunk.Circle(body, radius)  # 3
    shape.mass = mass  # 4
    shape.friction = 1
    space.add(body, shape)  # 5
    return shape


def add_L(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 1
    rotation_center_body.position = (300, 300)

    body = pymunk.Body()
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, -50.0), 5.0)
    l1.friction = 1
    l2.friction = 1
    l1.mass = 8  # 2
    l2.mass = 1
    rotation_center_joint = pymunk.PinJoint(
        body, rotation_center_body, (0, 0), (50, 50)
    )  # 3

    space.add(l1, l2, body, rotation_center_joint)
    return l1, l2


def add_L_2(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body()
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 10.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, -50.0), 5.0)
    l1.friction = 1
    l2.friction = 1
    l1.mass = 8
    l2.mass = 1

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100, 0), (0, 0), 0, joint_limit)

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1, l2


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 500.0)

    # lines = add_static_L(space)
    lines = add_L_2(space)
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


if __name__ == '__main__':
    main()
