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
