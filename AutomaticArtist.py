#

from PIL import Image
from PIL import ImageFilter


test = Image.new("RGB", (5000,5000), (0, 0, 0))
for w in range(test.size[0]):
    for h in range(test.size[1]):
        test.putpixel((w, h), ((w*4+h)%305, (w*h+h*20-w*35)%172,int(h*h/(w+2))%255))
test.filter(ImageFilter.GaussianBlur)
test.show()