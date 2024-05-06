import cv2
import json
from time import sleep, time
import playsound
import datetime
import easygui

def get_formatted_time():
    # Get current time
    now = datetime.datetime.now()

    # Format the time
    formatted_time = now.strftime("%m/%d/%Y | %I:%M %p")
    return formatted_time

def welcome(name, code):
    with open("logs.txt", "a") as f:
        f.write(f"{get_formatted_time()} | ALLOWED | {name} | CODE: {code}\n")
    playsound.playsound("allow.wav", block=False)

def denied(code):
    with open("logs.txt", "a") as f:
        f.write(f"{get_formatted_time()} | DENIED | ATTEMPTED CODE: {code}\n")
    playsound.playsound("deny.wav", block=False)

def scan_qr_code_from_camera(data_dict):
    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    # Initialize the QR Code detector
    qr_detector = cv2.QRCodeDetector()

    # To keep the last valid QR code data for persistent display
    last_valid_data = None
    qr_code_processed_time = None
    processing_hold_time = 5.0  # Time in seconds to hold after processing a valid QR code

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                continue  # Skip the rest of the loop if frame capture failed

            # Mirror the frame
            frame = cv2.flip(frame, 1)


            # Ready message
            frame[:70] = (255, 255, 255)  # Backing
            text_size = cv2.getTextSize("Ready to scan", cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = 50
            cv2.putText(frame, "Ready to scan", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            # Decode QR codes
            retval, decoded_info, decoded_idx, points = qr_detector.detectAndDecodeMulti(frame)

            current_time = time()
            # Check if we are within the hold time after processing a QR code
            if last_valid_data and (current_time - qr_code_processed_time < processing_hold_time):
                continue  # Skip processing new QR codes

            if points is not None and len(points) == 1:
                current_data = decoded_info[0]
                if current_data != last_valid_data:
                    last_valid_data = current_data  # Update the last seen valid QR data
                    qr_code_processed_time = current_time  # Update the time when this QR code was processed

                    if last_valid_data in data_dict:
                        message = f"WELCOME: {data_dict[last_valid_data]}"
                        frame[:] = (0, 255, 0)  # Green background
                        welcome(data_dict[last_valid_data], last_valid_data)  # Call the welcome function
                    elif last_valid_data == "000-000-000-000":
                        message = "CLEARING CACHE..."
                        playsound.playsound("reset.mp3", False)
                        frame[:] = (255, 100, 50)  # Green background
                    else:
                        message = "DENIED"
                        frame[:] = (0, 0, 255)  # Red background
                        denied(last_valid_data)  # Call the denied function

                    # Display the scan message in black text
                    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
                    text_x = (frame.shape[1] - text_size[0]) // 2
                    text_y = (frame.shape[0] + text_size[1]) // 2
                    cv2.putText(frame, message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

            # Display the resulting frame
            cv2.imshow('ID Scanner', frame)

            # Exit the loop with 'q' key
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            # elif key == ord('r'):
            #     last_valid_data = "" # allows a re-scan
            #     easygui.msgbox('Scanner reset. All IDs can now be scanned again.')

            #     playsound.playsound("reset.mp3")


    finally:
        # When everything done, release the capture and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

# Load the dictionary to look up QR code data
with open("identities.json", "r") as f:
    data_dict = json.load(f)

# Start the camera and QR code detection with dictionary data
scan_qr_code_from_camera(data_dict)