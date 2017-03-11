#!/usr/bin/env python
"""script to hide information within an image"""
from PIL import Image
import sys, binascii


def to2D(pixels, image):
    'convert a 1D list of pixels into a 2D list'
    width, height = image.size
    return [pixels[i * width:(i + 1) * width] for i in xrange(height)]


def setBit(number, offset, value):
    'set number[-offset] = value'
    # format number as a binary list, set value, join list, return decimal
    number = '{0:08b}'.format(number)
    number = list(number)
    number[-offset] = value
    number = ''.join(number)
    number = int(number, base = 2)
    return number


def readPixelData(image):
    'read set of three pixels from an image'
    im = Image.open(image)
    pixels = list(im.getdata())
    return pixels


def hideMessage(pixels, message):
    'hide string within an image'
    value, triple, offset = 0, 0, 1
    # set pixel in image depending on hidden message
    for c in list(message):
        pixels[value][triple] = setBit(pixels[value][triple], offset, c)
        if (value == len(pixels)):
            value = 0
            offset += 1
        else:
            value += 1
        if (triple == 2):
            triple = 0
        else:
            triple += 1
    return pixels


# read image as first argument on command line
image = str(sys.argv[1])
pixels = readPixelData(image)
pixels = [[i for i in triple] for triple in pixels]

# read message as second argument on command line, then convert to binary
message = str(sys.argv[2])
message = bin(int(binascii.hexlify(message), 16))[2:]

newImage = hideMessage(pixels, message)
