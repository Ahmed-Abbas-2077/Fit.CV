import cv2
import mediapipe as mp
import time


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
