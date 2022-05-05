import cv2
import math
import random
import numpy as np

gray = 127
white = 255


def dist_btwn(pt1, pt2):
    res = math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    return res


def find_shortest_path(image, start, end):
    open_ = {}
    closed = []
    img_copy = image.copy()
    height, width = image.shape
    open_[start] = dist_btwn(start, end)

    while end not in closed:
        # Finding the node having min distance from end
        min_valued_node = min(open_, key=open_.get)
        # Storing that node in closed
        closed.append(min_valued_node)
        # Poping that node to find the next min
        open_.pop(min_valued_node)
        x, y = min_valued_node
        img_copy[x, y] = gray

        if y - 1 >= 0:
            if img_copy[x, y - 1] == white:
                open_[(x, y - 1)] = dist_btwn((x, y - 1), end)

        if y + 1 < width:
            if img_copy[x, y + 1] == white:
                open_[(x, y + 1)] = dist_btwn((x, y + 1), end)

        if x - 1 >= 0:
            if img_copy[x - 1, y] == white:
                open_[(x - 1, y)] = dist_btwn((x - 1, y), end)

        if x + 1 < height:
            if img_copy[x + 1, y] == white:
                open_[(x + 1, y)] = dist_btwn((x + 1, y), end)

        if x - 1 >= 0 and y - 1 >= 0:
            if img_copy[x - 1, y - 1] == white:
                open_[(x - 1, y - 1)] = dist_btwn((x - 1, y - 1), end)

        if x - 1 >= 0 and y + 1 < width:
            if img_copy[x - 1, y + 1] == white:
                open_[(x - 1, y + 1)] = dist_btwn((x - 1, y + 1), end)

        if x + 1 < height and y - 1 >= 0:
            if img_copy[x + 1, y - 1] == white:
                open_[(x + 1, y - 1)] = dist_btwn((x + 1, y - 1), end)

        if x + 1 < height and y + 1 < width:
            if img_copy[x + 1, y + 1] == white:
                open_[(x + 1, y + 1)] = dist_btwn((x + 1, y + 1), end)

        if not bool(open_):
            break

        cv2.namedWindow("Finding path ....", cv2.WINDOW_NORMAL)
        cv2.imshow("Finding path ....", img_copy)
        cv2.waitKey(1)

    cv2.destroyWindow("Finding path ....")
    return closed


# img = cv2.imread("testMaze.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.resize(img, (20, 20))

# Defining a small white canvas for less calculation
r, c = 20, 20
maze = np.full((r, c), 255)

# Randomly making some pixels black
for i in range(r):
    for j in range(c):
        # Generating random numbers in range [0.0, 1.0)
        n = random.random()
        # Probability of n to be less than 0.3 is 0.3
        # Hence, probability of a pixel of getting converted to black pixel is also 0.3
        if n < 0.3:
            maze[i, j] = 0

# Resizing maze to (200, 200)
maze = cv2.resize(maze.astype(np.uint8), (200, 200))

# Thresholding resized pixelated maze
ret, maze = cv2.threshold(maze, 127, 255, cv2.THRESH_BINARY)

for i in range(0, 20):
    for j in range(0, 20):
        maze[i, j] = maze[180 + i, 180 + j] = 255
img = maze
r, c = img.shape

shortestPath = find_shortest_path(img, (0, 0), (r - 1, c - 1))

for i in range(len(shortestPath)):
    x, y = shortestPath[i]
    img[x, y] = gray

    if y - 1 >= 0:
        if img[x, y - 1] == white:
            img[x, y - 1] = gray

    if y + 1 < c:
        if img[x, y + 1] == white:
            img[x, y + 1] = gray

    if x - 1 >= 0:
        if img[x - 1, y] == white:
            img[x - 1, y] = gray

    if x + 1 < r:
        if img[x + 1, y] == white:
            img[x + 1, y] = gray

    if x - 1 >= 0 and y - 1 >= 0:
        if img[x - 1, y - 1] == white:
            img[x - 1, y - 1] = gray

    if x - 1 >= 0 and y + 1 < c:
        if img[x - 1, y + 1] == white:
            img[x - 1, y + 1] = gray

    if x + 1 < r and y - 1 >= 0:
        if img[x + 1, y - 1] == white:
            img[x + 1, y - 1] = gray

    if x + 1 < r and y + 1 < c:
        if img[x + 1, y + 1] == white:
            img[x + 1, y + 1] = gray

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

