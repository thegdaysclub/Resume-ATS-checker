# ATS Analyzer

##URL:
https://resume-ats-checker-llm.streamlit.app/

## Description
ATS Analyzer is a sophisticated Application Tracking System (ATS) project that uses Local LLMs (with Ollama) and Streamlit to provide comprehensive resume analysis. It evaluates resumes based on given job descriptions, considering aspects such as skills match, experience level, education relevance, project relevance, and overall suitability for the role.

## Features
- Preprocesses text by converting it to lowercase and removing special characters.
- Extracts skills from text based on a predefined list.
- Interacts with the Ollama API to generate responses.
- Extracts text from a PDF file.
- Calculates cosine similarity between two texts.
- Cleans and parses Ollama responses.
- Provides a detailed analysis and response in JSON format.

## Technologies Used
- Python
- Streamlit
- Ollama

## Installation
1. Clone the repository: `git clone https://github.com/your-username/ats-analyzer.git`
2. Navigate to the project directory: `cd ats-analyzer`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up the Ollama API URL and model locally
5. Run the application: `streamlit run atsanalyzer.py` and give you OLLAMA_API_URL and model name

## Usage
1. Paste the job description in the provided text area.
2. Upload the resume in PDF format.
3. Click the "Submit" button to analyze the resume.
4. View the detailed analysis and response in the JSON format.

## Contributing
Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
