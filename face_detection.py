import cv2  # Import the OpenCV library for computer vision tasks
import logging  # Import the logging library for logging messages

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceDetector:
    """Initialize the FaceDetector with the specified Haar cascade path."""
    def __init__(self, haar_cascade_path):
        # Load the Haar cascade classifier for face detection
        self.haar_cascade = cv2.CascadeClassifier(haar_cascade_path)
        if self.haar_cascade.empty():
            logging.error("Failed to load Haar cascade classifier. Check the provided path.")
            raise ValueError("Haar cascade classifier not loaded. Please check the path.")
        
    """Capture video from the specified camera index and detect faces."""
    # Note for webcam users: camera_index must be set to 1 (camera_index=1)
    def capture_video(self, camera_index=0):
        
        # Open a connection to the webcam or video file
        video_capture = cv2.VideoCapture(camera_index)

        # Check if the video capture was successful
        if not video_capture.isOpened():
            logging.error("Could not open video device.")
            return

        logging.info("Face Detection started...")

        # Start an infinite loop to continuously capture frames
        while True:
            # Capture a single frame from the video
            is_frame_captured, frame = video_capture.read()
            if not is_frame_captured:
                logging.warning("Failed to capture video frame.")
                break
            
            # Convert the captured frame to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the grayscale frame
            detected_faces = self.haar_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

            # Draw rectangles around detected faces
            for (x, y, width, height) in detected_faces:
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 1)

            # Display the frame with detected faces in a window
            cv2.imshow('Face Detection (ESC to Exit)', frame)

            # Exit the loop if the ESC key is pressed
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                logging.info("Exiting Face Detection.")
                break

        # Release the video capture object and close all OpenCV windows
        video_capture.release()
        cv2.destroyAllWindows()
        logging.info("Face Detection closed.")

"""Main function to run the face detection application."""
def run_face_detection_app():
    # Path to the Haar cascade classifier for frontal face detection
    haar_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    try:
        # Create an instance of the FaceDetector class
        face_detector = FaceDetector(haar_cascade_path)
        # Start capturing video and detecting faces
        face_detector.capture_video(camera_index=0)  # Change camera_index if needed
    except Exception as error:
        logging.error(f"An error occurred: {error}")

if __name__ == "__main__":
    # Note for webcam users: Ensure your webcam is connected and accessible.
    run_face_detection_app()  # Call the main function to run the application
    