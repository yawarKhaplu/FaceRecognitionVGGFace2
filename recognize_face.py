import cv2
import time
from deepface import DeepFace
import pandas as pd

def live_recongnize():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)


    if not cap.isOpened():
        print("Error Opening Video..")

    ptime = time.time()


    i = 1

    position = (50, 50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (225, 255, 255)  # Black text (BGR)
    bg_color = (0, 0, 0) # white
    thickness = 2
    line_type = cv2.LINE_AA  # Anti-aliased line type for smooth text edges
    padding = 10


    

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Video Ended in {(time.time() - ptime)/60:.2f} minutes")
            break
        
        print(f"{i} Frame Processing...")
        i += 1
        stime = time.time()

        # Perform face detection on the frame
        try:
            face_objs = DeepFace.extract_faces(
                img_path=frame,
                detector_backend='yolov8',  # Use YOLOv8 for face detection
                align=False,
                color_face='gray'
            )
        except Exception as e:
            # print(f"Error: {e}")
            
            # Show message on the frame when no face is detected
            (text_width, text_height), baseline = cv2.getTextSize("Please Bring Your Face", font, font_scale, thickness)
            cv2.rectangle(frame, 
                  (position[0] - padding, position[1] - text_height - padding),  # Top-left corner
                  (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                  bg_color, 
                  cv2.FILLED)
            cv2.putText(frame, "Please Bring Your Face", position, font, font_scale, color, thickness, line_type)
            
            (text_width, text_height), baseline = cv2.getTextSize("In front of Camera", font, font_scale, thickness)
            cv2.rectangle(frame, 
                  (position[0] - padding, position[1] - text_height+80 - padding),  # Top-left corner
                  (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                  bg_color, 
                  cv2.FILLED)
            cv2.putText(frame, "In front of Camera", (50, 90), font, font_scale, color, thickness, line_type)
            # cv2.putText(frame, "Please Bring Your Face ", position, font, font_scale, color, thickness, cv2.LINE_AA)
            # cv2.putText(frame, "In front of Camera", (50, 90), font, font_scale, color, thickness, line_type)

            cv2.imshow("LiveDetect", frame)
            cv2.setWindowProperty("LiveDetect", cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) == ord('q'):
                break
            continue  # Skip the rest of the loop and move to the next frame if there is no face

        
        if face_objs:
            j = 0
            for face in face_objs:
                facial_area = face['facial_area']  # Extract bounding box as a dictionary
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around face
                cropped_face = frame[y:y+h, x:x+w]

                result = DeepFace.find(
                    img_path=cropped_face,
                    db_path="Images",
                     detector_backend="skip",
                     model_name='Facenet512',
                     enforce_detection=False,
                     threshold=0.3
                )
                label = "?"
                color = (255, 0, 255)

                # Check if the result list is not empty when face found
                if result and isinstance(result[0], pd.DataFrame) and not result[0].empty:
                    identity = result[0].iloc[0]['identity']  # Assuming the first match is the best match
                    print("Result: ", result)
                    # print("Identity: ",identity)
                    label_m = identity.split("\\")[1]  # Extract a meaningful label (e.g., filename)
                    print("Label: ", label)
                    label = label_m.split("_")[0]  # Extract a meaningful label (e.g., filename)
                    user_color = label_m.split("_")[1]

                    color = (0, 255, 255) #Cyend defualt_color

                    color_dict = {
                        "Red": (255, 0, 0),
                        "Green": (0, 255, 0),
                        "Blue": (0, 0, 255),
                        "Yellow": (255, 255, 0),
                        "Purple": (128, 0, 128),
                        "Orange": (255, 165, 0),
                        "Pink": (255, 192, 203),
                        "Black": (0, 0, 0),
                        "White": (255, 255, 255),
                        "Gray": (128, 128, 128)
                    }

                    if user_color in color_dict:
                        color = color_dict[user_color]


                    # print("Type: ", type(label))
                    # color = (255, 255, 0)

                    # cv2.rectangle(frame, (x, y), (x+w,y+ h), color=(255, 255, 0), thickness=2)
                    # cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                # else:
                # No match found, label as unknown
                cv2.rectangle(frame, (x, y), (w+x, h+y), color=color, thickness=4)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                # print("img: ", image_count)
                



            print(f"{j+1} faces found in {time.time() - stime:.2f}s")

        else:
            print("No face found")

        # Show the video frame with/without rectangle
        cv2.imshow("LiveDetect", frame)
        cv2.setWindowProperty("LiveDetect", cv2.WND_PROP_TOPMOST, 1)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True



# live_recongnize()