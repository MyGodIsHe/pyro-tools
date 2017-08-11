#!/usr/bin/env python
""" Extract actions from Ragnarok data
    Format: http://mist.in/gratia/ro/spr/ActFileFormatFix.html
"""
import sys
from struct import unpack

__all__ = ['Frame', 'Animation', 'Actor', 'act_open']


class Frame(object):
    def __init__(self):
        self.offset_x = None
        self.offset_y = None
        self.image_n = None
        self.direction = None
        self.color = None
        self.scale_x = None
        self.scale_y = None
        self.rotation = None
        self.size_x = None
        self.size_y = None

    def __str__(self):
        return repr(self.__dict__)

    def __unicode__(self):
        return self.__str__()


class Animation(object):
    def __init__(self):
        self.speed = None
        self.frames = []


class Actor(object):
    def __init__(self):
        self.version = None
        self.animations = []
        self.sounds = []


def act_open(file_path):
    def to_char():
        return unpack('b', f.read(1))[0]

    def to_short():
        return unpack('h', f.read(2))[0]

    def to_int():
        return unpack('i', f.read(4))[0]

    def to_float():
        return unpack('f', f.read(4))[0]

    def read_frame():
        frame = Frame()
        frame.offset_x = to_int()
        frame.offset_y = to_int()
        frame.image_n = to_int()
        frame.direction = to_int()
        frame.color = f.read(4)
        if actions.version >= 2:
            frame.scale_x = to_float()
            if actions.version >= 4:
                frame.scale_y = to_float()
            else:
                frame.scale_y = frame.scale_x
            if actions.version >= 2:
                frame.rotation = to_int()
                dont_jump = to_int()
            else:
                dont_jump = None
            if dont_jump:
                f.seek(f.tell() + 12)
            if actions.version >= 5:
                frame.size_x = to_int()
                frame.size_y = to_int()
        # sound_no = to_int()
        return frame

    f = file(file_path, 'rb')

    f.seek(2)
    actions = Actor()
    actions.version = to_char()

    f.seek(4)
    animations_count = to_short()

    # skip trash
    f.seek(f.tell() + 10)

    # read actions
    for i_a in xrange(animations_count):
        frames_count = to_int()

        animation = Animation()
        for i_f in xrange(frames_count):
            # skip trash
            f.seek(f.tell() + 32)

            subframes_count = to_int()
            subframes = []
            for i_sf in xrange(subframes_count):
                subframes.append(read_frame())

            # todo: wtf
            f.seek(f.tell() + 8)
            # if version >= 2:
            #    extra_info = to_int()
            #    if extra_info:
            #        f.seek(f.tell() + 4)
            #        extra_x = to_int()
            #        extra_y = to_int()
            #        print "Extra:", extra_x, extra_y
            animation.frames.append(subframes)
        actions.animations.append(animation)

    # sound
    n_sound_file = to_int()
    for i in xrange(n_sound_file):
        sound_file_name = f.read(40)
        actions.sounds.append(sound_file_name)

    # speed
    for animation in actions.animations:
        animation.speed = to_float()
    f.close()
    return actions


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Need path to the act file"
    else:
        actor = act_open(sys.argv[1])
        print 'Version:', actor.version
        print 'Animations:', len(actor.animations)
        for animation in actor.animations:
            print "Frames: %2i, Speed: %2.2f" % (len(animation.frames), animation.speed)
        print 'Sounds:'
        for sound in actor.sounds:
            print sound
