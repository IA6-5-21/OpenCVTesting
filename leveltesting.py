import numpy as np
import cv2
from matplotlib import pyplot as plt

def find_parameters_for_canny_edge(image, sigma=0.23):
        # compute the median of the single channel pixel intensities
        median = np.median(image)
        # find bounds for Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))
        print(lower,upper)
        return lower, upper

morph_dilate_kernel_size = (7, 7)
morph_rect_kernel_size = (6, 1)

img = cv2.imread("./images/90.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img = clahe.apply(img)
canny_threshold_1, canny_threshold_2 = find_parameters_for_canny_edge(img)
#img = cv2.blur(img, (3, 3))
img = cv2.medianBlur(img, 15)
edges = cv2.Canny(img, canny_threshold_1,canny_threshold_2)

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
    MiddleOfImage = len(edgeImage[0])/2
    print(MiddleOfImage)
    for i in range(0, heightOfImage):
        if(edgeImage[i][MiddleOfImage] == 255):
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


try:
    print(f"{findLevelFromEdges(h_edges)} %")
except:
    print("Error")
plt.subplot(121), plt.imshow(edges, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(h_edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
