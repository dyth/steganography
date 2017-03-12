#!/usr/bin/env python
"""script to hide information within an image"""
# run using python hide.py <sampleImageName> "<sampleMessage>" <outImageName>
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
    width, height = im.size
    pixels = list(im.getdata())
    return pixels, width, height


def hideMessage(pixels, message):
    'hide string within an image'
    value, triple, offset = 0, 0, 1
    # set pixel in image depending on hidden message
    for c in list(message):
        pixels[value][triple] = setBit(pixels[value][triple], offset, c)
        if (value == len(pixels)):
            value = 0
            offset += 1
        if (triple == 2):
            triple = 0
            value += 1
        else:
            triple += 1
    return pixels


# get arguments from variables
image = str(sys.argv[1])
message = str(sys.argv[2])
imageOutput = str(sys.argv[3])

# read image as first argument on command line
pixels, width, height = readPixelData(image)
pixels = [[i for i in triple] for triple in pixels]

# read message as second argument on command line, then convert to binary
message = bin(int(binascii.hexlify(message), 16))[2:]

pixels = hideMessage(pixels, message)

# create hidden image
img = Image.new('RGB', (width, height))
pixels = [tuple(triple) for triple in pixels]
img.putdata(pixels)
img.save(imageOutput)
