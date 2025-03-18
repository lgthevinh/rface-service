import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from rface.RFace import RFace
import cv2

rface = RFace()

if __name__ == "__main__":
  rface.data_path = "./data/"
  rface.init()
  rface.face_reg.set_model("Dlib")
  rface.face_reg.set_threshold(0.06)
  
  # Test: check if the embedding is extracted correctly from image path
  # output_1 = rface.face_reg.extract_embeddings("./assets/obama1.jpg")
  # print(output_1[0])
  # print(type(output_1[0]))
  
  # Test: check if the embedding is extracted correctly from image array (np.ndarray)
  img = cv2.imread("./assets/obama2.jpg")
  # output_2 = rface.face_reg.extract_embeddings(img)
  # print(output_2[0])
  
  img_2 = cv2.imread("./assets/img1.jpg")
  # output_3 = rface.face_reg.extract_embeddings(img_2)
  # print(output_3[0])
  
  # Test: check if the embeddings are compared correctly (2 case scenarios)
  # print(rface.face_reg.compare_embeddings(output_1[0]["embedding"], output_2[0]["embedding"]))
  
  # print(rface.face_reg.compare_embeddings(output_2[0]["embedding"], output_3[0]["embedding"]))
  
  # Test: get all embeddings from the database
  # obama_embedding = rface.db.get_all_embedding()["Barrack Obama"].tolist()
  # print(obama_embedding)
  
  # Test: compare db stored embedding with the target embedding
  # print(rface.face_reg.compare_embeddings(obama_embedding, output_1[0]["embedding"]))
  
  # Test: store embedding in the database (Test done)
  rface.register_face(img, "Barrack Obama 1")
  rface.register_face(img, "Barrack Obama 2")
  
  # Test: recognize face from image array
  print(rface.recognize_face(img))
  print(rface.recognize_face(img_2))
  
  print(rface.get_all_faces())
  
  # Test: delete embedding from the database
  rface.delete_face("Barrack Obama 1")
  rface.delete_face("Barrack Obama 2")
  