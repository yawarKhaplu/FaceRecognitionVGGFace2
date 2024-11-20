from deepface import DeepFace
import os
import pickle
def genrate_embendings():
  db_path = "Images"
  embedding_file_path = "Images/face_embeddings.pkl"
  embeddings_dict = {}
  for person_folder in os.listdir(db_path):
    person_folder_path = os.path.join(db_path, person_folder)
    if not os.path.isdir(person_folder_path):
          continue
    person_embeddings = []

  # Loop through all images in the person's folder
    for img_file in os.listdir(person_folder_path):
      img_path = os.path.join(person_folder_path, img_file)
      # Extract embeddings for each image
      try:
        f_embeddings = DeepFace.represent(img_path=img_path, model_name="ArcFace", enforce_detection=False)
        embeddings = f_embeddings[0]['embedding']
        person_embeddings.append(embeddings)
      except Exception as e:
        print(f"Error processing {img_path}: {e}")
      # Store the list of embeddings for this person
      embeddings_dict[person_folder] = person_embeddings
  with open(embedding_file_path, 'wb') as f:
      pickle.dump(embeddings_dict, f)

  print("Embeddings saved successfully.")

genrate_embendings()