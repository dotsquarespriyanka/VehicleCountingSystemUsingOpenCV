# Vehicle Counting System using OpenCV

This project is a vehicle counting system implemented using OpenCV, a popular computer vision library. The system captures video from a source (camera or video file), detects moving vehicles, and counts the number of vehicles passing a designated count line.

## Installation

To run this project, you need to have OpenCV installed. You can install it using the following command:

```bash
pip install opencv-python
```

## Usage

1. Make sure you have a video file named `video.mp4` in the same directory as the script. You can also adjust the `cap = cv2.VideoCapture('video.mp4')` line to capture video from a camera instead.

2. Run the script using the following command:


3. The script will open a window displaying the processed video. Vehicles passing the count line will be detected and counted in real-time.

4. Press the 'q' key to exit the video display.

## Features

- Detects moving vehicles using background subtraction and morphological operations.
- Draws bounding rectangles around detected vehicles.
- Displays the count of vehicles passing the designated count line.
- Provides real-time video processing and counting.

## Customization

You can customize the following parameters in the script to adjust the behavior of the system:

- `count_line_position`: The y-coordinate of the count line.
- `min_width_react` and `min_height_react`: Minimum width and height of detected objects to be considered as vehicles.
- `offset`: Allowed error between the center of a detected object and the count line.
