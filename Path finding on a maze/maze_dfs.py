import cv2
import numpy as np
import time
import random

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
img = cv2.cvtColor(maze, cv2.COLOR_GRAY2RGB)
# img = cv2.imread("map.png")
# img = cv2.resize(img, (200, 200))
img[:, :, 0] = img[:, :, 1] = img[:, :, 2] = 0.21 * img[:, :, 0] + 0.72 * img[:, :, 1] + 0.07 * img[:, :, 2]
img = cv2.bitwise_not(img)
r, img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
img_copy = img.copy()

#cv2.imshow("m",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
grey = (128, 128, 128)
orange = (0, 128, 255)
pink = (255, 0, 255)
black = (0, 0, 0)
white=(255,255,255)

w, h, c = img.shape

class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

def get_dist(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


def get_min_dist_node(open_list):
    min_dist = np.inf
    min_node = None
    for node in open_list:
        if open_list[node].g < min_dist:
            min_dist = open_list[node].g
            min_node = open_list[node]
    return min_node


def obstacle(position):
    x, y = position
    if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 0:
        return True
    return False

def goal_reached(position):
    x, y = position
    if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 255:
        return True
    return False

def show_path(node):
    print('show path')
    current_node = node
    path = []
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    path.reverse()
    for i in range(len(path)-1):
        cv2.line(img_copy, path[i], path[i+1], green, 2)
    cv2.namedWindow('final path', cv2.WINDOW_NORMAL)
    cv2.imshow("final path", img_copy)
    cv2.imwrite("final_path.png", img_copy)
    if cv2.waitKey(1) == 'q':
        cv2.destroyAllWindows()
        return

def bfs(start, end):
    print('bfs called')
    open_list = []
    closed_list = []
    start_node =  Node(None, start)
    open_list.append(start_node)
    #open_list[start] = start_node
    while len(open_list)>0:
        # print("dict size = ", len(open_list))
        #current_node = get_min_dist_node(open_list)
        current_node=open_list.pop()
        #print(current_node.position)
        #print("node popped")
        img[current_node.position[1]][current_node.position[0]] = orange
        #open_list.pop(current_node.position)

        if current_node.position == end:
            print("Goal Reached")
            show_path(current_node)
            return

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (w - 1) or node_position[0] < 0 or node_position[1] > (h - 1) or node_position[1] < 0:
                continue
            if node_position in closed_list:
                continue
            if obstacle(node_position):
                continue
            
            img[node_position[1]][node_position[0]] = pink
            new_node = Node(current_node, node_position)
            if new_node.position not in open_list:
                if new_node.position not in closed_list:
                    open_list.append(new_node)
            
        
        if current_node.position not in closed_list:
            closed_list.append(current_node.position)
        
        cv2.namedWindow('path_finding', cv2.WINDOW_NORMAL)
        cv2.imshow("path_finding", img)
        cv2.waitKey(1)
    
if __name__ == '__main__':
    for i in range(w):
        for j in range(h):
            if (img[i][j] == red).all():
                start = (j, i)
                break
            
    for i in range(w):
        for j in range(h):
            if (img[i][j] == blue).all():
                end = (j, i)
                break

    #print(start)
    #print(end)

    start = (0,0)
    end = (199,199)
    img[start[0]][start[1]]=red
    img[end[0]][end[1]]=blue
    begin_ = time.time()
    bfs(start, end)
    end = time.time()

    print("algorithm time = ", (end-begin_))

    cv2.namedWindow("path_finding", cv2.WINDOW_NORMAL)
    cv2.imshow("path_finding", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

