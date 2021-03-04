import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt

morph_dilate_kernel_size = (7, 7)
morph_rect_kernel_size = (6, 1)


img = cv2.imread('Image/95.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img = cv2.blur(img, (3, 3))
img = cv2.medianBlur(img, 15)
edges = cv2.Canny(img, 49, 183)

h_edges = cv2.morphologyEx(edges, cv2.MORPH_DILATE, morph_dilate_kernel_size)
horizontal_structure = cv2.getStructuringElement(
    cv2.MORPH_RECT, morph_rect_kernel_size)
# to the edges, apply morphological opening operation to remove vertical lines from the contour image
h_edges = cv2.morphologyEx(h_edges, cv2.MORPH_OPEN, horizontal_structure)
# print(h_edges)


# dst=h_edges

def findLevelFromEdges(edgeImage):
    bottomIsDetected = False
    middleIsDetected = False
    topIsDetected = False
    hasBeenZero = False
    bottom, middle, top = 0, 0, 0
    heightOfImage = len(edgeImage)
    for i in range(0, heightOfImage):
        if(edgeImage[i][320] == 255):
            if(topIsDetected == False):
                top = heightOfImage-i
                topIsDetected = True
            elif(middleIsDetected == False and hasBeenZero == True):
                middle = heightOfImage-i
                middleIsDetected = True
            elif(bottomIsDetected == False and hasBeenZero == True):
                bottom = heightOfImage-i
                bottomIsDetected = True
            hasBeenZero = False
        else:
            hasBeenZero = True
    middle -= bottom
    top -= bottom
    levelPercent = (middle/top)*100
    print(bottom, middle, top)
    return round(levelPercent, 1)


print(f"{findLevelFromEdges(h_edges)} %")
plt.subplot(121), plt.imshow(edges, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(h_edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
