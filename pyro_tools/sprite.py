#!/usr/bin/env python
""" Extract sprites from Ragnarok data
    Format: http://mist.in/gratia/ro/spr/SprFileFormat.html
"""
import sys
import os
from PIL import Image
from struct import unpack

__all__ = ['Frame', 'Frames', 'spr_open']


def int2(f):
    return unpack('h', f.read(2))[0]


class Frame(object):

    def __init__(self, width=None, height=None, data=None):
        self.width = width
        self.height = height
        self.data = data

    def uncompress(self):
        """ RLE uncompress
        """
        prev = None
        data = []
        for i in self.data:
            b = ord(i)
            if prev == 0:
                if b == 0:
                    data.append(b)
                else:
                    data += [0] * (b - 1)
            else:
                data.append(b)
            prev = b
        return data


class Frames(list):

    def __init__(self):
        self.palette = []
        super(Frames, self).__init__()

    def fill_rgbx(self, frame):
        frame.data = [self.palette[i] for i in frame.uncompress()]

    def fill_rgba(self, frame):
        palette = self.palette[0:1] + [i[:3] + chr(255) for i in self.palette[1:]]
        frame.data = [palette[i] for i in frame.uncompress()]


def spr_open(name):
    f = file(name, 'rb')

    f.seek(4)
    frames_count = int2(f)

    # read frames
    f.seek(8)
    frames = Frames()
    for i in xrange(frames_count):
        frame = Frame()
        frame.width = int2(f)
        frame.height = int2(f)
        size = int2(f)
        frame.data = f.read(size)
        frames.append(frame)

    # read palette
    frames.palette = [f.read(4) for _ in xrange(256)]

    f.close()
    return frames


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Need path to the spr file"
    else:
        file_path = sys.argv[1]
        filename, ext = os.path.splitext(file_path)
        frames = spr_open(file_path)
        for i, frame in enumerate(frames, 1):
            frames.fill_rgba(frame)
            im = Image.fromstring('RGBA', (frame.width, frame.height), ''.join(frame.data))
            fn = "%s-%i.png" % (filename, i)
            im.save(fn, 'PNG')
            print fn
