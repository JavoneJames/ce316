import cv2


def fullbright(image):
    img = cv2.imread(image)
    ny = img.shape[0]
    nx = img.shape[1]

    pixels = []

    for y in range(0, ny):  # loop through the lines of the image
        for x in range(0, nx):  # loop through the pixels oer line in the image
            b, g, r = img[y, x]  # store the rbg values of the pixel - BGR format
            if b > 0 or g > 0 or r > 0:  # cehck if the pixel is not black
                # red, <10 on g&b are thresholds because centre of items are off
                if r > 0 and g < 50 and b < 50:  # check if the pixel value is red/within shade
                    img[y, x][0] = 0  # check pixel value to default red to brighten
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
                elif r > 0 and g > 0 and b < 40:  # check if rbg value is a mixture of r and g
                    rgratio = r - g  # subtract the difference
                    # orange
                    if rgratio > 20 and rgratio < 70:  # check if ratio is more than 20 and less than 70 to get orange
                        img[y, x][0] = 0
                        img[y, x][1] = 200
                        img[y, x][2] = 255
                        pixels.append((0, 200, 255, x, y))
                    else:  # it is yellow
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
