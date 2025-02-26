import cv2
import numpy as np

# Function to calculate distance
def calculate_distance(focal_length, real_object_width, object_width_in_image):
    """
    Calculate the distance of an object based on the known focal length,
    real object width, and object width in the image.

    Args:
    - focal_length: Focal length of the camera (in pixels)
    - real_object_width: Real-world width of the object (in cm or meters)
    - object_width_in_image: Width of the object in the image (in pixels)

    Returns:
    - Distance to the object (in same units as real_object_width)
    """
    # Use the formula for distance calculation
    distance = (real_object_width * focal_length) / object_width_in_image
    return distance

# Initialize the camera (use the default camera, or use an index if you have multiple cameras)
cap = cv2.VideoCapture(0)

# Focal length of the camera (in pixels) - You'll need to calibrate your camera to get this value.
# If you don't have a specific value, you may try approximating based on the field of view of your camera.
focal_length = 650  # Approximate value, this depends on your camera.

# Real-world size of the object (in cm or meters) - This should be the width of the object you're measuring.
real_object_width = 20  # For example, assume the object width is 20 cm.

print("Press 'q' to quit the camera view.")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Show the captured frame
    cv2.imshow("Camera", frame)

    # Assume you manually detect the object using a rectangle or use a method like object detection (for simplicity)
    # For now, we're using a hard-coded bounding box (you should replace it with your own detection logic).
    # Here, we're using the coordinates of the object in the frame (for example, a red object).
    # Define the region of interest (ROI) in the image where the object is
    # You can replace this with an actual object detection algorithm (like contour detection or an object recognition model)
   
    # Example: Hard-code the bounding box coordinates of the object
    x, y, w, h = 200, 150, 50, 30  # Example bounding box (you can replace this with actual detection)
   
    # Draw the bounding box (just for visual reference)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
   
    # Calculate the object width in the image (in pixels)
    object_width_in_image = w
   
    # Calculate the distance using the object width in the image
    if object_width_in_image > 0:
        distance = calculate_distance(focal_length, real_object_width, object_width_in_image)
        cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the updated frame with the distance
    cv2.imshow("Distance Calculation", frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
