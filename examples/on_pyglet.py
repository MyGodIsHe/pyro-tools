#!/usr/bin/env python
import pyglet
from pyglet.image import Animation, AnimationFrame, ImageData
from pyglet.sprite import Sprite
from pyglet.window import mouse, Window
from pyro_tools.sprite import spr_open
from pyro_tools.actor import act_open


def apply_actor(sprites, frame):
    sprite = sprites[frame.image_n]
    return ImageData(sprite.width, sprite.height, 'RGBA', ''.join(sprite.data))


def reverse(sprite):
    rdata = []
    for i in xrange(sprite.height - 1, -1, -1):
        rdata += sprite.data[i * sprite.width:(i + 1) * sprite.width]
    sprite.data = rdata


def setup_animations(actor, sprites):
    animations = []

    for i in sprites:
        sprites.fill_rgba(i)
        reverse(i)

    for animation in actor.animations:
        image_frames = []
        speed = 0.5 * animation.speed / len(animation.frames)
        for subframes in animation.frames:
            for frame in subframes:
                if frame.direction != 0:
                    continue
                frame = apply_actor(sprites, frame)
                animation_frame = (AnimationFrame(frame, speed))
                image_frames.append(animation_frame)
        if len(image_frames):
            animations.append(Animation(image_frames))
    return animations


window = Window(800, 600, resizable=True)
scale = 1.0
camera_x = 0.0
camera_y = 0.0
label_fps = pyglet.text.Label('FPS',
                              font_name='Times New Roman',
                              font_size=12,
                              x=795, y=5,
                              anchor_x='left', anchor_y='top')

actor = act_open('data/wolf.act')
sprites = spr_open('data/wolf.spr')
animations = setup_animations(actor, sprites)

drawableObjects = [Sprite(x=x, y=y, img=imgs) for x, y, imgs in [
    (0, 0, animations[0]),
    (100, 0, animations[4]),
    (200, 0, animations[8]),
    (300, 0, animations[12]),
    (400, 0, animations[16]),
    (500, 0, animations[20]),
]]

drawableObjects = [(i.x, i.y, i) for i in drawableObjects]


@window.event
def on_draw():
    global camera_x, camera_y
    window.clear()
    for x, y, i in drawableObjects:
        i.scale = scale
        i.x = x + (window.width // 2 - camera_x - x) * (1 - scale) + camera_x
        i.y = y + (window.height // 2 - camera_y - y) * (1 - scale) + camera_y
        i.draw()
    label_fps.draw()


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scale
    if scroll_y > 0:
        scale *= 1.05
    elif scroll_y < 0:
        scale *= 0.95


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camera_x, camera_y
    if buttons & mouse.LEFT:
        camera_x += dx
        camera_y += dy


pyglet.app.run()
