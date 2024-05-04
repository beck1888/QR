import cv2
import json

def scan_qr_code_from_camera():
    """Scan the QR code using the camera and return the decoded data when a QR code is detected. The camera feed is mirrored."""
    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    # Initialize the QR Code detector
    qr_detector = cv2.QRCodeDetector()

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video")
                continue

            # Mirror the frame
            frame = cv2.flip(frame, 1)

            # Decode the QR code
            data, bbox, _ = qr_detector.detectAndDecode(frame)

            if bbox is not None and data:
                print(f"QR Code Detected: {data}")
                return data

            # Display the resulting frame
            cv2.imshow('Scan QR Code (Mirrored)', frame)

            # Exit the loop with 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # When everything done, release the capture and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

def lookup_data(qr_data, data_dict):
    """Look up QR code data in the provided dictionary and print the corresponding value."""
    if qr_data in data_dict:
        print(f"Value corresponding to '{qr_data}': {data_dict[qr_data]}")
    else:
        print(f"No data found for '{qr_data}'.")

# Dictionary to look up QR code data and match to a person
with open("identities.json", "r") as f:
    data_dict = json.load(f)

# Scan the QR code using the camera
qr_data = scan_qr_code_from_camera()

# If QR code data is found, look it up in the dictionary
if qr_data:
    lookup_data(qr_data, data_dict)
else:
    print("No QR code detected.")