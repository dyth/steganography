#!/usr/bin/env python
"""script to show hidden information within an image"""
# run using python show.py <imageName> | less
from PIL import Image
import sys, binascii


def readPixelData(image):
    'read set of three pixels from an image'
    im = Image.open(image)
    width, height = im.size
    pixels = list(im.getdata())
    return pixels, width, height


def getBit(number, offset):
    'return number[-offset]'
    number = '{0:08b}'.format(number)
    number = list(number)
    return number[-offset]


def findMessage(pixels):
    'return hidden message stored in picture'
    message = []
    for offset in range(1, 2):
        for triple in pixels:
            for n in triple:
                message.append(getBit(n, offset))
    return message


def addPadding(message):
    'return correct padding'
    while ((len(message) % 8) != 7):
        message += '1'
    return message


def toMessage(image):
    'convert message to string'
    message = findMessage(image)
    message = ''.join(message)
    message = addPadding(message)
    message = int(message, 2)
    message = '%x' % message
    if (len(str(message)) % 2 == 1):
        message += '0'
    message = binascii.unhexlify(message)
    return message


image = str(sys.argv[1])
pixels, _, _ = readPixelData(image)
print toMessage(pixels)
