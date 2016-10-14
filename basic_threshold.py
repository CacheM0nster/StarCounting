from PIL import Image
import sys, os


def threshold(t, image):
  intensity_array = []
  for w in range(0, image.size[1]):
    for h in range(0, image.size[0]):
      intensity = image.getpixel((h, w))
      if intensity <= t:
        x = 0
      else:
        x = 255
      intensity_array.append(x)
  image.putdata(intensity_array)
  return image
