# 🤖 Multi-Agent Research System

An AI-powered **Multi-Agent Research System** built using **LangChain**, **LangGraph**, **Hugging Face**, **Tavily Search**, and **BeautifulSoup**. The system automates the complete research workflow by dividing tasks among specialized AI agents.

---

## 🚀 Features

- 🔍 **Search Agent**
  - Searches the web using Tavily Search API.
  - Finds recent and reliable information.

- 📖 **Reader Agent**
  - Extracts and cleans webpage content using BeautifulSoup.
  - Filters useful information from web pages.

- ✍️ **Writer Agent**
  - Generates a well-structured research report.
  - Includes Introduction, Key Findings, Conclusion, and Sources.

- 📝 **Critic Agent**
  - Reviews the generated report.
  - Assigns a score and suggests improvements.

- 🔄 Multi-Agent workflow powered by **LangGraph**

---

# 🏗️ System Architecture

```
                 User Query
                      │
                      ▼
              Search Agent (Tavily)
                      │
                      ▼
           Reader Agent (BeautifulSoup)
                      │
                      ▼
              Writer Agent (LLM)
                      │
                      ▼
              Critic Agent (LLM)
                      │
                      ▼
                Final Report
```

---

# 🛠️ Tech Stack

- Python
- LangChain
- LangGraph
- Hugging Face Inference API
- Tavily Search API
- BeautifulSoup4
- Requests
- python-dotenv

---

# 📂 Project Structure

```
Multi-Agent-System/
│
├── agents.py
├── pipeline.py
├── tools.py
├── app.py
├── check.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-research-system.git

cd multi-agent-research-system
```

---

### 2. Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
TAVILY_API_KEY=your_tavily_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
```

> **Note:** Never upload your `.env` file to GitHub.

---

# ▶️ Run the Project

```bash
python pipeline.py
```

or

```bash
python app.py
```

---

# 💡 Example

Input

```
What is the impact of war on the stock market?
```

Output

```
Introduction

Key Findings

• Impact on global indices

• Investor sentiment

• Commodity price fluctuations

Conclusion

Sources
```

---

# 📦 Dependencies

Major libraries used:

- LangChain
- LangGraph
- HuggingFace
- BeautifulSoup4
- Tavily
- Requests
- python-dotenv

---

# 🔮 Future Improvements

- Memory-enabled agents
- PDF report generation
- Streamlit UI
- Multi-source web search
- RAG integration
- Vector Database (FAISS / ChromaDB)
- Citation validation
- Export report as PDF

---

# 👨‍💻 Author

**Faiz Ali Chishti**

- B.Tech CSE Student
- Google Student Ambassador (2025 & 2026)
- AI & Machine Learning Enthusiast

---

## ⭐ If you found this project useful, consider giving it a star!
