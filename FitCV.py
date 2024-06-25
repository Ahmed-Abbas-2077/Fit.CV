import cv2
import numpy as np
import time
import PoseDetectorModule as pm


cap = cv2.VideoCapture(0)  # 0 for webcam
detector = pm.PoseDetector()  # Create an object of the PoseDetector class

# resized the window 1280x720
cap.set(3, 1280)


count = 0  # Counter for the number of curls
dir = 0  # Direction of the curl
pTime = 0  # Previous time

while True:
    success, img = cap.read()  # Read a frame
    img = detector.findPose(img)
    lmList = detector.findPosition(img, False)
    # print(lmList)

    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, lmList[12], lmList[14], lmList[16])

        # Left Arm
        # angle = detector.findAngle(img, lmList[11], lmList[13], lmList[15])

        # Interpolate the angle to a percentage
        per = np.interp(angle, (210, 310), (0, 100))

        # Interpolate the angle to a bar
        bar = np.interp(angle, (220, 310), (650, 100))

        # print(angle, per)

        # Check for the dumbbell curls
        color = (255, 0, 255)  # Default color
        if per == 100:  # If the arm is at 100% curl, that means the arm is straight
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:  # If the arm is at 0% curl, that means the arm is straight
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (350, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    # Calculate and display the frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
