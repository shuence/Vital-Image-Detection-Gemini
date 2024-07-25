import streamlit as st
from pathlib import Path
import google.generativeai as genai
import pyttsx3

st.set_page_config(page_title="Currency Detection", page_icon=":robot:")
st.image(r"image.png", width=150)

# Configure your API key
try:
    from api_keys import api_key
    genai.configure(api_key=api_key)
except ImportError:
    st.error("API key file not found. Please ensure you have 'api_key.py' with a valid 'api_key' variable.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring API key: {e}")
    st.stop()

# Generation configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 632,
    "max_output_tokens": 4096,
}  

# Safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
       "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE" 
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
### Currency Note Analysis
I'll analyze the uploaded image and provide insights on the currency note.
Indian Notes
Also give all four points in the following languages like english marathi hindi gujarati kannada
Also identify if note is counterfeit or not
and give output :- 
1. if Original give original or if fake give fake
2. If original Then amount with serial number
"""

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Error initializing GenerativeModel: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload the currency note image for analysis", type=["png", "jpg", "jpeg"])
submit_button = st.button("Generate the Analysis")

if submit_button:
    if uploaded_file is not None:
        try:
            image_data = uploaded_file.getvalue()
            
            # Making our image ready
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": image_data
                },
            ]
            
            # Making our prompt ready
            prompt_parts = [
                image_parts[0],
                system_prompt,
            ]
            
            # Generate response based on prompt and image
            try:
                response = model.generate_content(prompt_parts)
                analysis_text = response.text
                st.write(analysis_text)
                
                # Convert text to speech
                engine = pyttsx3.init()
                engine.say(analysis_text)
                engine.runAndWait()
            except Exception as e:
                st.error(f"Unexpected error: {e}")
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")
    else:
        st.error("Please upload a file before submitting.")
