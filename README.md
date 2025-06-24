# 🧪 R&D Task Management - Resume Builder LLM App

This folder contains all the core Research & Development (R&D) tasks and documentation related to building and scaling the `resume_builder_llm_app` project.

---

## 🔍 Purpose

To clearly define, assign, and track team responsibilities for various core modules in the project — from resume parsing to feedback generation — using a modular and LLM-powered architecture.

---

## 🧩 Core Task Assignments

| Task Title                        | Assigned To                     | Description                                                                                     |
|----------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| **Resume Upload & Parsing**      | Arun Raj, Gomathi               | Build Streamlit uploader, extract info from PDF/DOCX using OCR, PyMuPDF, docx, etc.            |
| **LinkedIn Profile Parser**      | Vinothini, Nilofer Mubeen       | Extract profile data from URL or PDF using LLMs and scraping tools                              |
| **AI Resume Template Agent**     | Amit Arjun Verma                | Use prompt engineering to generate LaTeX/DOCX templates based on user role                     |
| **LLM Prompt Builder Module**    | _To be assigned_                | Create a reusable prompt builder for all LLM calls (resume generation, feedback, etc.)         |
| **Feedback Generator**           | Nehlath Harmain, Subhash        | Compare resume with job description and suggest improvements using GPT                         |

> Full task board maintained here:  
> 🔗 [R&D Task Sheet (Google Sheets)](https://docs.google.com/spreadsheets/d/1KY6Vx0TY-qJGzmI6qb9OsHmCOVIDJMtFJiZTkRJzWyMM/edit)

---

## 🛠️ Tech Stack Per Module

| Module                 | Tools / Libraries Used                                                                 |
|------------------------|----------------------------------------------------------------------------------------|
| Resume Parsing         | `PyMuPDF`, `pdfplumber`, `python-docx`, `re`, `json`                                  |
| LinkedIn Parser        | `BeautifulSoup`, `Selenium` *(optional)*, GPT-4, LangChain                            |
| Prompt Builder         | `yaml`, `jinja2`, `langchain`, `openai`                                               |
| Template Agent         | `jinja2`, `python-docx`, `LaTeX`, `jinja + CSS`                                       |
| Feedback Generator     | `openai`, `sentence-transformers`, `cosine_similarity`, `langchain.embeddings_utils` |

---

## 🧠 Team Workflow

Each R&D member should:
1. Work on their assigned module in a separate branch
2. Push updates and raise PRs with testable code
3. Follow code documentation and naming conventions
4. Sync every week with updates/status

---

## 📂 Folder Content
