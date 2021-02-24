import cv2
import numpy as np

cap=cv2.VideoCapture(0)

if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read the video
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
 
    # Converting the image to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 20,30)

    edges_high_tresh = cv2.Canny(gray,60,120)

    images = np.hstack((gray, edges, edges_high_tresh))
    # Display the resulting frame
    cv2.imshow('Frame', images)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()