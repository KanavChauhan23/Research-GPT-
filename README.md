# 🔬 ResearchGPT

<div align="center">

![ResearchGPT Banner](https://img.shields.io/badge/ResearchGPT-AI%20Powered-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-Powered Research Assistant with Multi-Agent Intelligence**

[Live Demo](#) • [Report Bug](https://github.com/KanavChauhan23/research-gpt/issues) • [Request Feature](https://github.com/KanavChauhan23/research-gpt/issues)

*Conduct comprehensive research with AI agents, vector databases, and multi-source intelligence*

</div>

---

## 🌟 Overview

**ResearchGPT** is an advanced AI research assistant that leverages LangChain agents, vector databases, and multi-source intelligence to conduct comprehensive research on any topic. It combines web search, knowledge base retrieval, and AI synthesis to generate professional research reports with citations.

### Why ResearchGPT?

- 🤖 **AI Agents** - LangChain agents orchestrate complex research workflows
- 🌐 **Multi-Source** - Searches web + internal knowledge base
- 🧠 **RAG Architecture** - Retrieval Augmented Generation for accurate results
- 💾 **Vector Database** - ChromaDB stores and retrieves research efficiently
- 📊 **Comprehensive Reports** - Professional reports with citations
- 🔄 **Continuous Learning** - Each research adds to knowledge base
- ⚡ **Fast & Accurate** - Powered by Groq's lightning-fast inference

---

## ✨ Features

### 🔍 Advanced Research Capabilities

**Multi-Agent System**
- LangChain agents orchestrate research workflow
- Autonomous tool selection and execution
- Multi-step reasoning and planning

**Intelligent Search**
- Web search via DuckDuckGo (no API key needed!)
- Vector database semantic search
- Combines multiple information sources
- Citation tracking

**RAG (Retrieval Augmented Generation)**
- Stores research in vector database
- Retrieves relevant information for future queries
- Context-aware responses
- Knowledge accumulation over time

### 📊 Professional Outputs

**Comprehensive Reports**
- Executive summary
- Detailed findings
- Analysis and insights
- Source citations
- Conclusions and recommendations

**Export & History**
- Download reports as TXT
- Research history tracking
- Timestamp tracking
- Easy organization

### 🎨 User Experience

**Intuitive Interface**
- Clean, professional design
- Real-time progress tracking
- Multiple research depths (Quick/Standard/Deep)
- Sample queries for inspiration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Query                         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│            LangChain Agent (Orchestrator)            │
│  ┌──────────────────────────────────────────────┐  │
│  │  • Analyzes query                            │  │
│  │  • Plans research strategy                   │  │
│  │  • Selects appropriate tools                 │  │
│  │  • Coordinates multi-step research           │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
┌─────────────────┐   ┌─────────────────┐
│   Web Search    │   │  Vector Store   │
│      Tool       │   │      Tool       │
│                 │   │                 │
│ • DuckDuckGo    │   │ • ChromaDB      │
│ • Real-time     │   │ • Semantic      │
│ • Current info  │   │   search        │
│                 │   │ • Past research │
└────────┬────────┘   └────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  Information Synthesis │
         │  ┌──────────────────┐ │
         │  │ Groq (Llama 3.3) │ │
         │  │ - Analyzes       │ │
         │  │ - Synthesizes    │ │
         │  │ - Generates      │ │
         │  └──────────────────┘ │
         └──────────┬─────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  Report Generation    │
         │  • Executive Summary  │
         │  • Key Findings       │
         │  • Analysis           │
         │  • Citations          │
         │  • Conclusions        │
         └──────────┬─────────────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
┌──────────────────┐  ┌───────────────┐
│  Display to User │  │ Save to Vector│
│                  │  │   Database    │
│  • View report   │  │               │
│  • Download      │  │ • Future use  │
│  • Save history  │  │ • Knowledge   │
│                  │  │   retention   │
└──────────────────┘  └───────────────┘
```

---

## 🚀 Live Demo

**Try it now:** [YOUR-STREAMLIT-URL-HERE](#)

### Example Queries

- "What are the latest developments in quantum computing?"
- "Compare renewable energy sources and their efficiency"
- "Explain the impact of AI on healthcare in 2024-2025"
- "What are the most promising cancer treatment breakthroughs?"

---

## 🛠️ Tech Stack

### Core Technologies

**AI & LLM**
- [LangChain](https://langchain.com/) - Agent framework and orchestration
- [Groq](https://groq.com/) - Lightning-fast LLM inference (Llama 3.3 70B)
- [Sentence Transformers](https://www.sbert.net/) - Embeddings generation

**Vector Database**
- [ChromaDB](https://www.trychroma.com/) - Vector storage and retrieval
- Semantic search capabilities
- Persistent storage

**Search & Retrieval**
- DuckDuckGo Search - Free web search (no API key!)
- RAG (Retrieval Augmented Generation)
- Multi-source information gathering

**Framework**
- [Streamlit](https://streamlit.io/) - Web interface
- Python 3.9+ - Backend logic

### Key Libraries

```python
langchain              # Agent framework
langchain-groq         # Groq integration
langchain-community    # Community tools
chromadb              # Vector database
sentence-transformers  # Embeddings
duckduckgo-search     # Web search
```

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Groq API key ([Get free key](https://console.groq.com/))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/KanavChauhan23/research-gpt.git
   cd research-gpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Streamlit secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   ```
   Navigate to http://localhost:8501
   ```

---

## 📁 Project Structure

```
research-gpt/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
│
├── .streamlit/
│   └── secrets.toml      # API keys (local only)
│
├── chroma_db/            # Vector database storage (auto-created)
│   └── ...               # ChromaDB files
│
└── .gitignore            # Git ignore rules
```

---

## 🎯 Use Cases

### For Students
- **Academic Research** - Gather information for essays and papers
- **Topic Exploration** - Understand complex topics quickly
- **Exam Preparation** - Quick summaries and explanations
- **Project Research** - Comprehensive background research

### For Professionals
- **Market Research** - Industry trends and insights
- **Competitive Analysis** - Compare products and services
- **Technical Research** - Latest developments in technology
- **Decision Support** - Informed decision-making

### For Content Creators
- **Content Research** - Background for articles and videos
- **Fact-Checking** - Verify information quickly
- **Trend Analysis** - What's hot in your niche
- **Deep Dives** - Comprehensive topic exploration

---

## 🔑 Key Technical Features

### LangChain Agents

**What makes this advanced:**
- **Autonomous Decision Making** - Agent decides which tools to use
- **Multi-Step Reasoning** - Plans and executes complex research workflows
- **Tool Orchestration** - Combines multiple tools intelligently
- **Memory Management** - Maintains context across interactions

### RAG (Retrieval Augmented Generation)

**How it works:**
1. **Document Chunking** - Splits research into semantic chunks
2. **Embedding Generation** - Creates vector representations
3. **Vector Storage** - Stores in ChromaDB
4. **Semantic Retrieval** - Finds relevant information
5. **Context Injection** - Adds to LLM prompt
6. **Enhanced Generation** - More accurate, cited responses

### Vector Database

**ChromaDB Benefits:**
- **Fast Similarity Search** - Sub-second retrieval
- **Persistent Storage** - Keeps knowledge between sessions
- **Scalable** - Handles thousands of documents
- **No External Service** - Runs locally, no signup needed

---

## 🔬 How It Works

### Research Workflow

1. **Query Analysis**
   - Agent analyzes the research query
   - Determines research strategy
   - Plans tool usage

2. **Multi-Source Search**
   - Searches web for current information
   - Queries vector database for past research
   - Combines findings from both sources

3. **Information Synthesis**
   - LLM analyzes all findings
   - Identifies key themes and insights
   - Resolves conflicts between sources

4. **Report Generation**
   - Creates structured report
   - Includes citations and sources
   - Provides analysis and conclusions

5. **Knowledge Storage**
   - Chunks and embeds the report
   - Stores in vector database
   - Available for future queries

---

## 📊 Comparison with Traditional Research

| Feature | Traditional | ResearchGPT |
|---------|------------|-------------|
| **Speed** | Hours/Days | Minutes |
| **Sources** | Manual search | Automated multi-source |
| **Synthesis** | Manual | AI-powered |
| **Citations** | Manual tracking | Automatic |
| **Knowledge Retention** | Notes/files | Vector database |
| **Updates** | Manual | Automatic with new research |
| **Accessibility** | Scattered notes | Centralized, searchable |

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- PDF/DOCX document upload for research
- Multi-language support
- Advanced citation formats (APA, MLA, Chicago)
- Export to PDF/DOCX
- Research topic comparison
- Collaborative research features
- Custom search sources (arXiv, Google Scholar)

---

## 📝 Roadmap

- [x] Core LangChain agent functionality
- [x] Web search integration
- [x] Vector database storage
- [x] Report generation
- [x] Research history
- [ ] Document upload (PDF/DOCX)
- [ ] Export to PDF/DOCX
- [ ] Multi-query research
- [ ] Research topic comparison
- [ ] Custom knowledge bases
- [ ] API access
- [ ] Mobile app

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kanav Chauhan**

- GitHub: [@KanavChauhan23](https://github.com/KanavChauhan23)
- LinkedIn: [Kanav Chauhan](https://linkedin.com/in/kanavchauhan23)
- Portfolio: [Your Portfolio URL]

---

## 🙏 Acknowledgments

- **LangChain** for the amazing agent framework
- **Groq** for lightning-fast LLM inference
- **ChromaDB** for vector database capabilities
- **Streamlit** for the beautiful UI framework
- The open-source AI community

---

## 💡 Technical Highlights for Recruiters

### Advanced Concepts Demonstrated

**✅ LangChain Agents**
- Multi-agent orchestration
- Tool selection and execution
- Memory management
- Chain composition

**✅ RAG (Retrieval Augmented Generation)**
- Vector embeddings
- Semantic search
- Context injection
- Knowledge management

**✅ Vector Databases**
- ChromaDB integration
- Similarity search
- Persistent storage
- Scalable architecture

**✅ Production-Ready Features**
- Error handling
- Progress tracking
- Session management
- Export functionality

### Why This Project Stands Out

1. **Real-World Application** - Solves actual research needs
2. **Advanced Architecture** - RAG + Agents + Vector DB
3. **Scalable Design** - Can handle large knowledge bases
4. **Modern Stack** - Latest AI/ML technologies
5. **Production Quality** - Not a tutorial project

---

<div align="center">

**Made with ❤️ by Kanav Chauhan**

If you found this helpful, please give it a ⭐!

[⬆ Back to Top](#-researchgpt)

</div>
