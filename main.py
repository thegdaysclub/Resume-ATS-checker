import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import requests
import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase and remove special characters
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

# Function to extract skills from text
def extract_skills(text):
    # Expand this list or use NLP for more robust extraction
    skills = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'cloud computing']
    return [skill for skill in skills if skill in text.lower()]

# Function to interact with Ollama API
def get_ollama_response(prompt, url, model):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get('response', "No response from model")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to extract text from a PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to calculate cosine similarity
def calculate_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]

# Function to clean and parse Ollama response
def clean_ollama_response(response):
    try:
        # Extract the JSON-like content
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if not match:
            return None

        json_like = match.group(0)
        
        # Add quotes to keys
        json_like = re.sub(r'(\w+):', r'"\1":', json_like)
        
        # Fix escaped double quotes and other characters
        json_like = json_like.replace('\\"', '"')
        
        # Remove unnecessary backslashes
        json_like = json_like.replace("\\", "")
        
        # Ensure proper JSON formatting
        json_like = re.sub(r',\s*}', '}', json_like)  # Remove trailing commas
        json_like = re.sub(r',\s*]', ']', json_like)  # Remove trailing commas in lists

        # Validate and clean up JSON structure
        try:
            # Attempt to load the cleaned JSON string
            json_obj = json.loads(json_like)
            return json.dumps(json_obj, indent=4)  # Pretty-print for easier reading
        except json.JSONDecodeError as e:
            st.error(f"JSONDecodeError: {e}")
            return None

    except Exception as e:
        st.error(f"Error in cleaning response: {e}")
        return None


# Prompt template
input_prompt = """
Act as an experienced ATS (Application Tracking System) for the tech field. Evaluate the resume based on the given job description. Consider the following aspects:

1. Skills match
2. Experience level
3. Education relevance
4. Project relevance
5. Overall suitability for the role

Resume: {text}
Job Description: {jd}

Provide a detailed analysis and the response in the following JSON format:
{{
    "JD Match": "percentage",
    "MissingKeywords": ["keyword1", "keyword2"],
    "SkillsAnalysis": "detailed analysis of skills match",
    "ExperienceAnalysis": "analysis of candidate's experience",
    "EducationAnalysis": "analysis of candidate's education",
    "ProjectAnalysis": "analysis of relevant projects",
    "OverallSuitability": "overall suitability assessment",
    "ImprovementSuggestions": ["suggestion1", "suggestion2"]
}}
"""

## Streamlit app
st.set_page_config(page_title="Smart ATS for Resumes", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            #background-color: #020304;
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            padding: 2rem;
        }
        .header {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }
        .subheader {
            font-size: 1.5rem;
            color: #555;
        }
        .error {
            color: #e74c3c;
            font-weight: bold;
        }
        .success {
            color: #2ecc71;
            font-weight: bold;
        }
        .result {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
        }
        /* Remove extra padding from the text area */
        .stTextArea {
            margin: 0;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("This sophisticated ATS project uses Local LLMs (with ollama) and streamlit to provide comprehensive resume analysis.")
    
    st.markdown("""
    - [Streamlit](https://streamlit.io/)
    - [Ollama](https://ollama.ai/)
    """)
    
    add_vertical_space(5)
    st.write("Made with ❤ by Prakash K.")
    st.write("Connect with me on [Github](https://github.com/prakash888kp/prakash888kp)")

# Add custom URL and model inputs to the sidebar
st.sidebar.header("Ollama Settings")
custom_url = st.sidebar.text_input("Ollama API URL", value="http://localhost:11434/api/generate")
custom_model = st.sidebar.text_input("Ollama Model", value="llama2")


# Main Content
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description", height=200)
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit", key="submit_button", use_container_width=True)

# In the Streamlit app, handle the cleaned response
if submit:
    if uploaded_file is not None and jd.strip():
        with st.spinner("Analyzing your resume..."):
            resume_text = input_pdf_text(uploaded_file)
            if "Error:" not in resume_text:
                processed_resume = preprocess_text(resume_text)
                processed_jd = preprocess_text(jd)
                
                initial_similarity = calculate_similarity(processed_resume, processed_jd)
                resume_skills = extract_skills(processed_resume)
                jd_skills = extract_skills(processed_jd)
                
                prompt = input_prompt.format(text=processed_resume, jd=processed_jd)
                response = get_ollama_response(prompt, custom_url, custom_model)
                                
                st.markdown("<div class='result'>", unsafe_allow_html=True)
                st.subheader("Raw AI Response")
                st.text(response)  # Display the raw response for debugging
                cleaned_response = clean_ollama_response(response)
                
                if cleaned_response:
                    try:
                        response_json = json.loads(cleaned_response)
                        final_score = (float(response_json.get('JD Match', 0).strip('%')) + (initial_similarity * 100)) / 2
                        
                        st.subheader("Analysis Results")
                        st.write(f"JD Match: {final_score:.2f}%")
                        st.write("Skills Found:", ", ".join(resume_skills))
                        st.write("Missing Skills:", ", ".join(set(jd_skills) - set(resume_skills)))
                        st.write("AI Analysis:")
                        st.json(response_json)
                    
                    except json.JSONDecodeError as e:
                        st.error(f"Error: Unable to parse the cleaned response as JSON. Error: {str(e)}")
                        st.write("Cleaned response:")
                        st.code(cleaned_response)
                else:
                    st.error("Unable to extract JSON-like content from the Ollama response. Please check the API output format.")
                    st.write("Fallback Analysis:")
                    st.write(f"Similarity Score: {initial_similarity * 100:.2f}%")
                    st.write("Skills Found:", ", ".join(resume_skills))
                    st.write("Missing Skills:", ", ".join(set(jd_skills) - set(resume_skills)))
            else:
                st.error("Please upload a resume and paste the job description.")
                
        st.markdown("<div class='result'>", unsafe_allow_html=True)
        st.write("Fallback Analysis:")
        st.write(f"Similarity Score: {initial_similarity * 100:.2f}%")
        st.write("Skills Found:", ", ".join(resume_skills))
        st.write("Missing Skills:", ", ".join(set(jd_skills) - set(resume_skills)))

st.markdown("</div>", unsafe_allow_html=True)  # Close the main content div
