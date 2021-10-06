import cv2
import numpy as np
from tracker import *


def findBot(roi, s):
    findBot.counter += 1  # counting number of function calls
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)

        if area > 100:
            cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)

            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    # 2. Object Tracking

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        # cv2.putText(roi_1, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        return (s + str(findBot.counter))

    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)


findBot.counter = 0

#######################################################################

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("bot2.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

# Robot 1
while True:
    c = 0
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
    #roi_turn1 = frame[510: 550, 675: 720]  # OK
    roi_turn2 = frame[550: 595, 720: 760]  # OK
    #roi_turn3 = frame[550: 595, 760: 805]  # OK
    #roi_turn4 = frame[510: 550, 800: 845]  # OK

    #roi_s1 = frame[180:220, 685:730]
    # cv2.imshow("roi_s1",roi_s1)
    roi_s2 = frame[175:215, 725:765]
    # cv2.imshow("roi_s2", roi_s2)
    #roi_s3 = frame[180:220, 765:810]
    # cv2.imshow("roi_s3", roi_s3)
    #roi_s4 = frame[180:220, 805:850]
    # cv2.imshow("roi_s4",roi_s4)

    #roi_d1 = frame[510:550, 375:420]
    roi_d2 = frame[550:595, 375:420]
    #roi_d3 = frame[550:595, 1105:1150]
    #roi_d4 = frame[510:550, 1105:1150]

    # rois=[roi_turn1, roi_turn2, roi_turn3, roi_turn4]

    o1 = (findBot(roi_s2, "SS"))
    if o1:
         print(o1)
        # fcallnum = int(o1[2:])
        # if fcallnum < 1000:
        #     print("Start")
        # else:
        #     print("Stop")

    o2 = findBot(roi_turn2, "LR")
    if o2:
         print(o2)
        # fcallnum = int(o2[2:])
        # if fcallnum < 1200:
        #     print("Right")
        # else:
        #     print("Left")

    o3 = findBot(roi_d2, "DR")
    if o3:
        print("Drop and Reverse")

    # findBot(roi_s2)
    # findBot(roi_turn2)
    # findBot(roi_d2)

    # findBot(roi_s3)
    # findBot(roi_turn3)
    # findBot(roi_d3)

    # findBot(roi_s4)
    # findBot(roi_turn3)
    # findBot(roi_d4)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()