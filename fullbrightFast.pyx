import cython
import cv2
from libc.stdint cimport (uint8_t)

# omit array bounds checking
@cython.boundscheck(False)
cpdef fullbright(str image):

    cdef int x,y,nx,ny
    cdef uint8_t b,g,r
    cdef list pixels

    img = cv2.imread(image)
    ny = img.shape[0]
    nx = img.shape[1]

    pixels = []

    for y in range(0, ny):
        for x in range(0, nx):
            b, g, r = img[y, x]
            if b > 0 or g > 0 or r > 0:
                # red, <10 on g&b are thresholds because centre of items are off
                if r > 0 and g < 10 and b < 10:
                    img[y, x][0] = 0
                    img[y, x][1] = 0
                    img[y, x][2] = 255
                    pixels.append((0, 0, 255, x, y))
                # green
                elif r < 15 and g > 0 and b < 15:
                    img[y, x][0] = 0
                    img[y, x][1] = 255
                    img[y, x][2] = 0
                    pixels.append((0, 255, 0, x, y))

                # blue
                elif r == 0 and g == 0 and b > 0:
                    img[y, x][0] = 255
                    img[y, x][1] = 0
                    img[y, x][2] = 0
                    pixels.append((255, 0, 0, x, y))

                # cyan (red for middle pixels)
                elif r < 50 and g > 0 and b > 0:
                    img[y, x][0] = 255
                    img[y, x][1] = 255
                    img[y, x][2] = 0
                    pixels.append((255, 255, 0, x, y))

                # yellow or orange
                elif r > 0 and g > 0 and b < 40:

                    rgratio = r - g
                    # orange
                    if rgratio > 20 and rgratio < 70:
                        img[y, x][0] = 0
                        img[y, x][1] = 200
                        img[y, x][2] = 255
                        pixels.append((0, 200, 255, x, y))
                    else:
                        # yellow
                        img[y, x][0] = 0
                        img[y, x][1] = 255
                        img[y, x][2] = 255
                        pixels.append((0, 255, 255, x, y))

                # white
                elif r > 0 and g > 0 and b > 0:
                    img[y, x][0] = 255
                    img[y, x][1] = 255
                    img[y, x][2] = 255
                    pixels.append((255, 255, 255, x, y))

                else:
                    print("fullbright: unrecognised colour")

    return pixels

