from google.cloud import vision
from googletrans import Translator
from PIL import Image
import io
import os
import streamlit as st

# Set the environment variable to authenticate using the uploaded JSON credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "D:/Sanjay job/Projects/finial OCR solution/Sanjay Ocr.json"
# Initialize Google Cloud Vision API client
client = vision.ImageAnnotatorClient()

# Function to detect text using Google Vision API
def detect_text(image_path):
    """Detects text in an image using Google Vision API."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Convert image content to an image object
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Check if text was detected and return it
    if texts:
        detected_text = texts[0].description
        return detected_text
    else:
        return "No text detected."

def translate_text(text):
    """Translates text to multiple languages using Google Translate."""
    translator = Translator()
    
    languages = ['ta', 'en', 'kn', 'te', 'hi']  # Tamil, English, Kannada, Telugu, Hindi
    translated_texts = {}

    for lang in languages:
        # Auto-detect source language
        translated_texts[lang] = translator.translate(text, dest=lang).text

    return translated_texts


# Streamlit App GUI
st.title("Handwritten Text Recognition and Translation")

# Image upload option
image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Camera input option
camera_image = st.camera_input("Capture Image")

# If either an image is uploaded or captured via camera, process the image
if image_file is not None or camera_image is not None:
    # Use the uploaded or captured image
    if image_file is not None:
        # Display the uploaded image
        st.image(image_file, caption="Uploaded Image", use_container_width=True)

        # Save the uploaded image temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(image_file.getbuffer())

    else:
        # Display the captured camera image
        st.image(camera_image, caption="Captured Image", use_container_width=True)

        # Save the captured image temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(camera_image.getbuffer())

    # Detect text from image
    detected_text = detect_text("temp_image.jpg")
    st.subheader("Detected Text:")
    st.write(detected_text)

    if detected_text != "No text detected.":
        # Translate the detected text to multiple languages
        translations = translate_text(detected_text)

        # Display translated text
        st.subheader("Translations:")
        for lang, translation in translations.items():
            st.write(f"{lang.upper()}: {translation}")

else:
    st.info("Please upload an image or use the camera to capture one to proceed.")
