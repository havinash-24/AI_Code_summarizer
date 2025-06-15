
# 🧠 GenAI Code Documentation Assistant

A full-stack Generative AI system that automatically generates clean, human-readable documentation for source code using LLM-based multi-agent architecture. The project features a modular Python backend and a React frontend for seamless interaction.

---

## 📌 Features

- 🔍 **Multi-Agent Architecture** – Modular agents for parsing, transforming, and documenting code
- ✨ **AI-Powered Doc Generation** – Uses LLMs (OpenAI GPT) to create intelligent docstrings
- ⚙️ **Preprocessing Pipeline** – Cleans, extracts, and formats code for AI ingestion
- ✅ **Doc Quality Validation** – Automatic review of documentation quality
- 🖥️ **Frontend Interface** – Upload, view, and interact with generated documentation

---

## 🏗️ Tech Stack

### Backend (Python):
- Flask or FastAPI (for API endpoints)
- OpenAI API
- Modular agents (Parser, Transformer, Quality Check)
- JSON for structured data flow

### Frontend (React):
- React.js
- RESTful API integration
- CSS Modules / Plain CSS

---

## 📁 Folder Structure

```
GenAI_Proj/
├── backend/
│   ├── app.py
│   ├── main.py
│   ├── agents/
│   ├── utils/
│   ├── processed_code_doc_pairs.json
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── README.md
└── gen ai proj report.pdf
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # Add your OpenAI key in .env
python main.py
```

### 3. Setup Frontend

```bash
cd ../frontend
npm install
npm start
```

---

## 🧪 How It Works

1. Upload code via frontend
2. Backend agents:
   - Parse and clean the code
   - Generate docstrings with GPT
   - Review quality
3. Frontend displays the final output

---

## 📚 Use Cases

- Auto-documentation for legacy codebases
- Educational tools for code understanding
- Onboarding junior developers
- Internal API documentation

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR with suggestions, bug fixes, or improvements.

---

## 📄 License

MIT License

---

## ✍️ Author

Built with ❤️ by Havinash
