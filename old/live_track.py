import cv2
import json

def scan_qr_code_from_camera(data_dict):
    """Scan the QR code using the camera, display a blue border around it, and show the value from the dictionary above the QR code if found."""
    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    # Initialize the QR Code detector
    qr_detector = cv2.QRCodeDetector()

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                continue  # Skip the rest of the loop if frame capture failed

            # Mirror the frame
            frame = cv2.flip(frame, 1)

            # Decode the QR code
            data, bbox, _ = qr_detector.detectAndDecode(frame)

            # Check if there is a bounding box and data
            if bbox is not None and data:
                # Draw a rectangle around the QR code with a blue border
                points = bbox[0].astype(int)
                cv2.polylines(frame, [points], True, (255, 0, 0), 2)

                # Look up the data in the dictionary
                dictionary_value = data_dict.get(data, "Data not found")

                # Calculate the position for the dictionary value display above the QR code
                top_left = points.min(axis=0)
                bottom_right = points.max(axis=0)
                text_position = (top_left[0], max(0, top_left[1] - 20))

                # Calculate text size for the background rectangle
                (text_width, text_height), _ = cv2.getTextSize(dictionary_value, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (text_position[0], text_position[1] - text_height - 5), 
                              (text_position[0] + text_width, text_position[1]), (255, 0, 0), -1)

                # Display the dictionary value in white above the QR code
                cv2.putText(frame, dictionary_value, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Display the resulting frame
            cv2.imshow('Scan QR Code (Mirrored)', frame)

            # Exit the loop with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # When everything done, release the capture and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

# Load the dictionary to look up QR code data
with open("identities.json", "r") as f:
    data_dict = json.load(f)

# Start the camera and QR code detection with dictionary data
scan_qr_code_from_camera(data_dict)
