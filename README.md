# 🧪 R&D Task Dashboard – Resume Builder LLM App

Welcome to the **Research & Development** coordination space for the `resume_builder_llm_app`. This document tracks all major technical modules, task ownership, progress, and R&D planning involved in building a robust, LLM-powered resume generation system.

---

## 📌 Core Modules & Assignments

| 🔧 Task Title | 👤 Assigned To | 📄 Description |
|--------------|----------------|----------------|
| **Resume Upload & Parsing** | Arun Raj, Gomathi | Build resume upload component. Parse PDFs via pdfplumber or OCR and extract key fields (email, phone, links, etc.). |
| **LinkedIn Profile URL Parser / Description Extractor** | Vinothini, Nilofer Mubeen | Fetch public LinkedIn profile data from a URL or PDF export and extract fields like Name, Summary, Skills, Education, Experience using LLM/web scraping. |
| **AI Resume Template Agent** | Amit Arjun Verma | Build a prompt-based agent that dynamically generates LaTeX or CSS code for resume templates based on user preferences and style requirements. |
| **LLM Prompt Builder Module** | _(Not yet assigned)_ | Build a centralized engine to generate dynamic prompts for resume generation, parsing, feedback, and formatting (LaTeX/CSS). |
| **Feedback Generator** | Nehlath Harmain, Subhash | Compare resume content with JD, identify gaps or mismatches, and generate GPT-powered constructive feedback without exaggeration. |

---

## 📂 Folder Contents

---

## 🧠 R&D Goals

- Break the project into logical, modular units
- Assign owners for fast, parallel development
- Track status and progress transparently
- Ensure integration across all LLM + parsing + templating components

---

## 🛠 Tech Stack Reference

| Module | Suggested Tools / Tech |
|--------|-------------------------|
| Resume Parsing | `pdfplumber`, `PyMuPDF`, `pdf2docx`, `re`, `tiktoken` |
| LinkedIn Parser | `Selenium`, `BeautifulSoup`, `OpenAI GPT`, `json` |
| Prompt Builder | `langchain`, `yaml`, `jinja2`, `OpenAI API`, `promptlayer` |
| Template Agent | `python-docx`, `jinja2`, `LaTeX`, `CSS`, `WeasyPrint` |
| Feedback Gen | `OpenAI`, `cosine_similarity`, `embeddings`, `GPT-4o` |

---

## 🧭 Team Workflow

1. Each team member works on their assigned module in a dedicated branch.
2. Code should be modular and reusable inside the `src/` directory.
3. Push updates regularly and raise Pull Requests.
4. Communicate blockers/updates on Slack or internal group.
5. Weekly sync call to review progress.

---

## ✅ Task Status Tracker (from Google Sheet)

| Task | Status |
|------|--------|
| Resume Upload & Parsing | Not started |
| LinkedIn Profile Parsing | Not started |
| Resume Template Agent | Not started |
| Prompt Builder | Not started |
| Feedback Generator | Not started |

_Update live status here once each task progresses._

---

## 🔗 Task Sheet Link

Live team sheet with owner, status, and priority:  
👉 [Open in Google Sheets](https://docs.google.com/spreadsheets/d/1KY6Vx0TY-qJGzmI6qb90sHmC0VDJMtfJizTKjRzWyMM/edit?usp=sharing)

---

## 🤝 Contribution Guidelines

- Stick to assigned tasks unless re-discussed.
- Maintain clean, readable, and testable code.
- Create isolated modules that follow the project’s folder structure.
- Add minimal unit tests inside the `tests/` folder where applicable.

---

## 📣 Notes

- Ping Subhash if GitHub or LLM integration help is needed.
- Suggestions and improvements to R&D flow are welcome!

Let’s build a resume builder that stands out 💪🚀
