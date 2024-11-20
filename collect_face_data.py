import cv2
import time
from deepface import DeepFace
def collect_face_from_cam(name):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)


    if not cap.isOpened():
        print("Error Opening Video..")

    ptime = time.time()


    i = 1
    image_count = 0

    position = (50, 50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (225, 255, 255)  # Black text (BGR)
    bg_color = (0, 0, 0) # white
    thickness = 2
    line_type = cv2.LINE_AA  # Anti-aliased line type for smooth text edges
    padding = 10


    last_capture_time = time.time()
    skip_interval = 5

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
            print(f"Error: {e}")
            
            # Show message on the frame when no face is detected
            (text_width, text_height), baseline = cv2.getTextSize("Please Bring Your Face", font, font_scale, thickness)
            cv2.rectangle(frame, 
                  (position[0] - padding, position[1] - text_height - padding),  # Top-left corner
                  (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                  bg_color, 
                  cv2.FILLED)
            cv2.putText(frame, "Please Bring Your Face", position, font, font_scale, color, thickness, line_type)
            
            (text_width, text_height), baseline = cv2.getTextSize("Please Bring Your Face", font, font_scale, thickness)
            cv2.rectangle(frame, 
                  (position[0] - padding, position[1] - text_height+80 - padding),  # Top-left corner
                  (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                  bg_color, 
                  cv2.FILLED)
            cv2.putText(frame, "In front of Camera", (50, 90), font, font_scale, color, thickness, line_type)
            # cv2.putText(frame, "Please Bring Your Face ", position, font, font_scale, color, thickness, cv2.LINE_AA)
            # cv2.putText(frame, "In front of Camera", (50, 90), font, font_scale, color, thickness, line_type)

            cv2.imshow("LiveDetect", frame)
            if cv2.waitKey(1) == ord('q'):
                break
            continue  # Skip the rest of the loop and move to the next frame if there is no face

        # If face_objs is empty, handle accordingly
        if len(face_objs) > 1:
            print("Multiple faces are there ")
            continue
        elif face_objs:
            j = 0
            for face in face_objs:
                facial_area = face['facial_area']  # Extract bounding box as a dictionary
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
                cv2.rectangle(frame, (x-5, y-5), (x + w+10, y + h+10), (0, 255, 0), 2)  # Draw rectangle around face
                cropped_face = frame[y:y+h, x:x+w]
                
                print("img: ", image_count)
                if j == 1:
                    print("Multiple Faces Found Skipping this frame... ")
                    break
                
                elif cropped_face.size > 0:
                    img_name = f"{name}/face_{image_count}.jpg"
                    # When to save img

                    # Display some instructions while collecting facez

                    if image_count <= 4:
                        text = "Please Bring Your Front Face"
                    elif image_count <= 8:
                        text = "Turn Left Side"
                    elif image_count <=12:
                        text = "Turn Right side"
                    elif image_count <= 16:
                        text = "Please Close Your Eyes"
                    elif image_count <= 20:
                        text = "Open Your Mouth"
                    else:
                        text = "Please Smile"

                    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                    cv2.rectangle(frame, 
                    (position[0] - padding, position[1] - text_height - padding),  # Top-left corner
                    (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                    bg_color, 
                    cv2.FILLED)
                    cv2.putText(frame, text, position, font, font_scale, color, thickness, line_type)
                
                    (text_width, text_height), baseline = cv2.getTextSize("In front of Camera", font, font_scale, thickness)
                    cv2.rectangle(frame, 
                    (position[0] - padding, position[1] - text_height+90 - padding),  # Top-left corner
                    (position[0] + text_width + padding, position[1] + baseline + padding),  # Bottom-right corner
                    bg_color, 
                    cv2.FILLED)
                    cv2.putText(frame, "In front of Camera", (50, 90), font, font_scale, color, thickness, line_type)
                    current_time = time.time()
                    if current_time - last_capture_time >= skip_interval:
                        cv2.imwrite(img_name, cropped_face)
                        # print(f"{img_name} saved.")
                        image_count+=1
                        skip_interval+=1
                    continue  # Skip the rest of the loop and move to the next frame
                break





            print(f"{j+1} faces found in {time.time() - stime:.2f}s")

        else:
            print("No face found")

        # Show the video frame with/without rectangle
        cv2.imshow("LiveDetect", frame)
        cv2.setWindowProperty("LiveDetect", cv2.WND_PROP_TOPMOST, 1)

        if image_count > 25:
            print("Img Captured...")
            break

        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True



# collect_face_from_cam("Images/Yawar")