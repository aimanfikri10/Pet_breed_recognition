import os
import streamlit as st
import google.generativeai as genai
import time
import requests
from openai import OpenAI
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize language model
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Define background image style
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #a0522d;
    opacity: 0.8;
}
</style>
"""

# Function to display the upload photo page
def upload_photo_page():
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.image("catdogg.png", width=180)

    st.title("Pet Breed Recognition and Information")

    uploaded_file = st.file_uploader("Upload an image of a dog or cat", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.subheader("Pet Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Pet Uploaded Image", use_column_width=True)
        vision_model = genai.GenerativeModel('gemini-pro-vision')

        st.subheader("Breed Information")
        
        st.subheader('Breed', divider='gray')
        response = vision_model.generate_content(["""
                                                  (If the image contains cat show cat Breed, if contains dog show dog Breed)
                                                  What Breed is this?   
                                                  'Breed Name make it bold:' The name of the identified breed. Example:-Bengal. (Do in bullet points)
                                                  else image generate "N/A"
                                                  """,image])
        with st.spinner('Wait for it...'):
             time.sleep(1)
             
        st.write(response.text)

        st.subheader('Characteristics', divider='gray')
        response = vision_model.generate_content([""" 
                                                  (If the image contains cat show cat Characteristics, if contains dog show dog Characteristics)
                                                  Characteristics: Description of the breed's physical appearance, size, coat type, and color patterns.
                                                  (Do in bullet points)
                                                  else image generate "N/A"
                                                  """,image])
        with st.spinner('Wait for it...'):
             time.sleep(1)
        st.write(response.text)

        st.subheader('Temperament', divider='gray')
        response = vision_model.generate_content([""" 
                                                  (If the image contains cat show cat Temperament, if contains dog show dog Temperament)
                                                  Temperament: Information about the typical behavior traits and personality characteristics associated with the breed.
                                                  (Do in bullet points)
                                                  else image generate "N/A"
                                                  """,image])
        with st.spinner('Wait for it...'):
             time.sleep(1)
        st.write(response.text)

        st.subheader('Care Requirements', divider='gray')
        response = vision_model.generate_content([""" 
                                                  (If the image contains cat show cat Care Requirements, if contains dog show dog Care Requirements)
                                                  Care Requirements: Guidelines on grooming, exercise needs, dietary considerations, and common health issues associated with the breed.
                                                  (Do in bullet points)
                                                  else image generate "N/A"
                                                  """,image])
        with st.spinner('Wait for it...'):
             time.sleep(1)
        st.write(response.text)

        st.balloons()

# Function to retrieve dog breeds from an API
def get_dog_breeds():
    url = "https://api.thedogapi.com/v1/breeds"
    response = requests.get(url)
    if response.ok:
        breeds = [breed['name'].lower() for breed in response.json()]
        return breeds
    else:
        return []

# Function to retrieve cat breeds from an API
def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.ok:
        breeds = [breed['name'].lower() for breed in response.json()]
        return breeds
    else:
        return []

# Function to display the breed search page
def search_breed_page():
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.title("Pet Breed Image Generator")
    st.image("catdogg.png", width = 150)
    
    st.write('<span style="color:black; font-size: 16px;">Welcome to Pet Breed Image Generator!</span> Select a pet type and enter the breed name to generate an image.', unsafe_allow_html=True)
    
    pet_type = st.selectbox("Select pet type:", ["Dog", "Cat"])
    
    if pet_type == "Dog":
        st.subheader("Enter the dog breed name:")
        animal_breeds = get_dog_breeds()  # Example list of dog breeds
    else:  # Assume "Cat" is selected
        st.subheader("Enter the cat breed name:")
        animal_breeds = get_cat_breeds()  # Example list of cat breeds
    
    breed_name = st.text_input("")
    
    if st.button("Generate Image"):
        if breed_name:
            if is_animal_breed(breed_name, animal_breeds):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"An image of a {pet_type.lower()} {breed_name}",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                st.image(image_url, caption=f"Generated Image for {pet_type} {breed_name}", use_column_width=True)
            else:
                st.error("There is no breed with this name for this pet.")
        else:
            st.warning("Please enter a breed name.")

# Function to check if the input is an animal breed
def is_animal_breed(breed_name, animal_breeds):
    # Check if the breed name exists in the list of animal breeds
    return breed_name.lower() in animal_breeds

# Main function to handle page navigation
def main():
    st.sidebar.title("Select Input Method")


    selection = st.sidebar.radio("Go to", ["Upload Photo", "Pet Breed Image Generator"])

    if selection == "Upload Photo":
        upload_photo_page()
    elif selection == "Pet Breed Image Generator":
        search_breed_page()

if __name__ == "__main__":
    main()
