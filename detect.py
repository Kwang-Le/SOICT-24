from ultralytics import YOLO
from PIL import Image, ImageDraw
import cv2
from pytesseract import pytesseract
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
import time
import requests
import re
# from boilerpy3 import extractors
# from underthesea import lang_detect
import Levenshtein

# keyword list
keyword_list = ["accept", "decline", "cookies", "privacy"]
threshold_score = 0.2

model = YOLO("model_epoch_64.pt")

def detect_banner(image_string):
  # Load the image
  image = cv2.imread(image_string)
  # image = decode_base64_to_opencv(image_string)

  results = model(image, save=True)

  # print(results)
  top_score = 0
  result_detection = {}
  result_width = 0
  result_height = 0
  result_text = None
  # Loop through each detection
  for result in results:
    # Get bounding box coordinates (x1, y1, x2, y2)
    x1, y1, x2, y2 = result.boxes.xyxy[0]
    print(x1.item(), y1, x2, y2)
    x,y,w,h = result.boxes.xywh[0]
    print("Width of Box: {}, Height of Box: {}".format(w, h))

    # Extract the detected object region from the image
    detected_object = image[int(y1.item()) : int(y2.item()), int(x1.item()): int(x2.item())]

    # Convert the image to a format compatible with Pytesseract (RGB)
    rgb_image = cv2.cvtColor(detected_object, cv2.COLOR_BGR2RGB)
    # Convert from OpenCV image to PIL format for Pytesseract
    pil_image = Image.fromarray(rgb_image)

    # Perform OCR using Pytesseract
    target_text = pytesseract.image_to_string(pil_image)
    print(f"Detected Text: {target_text}")

    # Check for keyword presence (modify based on your needs)
    keyword_found = any(keyword in target_text.lower() for keyword in keyword_list)  # Case-insensitive search

    print(result.boxes.conf.item())
    score = result.boxes.conf.item()
    # Update detection score if keyword found
    if keyword_found:
      score += threshold_score  # Increase score based on threshold

    if score >= top_score:
      top_score = score
      result_detection = detected_object
      result_width = w
      result_height = h
      result_text = target_text

  if result_detection.any() and top_score > 0.2:
    # Create a window to display the detected object
    cv2.imshow('Detected Object', result_detection)
    # matching_element = get_bounding_boxes("https://misa.vn/", result_text, result_width, result_height)
    # print("real value: ", matching_element.rect)
    # print("id: ", matching_element.get_attribute("id"))
    # Wait for a key press to close the window
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optionally, save the detected object image
    # cv2.imwrite('detected_object.jpg', detected_object)
    return True
  else:
    return False

  print("Finished processing image!")

def decode_base64_to_opencv(image_data):
  """Decodes a base64 encoded image string and returns a cv2 Image object.

  Args:
    image_string: The base64 encoded image data.

  Returns:
    A cv2 Image object or None if decoding fails.
  """
  try:
    # Load the image using PIL (RGB format by default)
    pil_image = Image.open(image_data)

    # Convert PIL image to cv2 format (BGR)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)

    return opencv_image
  except Exception as e:
    print(f"Error decoding image: {e}")
    return None

def is_within_tolerance(box_width, box_height,target_width, target_height, rel_tol=10000, abs_tol=0.0):
    # target_width = 409
    # target_height = 344
    target_area = target_width * target_height
    box_area = box_width * box_height
    return abs(box_area - target_area) <= rel_tol

def is_matching_text(text_target, text_box):
    distance = Levenshtein.distance(text_target, text_box)
    similarity = 1 - (distance / max(len(text_target), len(text_box)))
    print("Similarity:", similarity)
    if similarity > 0.7:
      return True
    else:
      return False

def get_bounding_boxes(url, target_text, target_width, target_height):
    driver = webdriver.Chrome(ChromeDriverManager().install())  # Replace with your preferred webdriver
    driver.get(url)
    time.sleep(1)
    elements = driver.find_elements(By.XPATH, "//*")
    banner = driver.find_element(By.ID, "onetrust-banner-sdk")
    print("expected value: ", banner.rect)
    bounding_boxes = []
    texts = []
    matching_element = None
    for element in elements:
        rect = element.rect
        text = element.text
        if is_within_tolerance(rect['width'], rect['height'], target_width, target_height) and is_matching_text(target_text, text):
          matching_element = element
          print(matching_element.rect)
          break
        # if "cookie" in text:
        #   texts.append(text)
        #   bounding_boxes.append(rect)

    # driver.close()
    # driver.quit() #cause crash
    return matching_element


detect_banner("/home/quangle2/Desktop/paper/cookiebannerdetection/images/gucci.png")
# url = "https://stackoverflow.com/"
# get_bounding_boxes(url, text_target)