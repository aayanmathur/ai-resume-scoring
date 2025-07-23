import pdfplumber
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Groq API Key from .env
groq_api_key = os.getenv("GROQ_API_KEY")

# LangChain Groq Chat setup
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Function to extract text from PDF using pdfplumber
def extract_resume_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# Function to parse resume using LangChain + Groq
def parse_resume_text_with_langchain(text):
    prompt = f"""
From the following resume text, extract:
- Full Name
- Phone Number
- Email Address
- LinkedIn Profile URL
- GitHub Profile URL
- Skills
- Work Experience (job title, company, duration, description)
- Achievements
- Summary or professional summary
- Education
- Certifications
- Projects (title, description, tools, duration)

Omit missing fields.

Format the result in clean JSON like:
{{
  "name": "",
  "phone": "",
  "email": "",
  "location": "",
  "linkedin": "",
  "github": "",
  "skills": [],
  "experience": [],
  "achievements": [],
  "summary": "",
  "education": [],
  "certifications": [],
  "projects": []
}}

Resume Text:
{text}


*Deliverables*:
- Return the parsed resume fields in JSON format as specified above.
- DO NOT include any additional text or explanations, just the JSON output.
"""

    messages = [
        SystemMessage(content="You are a professional resume parser."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content

# Main function to handle resume parsing
def main(pdf_path):     
       
    # Extract text from the PDF resume
    resume_text = extract_resume_text(pdf_path)
    
    parsed_resume = parse_resume_text_with_langchain(resume_text)
    
    return parsed_resume

print(main("data/ARUNRAJ_Business Analyst.pdf"))