from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai


# Configure the Google Gemini Pro API with the API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get the response from Google Gemini Pro
def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to set up the PDF input and convert it to image
def input_pdf_setup(uploaded_file):
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        # Get the first page of the PDF
        first_page = images[0]

        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Prepare the image in base64 format for API consumption
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    except Exception as e:
        st.write(f"Error processing PDF: {e}")
        return []

# Streamlit App
st.set_page_config(page_title='Panel Niyukti: AI-Powered Expert Matching System for Interview Boards')
st.header("Panel Niyukti")

# Text input for expert description
input_text = st.text_area("Expert Description: ", key="input")

# File uploader for resume/CV
upload_file = st.file_uploader("Upload Resume / CV of Expert (PDF)...", type=["pdf"])

# Notify if the file is successfully uploaded
if upload_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for different prompts
submit1 = st.button("Tell About Expert")
submit2 = st.button("What are the keywords that are Missing")
submit3 = st.button("Relevance Score")

# Prompt 1: Tell About Expert
input_prompt1 = """
Provide a detailed profile of the subject matter expert 
whose domain matches with the interview board subject. 
Explain their qualifications, areas of expertise, 
and how they are relevant to assessing the candidates.
"""

# Prompt 2: What are the keywords that are Missing
input_prompt2 = """
Identify the key skills, topics, or subject areas that 
are missing from the candidate's profile that are relevant 
for evaluating expertise for the interview board. 
Explain why these keywords are essential and how they 
relate to the interview subject.
"""

# Prompt 3: Relevance Score
input_prompt3 = """
Analyze the profile of the subject expert and the candidate's 
expertise. Calculate a relevance score that determines the 
suitability of this expert for the interview board based on 
their matching qualifications and expertise areas.
"""

# Handle responses based on the selected prompt
if submit1 or submit2 or submit3:
    if upload_file is not None:
        pdf_content = input_pdf_setup(upload_file)
        if pdf_content:
            if submit1:
                response = get_gemini_response(input_prompt1, pdf_content, input_text)
            elif submit2:
                response = get_gemini_response(input_prompt2, pdf_content, input_text)
            elif submit3:
                response = get_gemini_response(input_prompt3, pdf_content, input_text)
            
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Failed to process PDF")
    else:
        st.write("Please upload the resume / CV")
