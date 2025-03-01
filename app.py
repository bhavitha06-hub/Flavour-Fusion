import streamlit as st
import google.generativeai as genai
import random
import base64
import os

# Configure API key
api_key = "AIzaSyALNYu5js8raZ5ccF_W2MDdqPNq0frAoGs"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def get_joke():
    jokes = [
        "Why did the bicycle fall over? Because it was two-tired.",
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "I'm friends with 25 letters of the alphabet—I don't know Y.",
        "Why did the math book look sad? Because it had too many problems.",
        "Why don't eggs tell jokes? They might crack up!",
    ]
    return random.choice(jokes)

def generate_recipe(topic, word_count):
    try:
        st.write("👩‍🍳 Whipping up something delicious for you...")        
        st.write(f"🤖 Stirring up your recipe blog! Enjoy this bite-sized joke: \n\n {get_joke()}")

        chat_session = genai.GenerativeModel("gemini-1.5-flash").start_chat()

        prompt = f"Write a recipe blog on '{topic}' with {word_count} words."
        response = chat_session.send_message(prompt)

        st.success("✅ Your recipe is ready!")
        return response.text
    except Exception as e:
        st.error(f"Error generating blog: {e}")
        return None

def get_base64_image(image_path):
    """Encode the image file to base64."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def main():
    # Path to the local image
    image_path = r"D:/my_project/project_files/flavour_fusion/kitchen_background.jpg"

    # Check if the image exists
    if not os.path.exists(image_path):
        st.error(f"Image file not found: {image_path}")
    else:
        # Encode the image to base64
        encoded_image = get_base64_image(image_path)

        # Custom CSS for the background and text color
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            body, p, h1, h2, h3, h4, h5, h6, label, .stButton>button {{
                color: white !important;
            }}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
                color: black !important;
                background-color: rgba(255, 255, 255, 0.8) !important;
                border: 1px solid #ccc !important;
                border-radius: 5px !important;
                padding: 10px !important;
            }}
            .stButton>button {{
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                border-radius: 5px !important;
                cursor: pointer !important;
            }}
            .stButton>button:hover {{
                background-color: #45a049 !important;
            }}
            .stDownloadButton>button {{
                background-color: #4CAF50 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                border-radius: 5px !important;
                cursor: pointer !important;
            }}
            .stDownloadButton>button:hover {{
                background-color: #45a049 !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Set the title and subheading with white text color
    st.markdown("<h1 style='color: white;'>Flavour Fusion: AI-Driven Recipe Blogging 🤖</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white;'>Generate AI-powered recipe blogs with ease!</h3>", unsafe_allow_html=True)

    # Input fields
    topic = st.text_input("Enter your recipe topic:", placeholder="e.g., Vegan Chocolate Cake")
    word_count = st.number_input("Word count:", min_value=100, max_value=2000, step=100)

    # Generate recipe button
    if st.button("Generate Recipe"):
        if topic and word_count:
            recipe = generate_recipe(topic, word_count)
            if recipe:
                st.text_area("Generated Recipe:", recipe, height=300)
                st.download_button(
                    label="Download Recipe",
                    data=recipe,
                    file_name=f"{topic}.txt",
                    mime="text/plain",
                    key="download_recipe"
                )
        else:
            st.warning("Please enter a topic and word count.")

if __name__ == "__main__":
    main()