import numpy as np
import cv2
#import fullbright (for cython if using)

# convert pixels to full brightness
# adapted from email pointers
def fullbright(image):

    height = image.shape[0]
    width = image.shape[1]

    pixels = []

    for y in range(0, height):
        for x in range(0, width):

            b,g,r = image[y, x]
            if b > 0 or g > 0 or r > 0:

                # red, <10 on g&b are thresholds because centre of items are off
                if r > 0 and g < 10 and b < 10:
                    image[y, x][0] = 0
                    image[y, x][1] = 0
                    image[y, x][2] = 255
                    pixels.append((0,0,255,x,y))

                # green
                elif r < 15 and g > 0 and b < 15:
                    image[y, x][0] = 0
                    image[y, x][1] = 255
                    image[y, x][2] = 0
                    pixels.append((0,255,0,x,y))

                # blue
                elif r == 0 and g == 0 and b > 0:
                    image[y, x][0] = 255
                    image[y, x][1] = 0
                    image[y, x][2] = 0
                    pixels.append((255,0,0,x,y))

                # cyan (red for middle pixels)
                elif r < 50 and g > 0 and b > 0:
                    image[y, x][0] = 255
                    image[y, x][1] = 255
                    image[y, x][2] = 0
                    pixels.append((255,255,0,x,y))

                # yellow or orange
                elif r > 0 and g > 0 and b < 40:
                    rgratio = r-g
                    # orange
                    if rgratio > 20 and rgratio < 70:
                        image[y, x][0] = 0
                        image[y, x][1] = 200
                        image[y, x][2] = 255
                        pixels.append((0,200,255,x,y))
                    else:
                        #yellow
                        image[y, x][0] = 0
                        image[y, x][1] = 255
                        image[y, x][2] = 255
                        pixels.append((0,255,255,x,y))
                # white
                elif r > 0 and g > 0 and b > 0:
                    image[y, x][0] = 255
                    image[y, x][1] = 255
                    image[y, x][2] = 255
                    pixels.append((255,255,255,x,y))

                else:
                    print("fullbright: unrecognised colour")

    return pixels

# convert pixel list to a dictionary, colour values as keys, with extents
# adapted from email pointers
def positions(pixels):
    items = {}

    # dictionary to look up the object label
    labels = {}
    labels[(255,0,0)] = "blue"
    labels[(0,255,0)] = "green"
    labels[(255,255,0)] = "cyan"
    labels[(0,0,255)] = "red"
    labels[(0,255,255)] = "yellow"
    labels[(0,200,255)] = "orange"
    labels[(255,255,255)] = "white"

    for pixel in pixels:
        (b,g,r,x,y) = pixel
        key = (b,g,r)

        # colour has already been seen
        if key in items:
            minX, maxX, minY, maxY, label = items[key]
            if x < minX:
                minX = x
            if y < minY:
                minY = y
            if x > maxX:
                maxX = x
            if y > maxY:
                maxY = y
            items[key] = (minX, maxX, minY, maxY, label)
        else:
            # add colour
            # format (minX, maxX, minY, maxY, label)
            items[key] = (x, x, y, y, labels[key])
    return items


img = cv2.imread('img/right-035.png')
img1 = img.copy()

# cython version (can remove if not using)
# fullbright.fullbright(img1)

# make pixels bright
# also receive a list of pixels in the format (b, g, r, x, y)
pixels = fullbright(img1)

items = positions(pixels)
for key, value in items.items():
    #print(key, value)
    minX, maxX, minY, maxY, label = value
    cv2.rectangle(img1, (minX-5, minY-5), (maxX+5, maxY+5), key, 1)
    cv2.putText(img1, text=label, org=(maxX+10,maxY),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(255,255,255),
            thickness=1, lineType=cv2.LINE_AA)


# do the same calculations for each image in the list (both left and right)
# keep a log of their coordinates given by these functions
# determine whether the motion is linear


cv2.imshow('image',img)
cv2.imshow('image1',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
