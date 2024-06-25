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
