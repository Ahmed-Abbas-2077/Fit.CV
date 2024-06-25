import cv2
import mediapipe as mp
import time
import math


class PoseDetector:
    def __init__(self, mode=False, complexity=1, smoothLm=True, seg=True, smoothSeg=True, detectionCon=0.5, trackCon=0.5):
        """
            mode: In static images, set this to False. In videos, set this to True.
            complexity: The complexity of the pose model: 0, 1, or 2. 0 is the fastest, and 2 is the most accurate.
            smoothLm: Smooth the landmark points to reduce jitter.
            seg: Segment the body into parts.
            smoothSeg: Smooth the segmented parts.
            detectionCon: Minimum confidence value ([0.0, 1.0]) for the detection to be considered successful.
            trackCon: Minimum confidence value ([0.0, 1.0]) for the tracking to be considered successful.
        """
        self.mode = mode
        self.complexity = complexity
        self.smoothLm = smoothLm
        self.seg = seg
        self.smoothSeg = smoothSeg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize the MediaPipe Pose model
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smoothLm,
                                     self.seg, self.smoothSeg, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        """
            Args:
                img: The image to process.
                draw: Whether to draw the pose landmarks on the image.

            Returns:
                img: The image with or without the pose landmarks drawn on it.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        """ 
            Args:
                img: The image to process.
                draw: Whether to draw the pose landmarks on the image.

            Returns:
                lmList: A list of the landmark points.
        """
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = p1[1], p1[2]
        x2, y2 = p2[1], p2[2]
        x3, y3 = p3[1], p3[2]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) -
                             math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360

        # Draw the angle on the image
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2-50, y2+50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


def main():
    # Open the video file
    cap = cv2.VideoCapture(0)

    # Check if the video file opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    # Get the width and height of the video frames
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the aspect ratio of the video
    aspect_ratio = frame_width / frame_height

    # Set a target width for display (e.g., 1000 pixels)
    target_width = 1000
    # Calculate target height based on the aspect ratio
    target_height = int(target_width / aspect_ratio)

    # Create a named window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    # Resize the window to the size of the video frames
    cv2.resizeWindow('Video', target_width, target_height)

    pTime = 0  # Previous time
    detector = PoseDetector()  # Initialize the PoseDetector class

    # Process the video frames
    while True:
        success, img = cap.read()  # Read a frame
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        # Track elbows
        # if len(lmList) != 0:
        #     print(lmList[14], lmList[13])
        #     cv2.circle(img, (lmList[14][1], lmList[14]
        #                [2]), 15, (0, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (lmList[13][1], lmList[13]
        #                [2]), 15, (0, 0, 255), cv2.FILLED)

        # Caclulate the angle between the shoulders, elbows, and wrists
        if len(lmList) != 0:
            angle1 = detector.findAngle(
                img, lmList[11], lmList[13], lmList[15])
            print(angle1)

            angle2 = detector.findAngle(
                img, lmList[12], lmList[14], lmList[16])
            print(angle2)

        # Calculate and display the frame rate
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        # Display the frame rate on the video frame
        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Display the video frame with pose landmarks
        cv2.imshow('Video', img)

        # Press 'q' to exit the video display
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
