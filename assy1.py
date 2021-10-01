import sys
import time
import positions
import fullbright
import cv2
from multiprocessing import Pool
import math

DEBUG_MODE = False


def calc_frame(image):
    pixels = fullbright.fullbright(image)
    items = positions.positions(pixels)
    return items


def calc_distance(xL, xR, centerX):
    focalLength = 12
    baseline = 3500

    if xL > centerX:
        xL = xL - centerX
    else:
        xL = centerX - xL

    if xR > centerX:
        xR = xR - centerX
    else:
        xR = centerX - xR

    denominator = (xL - xR) / 1E5

    if (denominator == 0):
        return -1

    xDistance = 42000 / denominator

    return xDistance


if __name__ == '__main__':

    nframes = int(sys.argv[1])

    framePairs = []
    imageCentres = {}
    distances = {}
    frameFirstLast = {}
    deviations = {}

    with Pool(2) as p:
        t0 = time.time()
        for frame in range(0, nframes):
            argv_frame = 'img/' + sys.argv[2] % frame
            sys_argv_frame = 'img/' + sys.argv[3] % frame
            fn_left, fn_right = p.map(calc_frame, [argv_frame, sys_argv_frame])

            shape = cv2.imread(argv_frame).shape
            # (centerX, centerY)
            xCenter = shape[0] // 2
            yCenter = shape[1] // 2

            imageCentres[frame] = (xCenter, yCenter)

            framePairs.append((fn_left, fn_right))

    deltas = []

    for counter, frame in enumerate(framePairs):

        # do this for each item in this frame
        leftFrame = frame[0]
        rightFrame = frame[1]

        frameItemDistances = {}

        for colour, item in leftFrame.items():

            # (minX, maxX, midX, minY, maxY, midY, label)

            # deltas
            previousFrameNo = counter - 1
            try:
                if previousFrameNo > -1:
                    # there is a previous frame
                    previousX = framePairs[previousFrameNo][0][colour][2]
                    previousY = framePairs[previousFrameNo][0][colour][5]
                    # compare it with the current y
                    currentX = framePairs[counter][0][colour][2]
                    currentY = framePairs[counter][0][colour][5]
                    # calculate deltas
                    dX = currentX - previousX
                    dY = currentY - previousY

                    # calculate atan2
                    result = math.degrees(math.atan2(dY, dX))
                    degrees = (result + 360) % 360

                    # store in a dictionary or something?
                    if result != 0:
                        deltas.append((framePairs[counter][0][colour][6], result, degrees))
                else:
                    currentX = framePairs[counter][0][colour][2]
                    currentY = framePairs[counter][0][colour][5]
            except KeyError:
                if DEBUG_MODE:
                    print("out of bounds key")

            try:
                xLMid = leftFrame[colour][2]
                xRMid = rightFrame[colour][2]

                imgCentreX = imageCentres[counter][1]

                distance = calc_distance(xLMid, xRMid, imgCentreX)
                frameItemDistances[colour] = distance

            except KeyError:
                if DEBUG_MODE:
                    print("empty frame", colour)

        distances[counter] = frameItemDistances

    # determine the ship
    maxChange = {}
    for key, val in enumerate(deltas):
        colour = val[0]

        previous = 0
        current = val[2]

        if key - 1 >= 0:
            previous = deltas[key - 1][2]

        change = abs(int(current - previous))

        if colour in maxChange:
            # update
            maxChange[colour] = maxChange[colour] + change
        else:
            # add
            maxChange[colour] = change
    labels = {(255, 0, 0): "blue", (0, 255, 0): "green", (255, 255, 0): "cyan", (0, 0, 255): "red",
              (0, 255, 255): "yellow", (0, 200, 255): "orange", (255, 255, 255): "white"}
    for key, value in distances.items():
        for colour, distance in value.items():
            print("{:>3}{:>12}{:.2e}".format(key + 1, labels[colour], distance))
