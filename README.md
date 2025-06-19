# 🧠 PromptStudio

**PromptStudio** is a personal sandbox project that allows users to create, customize, and test their own prompt templates and model settings. Users can sign in using Google authentication and manage prompt configurations like edit, load, or delete prompts stored in MongoDB.

It features a built-in chatbot interface where users can interact with custom prompts in real time. PromptStudio also supports document uploads, which are converted into embeddings and stored in ChromaDB to enable context-aware Q&A. The entire system is powered by a FastAPI backend for fast, secure, and modular operations.

---

## 🚀 Features

- 🧩 Prompt templating with variable injection
- 🔁 Chat-based interface for real-time prompt testing
- 🔧 Adjustable model parameters (model, temperature, top_p, context toggle)
- 💬 Prompt history management (edit/load/delete)
- 📎 File upload and document embedding (for RAG)
- 🔐 Google OAuth2 login with JWT-based authentication
- 📊 Streamlit UI with modular navigation
- ⚙️ FastAPI backend with clean architecture
- 🧠 LangChain support for LLM orchestration and tracing

---

## 📁 Folder Structure

```bash
PromptStudio/
├── app/                  # Streamlit frontend (UI)
│   ├── main.py
│   ├── login.py
│   ├── dashboard.py
│   └── sidebar.py
├── src/                  # FastAPI backend logic
│   ├── main.py
│   ├── database/         # DB connections and models
│   ├── models/           # Pydantic schemas
│   ├── routes/           # API routes (auth, prompt, chat)
│   ├── services/         # Core logic (chains, handlers)
│   └── utils/            # Helpers and constants
├── .env.examples         # Environment variable template
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
└── README.md             # This file

```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/andreimiranda0121/PromptStudio.git
cd PromptStudio
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy .env.examples and rename it to .env, then update it with your API keys and configuration values.


## How to run the app?

### 1. Start FastAPI backend

```bash
python -m src.main # or you can use py -m src.main
```

### 2. Start Streamlit frontend

```bash
cd app
streamlit run main.py
```

## 📦 Tech Stack

Frontend: Streamlit

Backend: FastAPI

AI: LangChain + OpenAI API + Gemini API

Auth: Google OAuth2 + JWT

Database: MongoDB and ChromaDB

## 🔮 Future Enhancements

- Prompt performance analytics and logging  
- Prompt set import/export  
- Prompt similarity or clustering features  
- User usage tracking  
- RAG-based document QA enhancements  
- Automatic deletion of RAG documents linked to removed prompt settings  
- Automatic reloading of associated RAG context when loading prompt settings  

## ✨ Contributors

- [Andrei Miranda](https://github.com/andreimiranda0121)