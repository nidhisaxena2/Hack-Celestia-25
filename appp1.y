import streamlit as st
import cv2
import numpy as np
import pyttsx3
import os
import time
import mediapipe as mp
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from streamlit_webrtc import webrtc_streamer

def camera_app():
    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Load YOLO model
    required_files = ['yolov4-tiny.weights', 'yolov4-tiny.cfg', 'coco.names']
    if not all(os.path.exists(file) for file in required_files):
        st.error("Required YOLO files are missing!")
        return

    net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Load facial expression dataset and train KNN
    dataset_path = "facial_expression_data_new.csv"
    data = pd.read_csv(dataset_path)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    # Initialize MediaPipe Pose and Face Mesh
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=False, max_num_faces=1)

    # Function to calculate distance
    def calculate_distance(area, K=1000):
        return K / np.sqrt(area) if area > 0 else float('inf')

    # Function to infer action
    def infer_action(landmarks):
        left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        if left_hand.y < nose.y and right_hand.y < nose.y:
            return "Hands raised"
        elif left_hand.y > nose.y and right_hand.y > nose.y:
            return "Hands lowered"
        return "Neutral position"

    # Real-time video capture
    def process_frame():
        cap = cv2.VideoCapture(0)
        last_person_detected_time = 0
        detection_interval = 10  # Detect YOLO objects every 10 seconds

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            height, width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Real-time Pose Estimation
            pose_results = pose.process(rgb_frame)
            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                action = infer_action(pose_results.pose_landmarks.landmark)
                cv2.putText(frame, f"Action: {action}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Real-time Distance Calculation
            if pose_results.pose_landmarks:
                nose = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                if nose.visibility > 0.5:
                    area = 10000  # Example fixed area
                    distance = calculate_distance(area)
                    cv2.putText(frame, f"Distance: {distance:.2f} cm", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Real-time Facial Expression Recognition
            face_results = face_mesh.process(rgb_frame)
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    landmarks = [lm.x for lm in face_landmarks.landmark] + [lm.y for lm in face_landmarks.landmark]
                    expression = knn.predict([landmarks])[0]
                    cv2.putText(frame, f"Expression: {expression}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # YOLO Object Detection every 10 seconds
            current_time = time.time()
            if current_time - last_person_detected_time > detection_interval:
                last_person_detected_time = current_time
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outputs = net.forward([net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers()])
                boxes, confidences, class_ids = [], [], []
                for output in outputs:
                    for detection in output:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype(int)
                            x, y = int(center_x - w / 2), int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                detected_objects = []
                if len(indexes) > 0:
                    for i in indexes.flatten():
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        if label == "person":
                            color = colors[class_ids[i]]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            cv2.putText(frame, f"{label}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            detected_objects.append(label)

                # Provide feedback through TTS
                if "person" in detected_objects:
                    engine.say("Person detected")
                    engine.runAndWait()

            # Show real-time output
            cv2.imshow("Real-Time Detection", frame)

            # Exit on ESC key
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    if st.button("Start Camera Stream"):
        st.write("Starting camera...")
        process_frame()

if __name__ == "__main__":
    st.set_page_config(page_title="Camera App", layout="wide")
    st.title("Real-Time Camera App")
    camera_app()
