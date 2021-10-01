def positions(pixels):
    items = {}
    # dictionary to look up the object label - store rgb values in a tuple key = name as it's value
    labels = {}
    labels[(255,0,0)] = "blue"
    labels[(0,255,0)] = "green"
    labels[(255,255,0)] = "cyan"
    labels[(0,0,255)] = "red"
    labels[(0,255,255)] = "yellow"
    labels[(0,200,255)] = "orange"
    labels[(255,255,255)] = "white"

    # loop through each pixel element in the list
    for pixel in pixels:
        (b,g,r,x,y) = pixel #store the colour value and size
        key = (b,g,r) #store colour value tuple in str array to str iterate over
        # colour has already been seen
        if key in items: # checks if the current colour key is in the dict
            minX, maxX, minY, maxY, label = items[key]
            # checks if the min and max value of x and y
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