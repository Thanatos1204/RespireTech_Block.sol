from flask import Flask, Response
from flask_cors import CORS
import cv2
import mediapipe as mp
import math
import time
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speed of speech
engine.setProperty('volume', 0.9)

def text_to_speech(text):
    # Convert text to speech
    engine.say(text)
    time.time()
    engine.runAndWait()

app = Flask(__name__)
CORS(app)

@app.route('/video_feed', endpoint='video_feed_endpoint')
def video_feed():
    def generate_frames():
        prev_thumb_angle = None  # Initialize prev_thumb_angle outside the loop
        prev_index_angle = None  # Initialize prev_index_angle outside the loop
        prev_thumb_x, prev_thumb_y = 0, 0  # Initialize previous thumb coordinates
        last_click_time = time.time()  # Initialize last click time
        click_count = 0  # Initialize click count
        thumb_click_count = 0  # Initialize thumb click count
        index_click_count = 0  # Initialize index click count
        click_delay = 1  # Delay between clicks
        shake_count = 0

        # Initialize MediaPipe hand solution
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        mp_face = mp.solutions.face_mesh
        face_mesh = mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        # Start capturing video from the webcam
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # Flip the frame horizontally for a natural viewing experience
            frame = cv2.flip(frame, 1)

            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe
            results = pose.process(rgb_frame)
            hand_results = hands.process(rgb_frame)
            face_results = face_mesh.process(rgb_frame)

            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Example: Analyze neck and torso inclination
                neck = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                # Calculate the angle between the neck and the shoulders
                neck_to_left_shoulder = math.hypot(neck.x - left_shoulder.x, neck.y - left_shoulder.y)
                neck_to_right_shoulder = math.hypot(neck.x - right_shoulder.x, neck.y - right_shoulder.y)
                average_neck_to_shoulder = (neck_to_left_shoulder + neck_to_right_shoulder) / 2

                # Define a threshold for good posture
                good_posture_threshold = 0.4  # Example value, adjust based on your criteria

                if average_neck_to_shoulder > good_posture_threshold:
                    # Poor posture detected
                    text_to_speech('Poor Posture Detected')
                    # Draw the text at the top right corner
                    cv2.putText(frame, 'Poor Posture ', (frame.shape[1] - 160, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                else:
                    # Good posture detected
                    # Draw the text at the top right corner
                    cv2.putText(frame, 'Good Posture', (frame.shape[1] - 160, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 255, 0), 2)

            # Draw facial landmarks
            if face_results.multi_face_landmarks:
                for face_landmark in face_results.multi_face_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, face_landmark, mp_face.FACEMESH_CONTOURS)
                    nose_landmark = face_landmark.landmark[1]  # Nose tip landmark
                    nose_x, nose_y = int(nose_landmark.x * frame.shape[1]), int(nose_landmark.y * frame.shape[0])

            vertical_shake_detected = False
            horizontal_shake_detected = False

            if hand_results.multi_hand_landmarks:
                for hand_landmark in hand_results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

                    # Get landmarks for thumb and index finger
                    thumb_tip = hand_landmark.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumb_mcp = hand_landmark.landmark[mp_hands.HandLandmark.THUMB_MCP]
                    index_tip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_mcp = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    index_pip = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

                    thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
                    index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

                    # Angle calculation for the pen
                    pen_dx = index_x - thumb_x
                    pen_dy = index_y - thumb_y
                    angle_rad = math.atan2(pen_dy, pen_dx)
                    angle_deg = math.degrees(angle_rad)
                    angle_with_vertical = 90 - angle_deg

                    # Calculate the distance between the nose and the thumb
                    nose_thumb_distance = math.hypot(thumb_x - nose_x, thumb_y - nose_y) * 0.1

                    # Calculate the angle at the index finger's MCP joint
                    angle_rad_index = math.atan2(index_tip.y - index_mcp.y, index_tip.x - index_mcp.x) - \
                                      math.atan2(index_pip.y - index_mcp.y, index_pip.x - index_mcp.x)
                    index_angle = abs(math.degrees(angle_rad_index))

                    # Calculate the angle at the thumb's MCP joint
                    angle_rad_thumb = math.atan2(thumb_tip.y - thumb_mcp.y, thumb_tip.x - thumb_mcp.x) - \
                                      math.atan2(index_tip.y - thumb_mcp.y, index_tip.x - thumb_mcp.x)
                    thumb_angle = abs(math.degrees(angle_rad_thumb))

                    current_time = time.time()

                    # Detect a click based on the change in the thumb's angle
                    if prev_thumb_angle is not None and (current_time - last_click_time) > click_delay:
                        angle_change_thumb = abs(thumb_angle - prev_thumb_angle)
                        if angle_change_thumb > 20:  # Threshold for detecting a click based on angle change
                            click_count += 1
                            thumb_click_count += 1
                            last_click_time = current_time

                    prev_thumb_angle = thumb_angle

                    # Detect a click based on the change in the index finger's angle
                    if prev_index_angle is not None and (current_time - last_click_time) > click_delay:
                        angle_change_index = abs(index_angle - prev_index_angle)
                        if angle_change_index > 20:  # Threshold for detecting a click based on angle change
                            click_count += 1
                            index_click_count += 1
                            last_click_time = current_time

                    prev_index_angle = index_angle

                    # Shaking detection
                    if prev_thumb_x != 0 and prev_thumb_y != 0:
                        vertical_change = abs(thumb_y - prev_thumb_y)
                        horizontal_change = abs(thumb_x - prev_thumb_x)
                        vertical_shake_detected = vertical_change > 20  # Example threshold
                        horizontal_shake_detected = horizontal_change > 20

                    prev_thumb_x, prev_thumb_y = thumb_x, thumb_y

                    # Display the information on the frame
                    cv2.putText(frame, 'Distance: {:.2f}'.format(nose_thumb_distance), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, 'Pen Angle: {:.2f}'.format(angle_with_vertical), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, 'Total Clicks: {}'.format(click_count), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, 'Thumb Clicks: {}'.format(thumb_click_count), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, 'Index Clicks: {}'.format(index_click_count), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                    if vertical_shake_detected:
                        #   text_to_speech('Vertical Shake Detected')
                        shake_count+=1
                        cv2.putText(frame, 'Vertical Shake Detected', (frame.shape[1] - 300, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                    
                    if horizontal_shake_detected:
                        #  text_to_speech('Horizontal Shake Detected')
                        shake_count+=1
                        cv2.putText(frame, 'Horizontal Shake Detected', (frame.shape[1] - 300, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                       
                    if -30 > angle_with_vertical or angle_with_vertical > 30:
                        # Angle not within acceptable range, display text
                        cv2.putText(frame, 'Hold at Correct Angle', (frame.shape[1] - 300, 120),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                       # text_to_speech('Hold at Correct Angle')
                    cv2.putText(frame, 'Shake Count: {}'.format(shake_count), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                    # Encode the frame to JPEG format
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
