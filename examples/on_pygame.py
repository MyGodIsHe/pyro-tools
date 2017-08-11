#!/usr/bin/env python
import pygame
from pyro_tools import spr_open
from pyro_tools import act_open


class Animation:

    def __init__(self, frames=None, time=100):
        self.x = 0
        self.y = 0
        self.frames = frames
        self.time = time
        self.work_time = 0
        self.skip_frame = 0
        self.frame = 0
        if isinstance(time, list):
            self.__update = self.__update_any_time
        else:
            self.__update = self.__update_const_time

    def update(self, dt):
        self.work_time += dt
        self.__update(dt)

    def __update_const_time(self, dt):
        self.skip_frame = self.work_time / self.time
        if self.skip_frame > 0:
            self.work_time = self.work_time % self.time
            self.frame += self.skip_frame
            if self.frame >= len(self.frames):
                self.frame = 0

    def __update_any_time(self, dt):
        while self.work_time - self.time[self.frame] > 0:
            self.work_time -= self.time[self.frame]
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0

    def get_frame(self):
        return self.frames[self.frame]

    def draw(self, surface):
        for frame in self.get_frame():
            surface.blit(frame.sprite, (self.x + frame.offset_x, self.y + frame.offset_y))


def setup_animations(actor, sprites):
    animations = []

    for i in sprites:
        sprites.fill_rgba(i)
        i.data = ''.join(i.data)

    for animation in actor.animations:
        image_frames = []

        for subframes in animation.frames:
            image_subframes = []
            for frame in subframes:
                if frame.direction != 0:
                    continue
                sprite = sprites[frame.image_n]
                sprite = pygame.image.fromstring(sprite.data,
                                                 (sprite.width, sprite.height),
                                                 'RGBA')
                sprite = pygame.transform.rotate(sprite, -frame.rotation)
                frame.sprite = sprite
                image_subframes.append(frame)
            if image_subframes:
                image_frames.append(image_subframes)
        if len(image_frames):
            speed = animation.speed
            animations.append(Animation(image_frames, int(speed*40)))
    return animations


if __name__ == '__main__':
    pygame.init()

    display = pygame.display.set_mode((800, 600))

    screen = pygame.Surface(display.get_size())

    draw_objects = []

    wolfs = setup_animations(act_open('data/wolf.act'), spr_open('data/wolf.spr'))
    wolfs = [x for i, x in enumerate(wolfs) if i % 4 == 0]
    y = 20
    for i in wolfs:
        i.x = 50
        i.y = y
        y += 100
    draw_objects += wolfs

    lunatics = setup_animations(act_open('data/lunatic.act'), spr_open('data/lunatic.spr'))
    lunatics = [x for i, x in enumerate(lunatics) if i % 4 == 2]
    y = 20
    for i in lunatics:
        i.x = 250
        i.y = y
        y += 100
    draw_objects += lunatics

    green_plant = setup_animations(act_open('data/green_plant.act'), spr_open('data/green_plant.spr'))
    green_plant = [x for i, x in enumerate(green_plant) if i % 4 == 2]
    y = 20
    for i in green_plant:
        i.x = 450
        i.y = y
        y += 100
    draw_objects += green_plant

    clock = pygame.time.Clock()

    done = False
    dt = 0
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    done = True
                

        for obj in draw_objects:
            obj.update(dt)

        screen.fill((255,255,255))

        for obj in draw_objects:
            obj.draw(screen)

        display.blit(screen,(0,0))
        pygame.display.flip()

        dt = clock.tick(40)