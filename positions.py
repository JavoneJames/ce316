def positions(pixels):
    items = {}

    # dictionary to look up the object label
    labels = {(255, 0, 0): "blue", (0, 255, 0): "green", (255, 255, 0): "cyan", (0, 0, 255): "red",
              (0, 255, 255): "yellow", (0, 200, 255): "orange", (255, 255, 255): "white"}

    for pixel in pixels:  # loop through pixel value stored in the list
        (b, g, r, x, y) = pixel  # unpack BGR values and coords
        key = (b, g, r)
        # colour has already been seen
        if key in items:  # check if the key exists int he dict already
            minX, maxX, minY, maxY, label = items[key]  # unpacks the values of the key
            maxX, maxY, minX, minY = get_min_max(maxX, maxY, minX, minY, x,
                                                 y)  # calls function to check if the old values or small or bigger than the old ones
            items[key] = (
            minX, maxX, minY, maxY, label)  # store the results back into the dict as new values of the key
        else:
            # add colour
            # format (minX, maxX, minY, maxY, label)
            items[key] = (x, x, y, y, labels[key])

    # now we have all of the x,y values, we can calculate midpoints
    for colour, pixelData in items.items():
        minX, maxX, minY, maxY, label = pixelData  # unpack the data we have so far
        # calculate and store the midpoint of X and Y
        midX = minX + ((maxX - minX) // 2)  # calculate and store midpoint for x
        midY = minY + ((maxY - minY) // 2)  # same as above
        # store the result back into the dict along with the midpoint for X and Y
        items[colour] = (minX, maxX, midX, minY, maxY, midY, label)
        # print(items[colour])
    return items


def get_min_max(maxX, maxY, minX, minY, x, y):
    if x < minX:
        minX = x
    if y < minY:
        minY = y
    if x > maxX:
        maxX = x
    if y > maxY:
        maxY = y
    return maxX, maxY, minX, minY
