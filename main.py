# Import the necessary libraries
import cv2
import numpy as np

# Open the video file
cap = cv2.VideoCapture('video.mp4')

# Set some variables
count_line_position = 550
min_width_react = 80
min_height_react = 80


def center_handle(x, y, w, h):
    """
    his function calculates and returns the center coordinates (cx, cy) of a bounding rectangle given its top-left coordinates (x, y) and its width and height (w, h)
    """
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1 
    cy = y+y1 
    return cx, cy

detect = []    # An empty list to store the center coordinates of detected objects.
offset = 6     # Allowed error between the center of a detected object and the count line
counter = 0    # Keeps track of the number of vehicles counted.

# Check if cemera is opened
if not cap.isOpened():
    print("Error opening video file")

# Get the default screen resolution
# screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# cv2.resizeWindow('My Video', screen_width, screen_height)

# cv2.namedWindow("My Video", cv2.WINDOW_NORMAL)

#  Create a background subtractor object to detect moving objects in the video.
algo = cv2.createBackgroundSubtractorMOG2() 

while True:
    # read video
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 5)
    # applying on each frame
    img_sub = algo.apply(blur)

    # Perform morphological operations to enhance the detected objects
    dilt = cv2.dilate(img_sub, np.ones((5,5)) )
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    dilatada = cv2.morphologyEx(dilt, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    # Find contours in the dilated image
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    # Draw a line on the frame to mark the count line
    cv2.line(frame, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)


    # Iterate over the detected contours and filter out objects that are too small
    for (i, c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (h>=min_height_react)
        if not validate_counter:
            continue

        # Draw a bounding rectangle around each valid object
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

        # Display the vehicle count above each detected object
        cv2.putText(frame, "VEHICLE:"+str(counter), (x, y-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,0,244), 2)

        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame, center, 4, (0,0,255), -1)

        for (x, y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
                cv2.line(frame, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
                detect.remove((x, y))
                print("Vehicle Counter:" + str(counter))
        
    # Display the vehicle count on the frame
    cv2.putText(frame, "VEHICLE COUNTER :"+str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            


    if ret:

        # cv2.imshow("My Video", dilatada)  #in backend process
        cv2.imshow("My Video", frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()
