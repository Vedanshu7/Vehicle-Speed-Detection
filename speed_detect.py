
# //////////////////////////////////////////////////////////////////////////////////////////////
# simultaneous
import threading
import numpy as np
import cv2
import time
import os

input_image = 'input-image.jpg'
input_video = 'input.mp4'
# Let's load a simple image with 3 black squares
image = cv2.imread(input_image)
cv2.waitKey(0)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 30, 200)

cv2.waitKey(0)

# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
contours, hierarchy = cv2.findContours(edged,
                                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cv2.imshow('Canny Edges After Contouring', edged)

# cv2.waitKey(0)

arr = []
arr2 = []

print("Number of Contours found = " + str(len(contours)))
#print(contours)

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    #print(x,end=" ")
    #print(y,end=" ")
    #print(w,end=" ")
    #print(h)
    # if cv2.contourArea(contour) < 0:
    #     continue
    if w < 100:
        continue
    # if h > 10:
    #     continue
    # print(x, y)
    arr.append(y)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f"Coordinates:{x,y} x/y", (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 3)

# Draw all contours
# -1 signifies drawing all contours
# cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
cv2.imwrite(f"output.jpeg",image)
arr.sort()


for i in range(len(arr)-1):
    if arr[i+1]-arr[i] > 70:
        arr2.append(arr[i])
temp = abs(arr2[-1]-arr[-1])
if temp > 70:
    arr2.append(arr[-1])

for y in arr2:
    cv2.line(image, (0, y), (2000, y) ,(255, 0, 0), 5)

cv2.imwrite(f"output1.jpeg",image)
print(arr)
print(arr2)
cv2.imshow('Contours', image)
# cv2.waitKey(0)
cv2.destroyAllWindows()

# arr2 = [15, 172, 325, 487, 649, 803, 963]
cap = cv2.VideoCapture(input_video)
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(5)
frame_count = 0

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, frame1 = cap.read()
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = []
framet = []
if not os.path.exists(f"split"):
    os.makedirs(f"split")
for i in range(len(arr2)-1):
    out.append(0)
    out.append(0)

for i in range(len(arr2)-1):
    upper = arr2[i]
    lower = arr2[i+1]
    out[i] = cv2.VideoWriter(f"split\\output{i+1}.avi", fourcc, fps,
                             (frame1.shape[1], lower-upper))


while cap.isOpened():
    ret, frame = cap.read()
    # image = cv2.resize(frame1, (frame1.shape[1], frame1.shape[0]))
    # (x, y, w, h) = cv2.boundingRect(c)
    # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    try:
        for i in range(len(arr2)-1):
            upper = arr2[i]
            lower = arr2[i+1]
            try:
                framet = frame[upper:lower, 0:frame_width]
            except Exception:
                raise Exception('End')
            out[i].write(framet)
            cv2.imshow("feed", framet)
    except Exception:
        break
    # frame1 = frame2
    # print('FPS {:.1f}'.format(1 / (time.time() - stime)))

    if cv2.waitKey(40) == 27:
        break
    frame_count += 1
    print(f"{round((frame_count/total_frame)*100, 2)}% (1/2)")

cv2.destroyAllWindows()
cap.release()
for i in range(len(arr2)-1):
    out[i].release()


