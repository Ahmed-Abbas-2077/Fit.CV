# Fit.CV 💪
Use **OpenCV** and a custom PoseDetector module to track and count dumbbell curls in real-time using your webcam. 📸

## Features ✨
- **Real-Time Pose Detection:** Utilizes a webcam to capture and process video frames in real-time.
- **Angle Calculation:** Computes the angle of the arm to determine the progress of each curl.
- **Progress Bar:** Displays a progress bar indicating the completion percentage of each curl.
- **Curl Counter:** Counts the number of completed curls.
- **Frame Rate Display:** Shows the current frame rate.

## Installation

### Clone the Repository
    git clone https://github.com/Ahmed-Abbas-2077/Fit.CV.git
    cd Fit.CV

### Install Dependencies
    pip install -r requirements.txt


## How It Works 🛠️
- **Initialize Webcam:** Starts video capture from the default webcam.
- **Pose Detection:** Uses the PoseDetector module to detect body landmarks.
- **Angle Calculation:** Computes the angle between shoulder, elbow, and wrist.
- **Progress Calculation:** Converts the angle into a percentage and a bar representation.
- **Curl Detection:** Tracks the direction and counts each complete curl.
- **Display:** Shows the progress bar, curl count, and frame rate on the video feed.
- **Quit:** Press 'q' to exit the application.

## License
This project is licensed under the **MIT** License. See the **LICENSE** file for details.

**Enjoy** tracking your workouts with real-time feedback! 🏋️‍♀️📊
