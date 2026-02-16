# 🔬 ResearchGPT

<div align="center">

![ResearchGPT](https://img.shields.io/badge/ResearchGPT-LangChain%20+%20RAG-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.1.20-green?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-1.7.4-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Professional AI Research Assistant with LangChain, RAG & Vector Database**

[Live Demo](https://ai-researchgpt.streamlit.app/) • [Report Bug](https://github.com/KanavChauhan23/research-gpt/issues) • [Request Feature](https://github.com/KanavChauhan23/research-gpt/issues)

*Multi-Source Intelligence • RAG Architecture • Production-Ready*

</div>

---

## 🌟 Overview

**ResearchGPT** is a professional AI research assistant built with **LangChain**, **RAG (Retrieval Augmented Generation)** architecture, and **FAISS vector database**. It combines web search with accumulated knowledge to generate comprehensive, cited research reports.

### Why ResearchGPT?

- 🦜 **LangChain Framework** - Production-grade AI chains and prompt management
- 📊 **RAG Architecture** - Retrieval Augmented Generation for grounded responses
- 🧠 **FAISS Vector DB** - Facebook's efficient similarity search engine
- 🌐 **Multi-Source Intelligence** - Combines web search + knowledge base
- ⚡ **Groq Inference** - Lightning-fast LLM processing (Llama 3.3 70B)
- 💾 **Knowledge Retention** - Learns and builds knowledge base over time
- 🎯 **Citation Tracking** - Proper source attribution in reports

---

## ✨ Key Features

### 🦜 LangChain Integration

**Professional Implementation:**
- **LLMChain** - Structured reasoning chains
- **PromptTemplate** - Engineered prompt management
- **ChatGroq** - Production LLM backend
- **Document System** - Proper document handling

### 📊 RAG (Retrieval Augmented Generation)

**Complete RAG Pipeline:**

```
1. Index: Documents → Embeddings → FAISS Vector Store
2. Retrieve: Query → Similarity Search → Top-K Documents
3. Augment: Retrieved Context + Query → Enhanced Prompt
4. Generate: LLM → Comprehensive, Grounded Response
```

**Benefits:**
- ✅ Reduces hallucinations
- ✅ Grounded in actual data
- ✅ Cites sources
- ✅ Knowledge accumulation

### 🧠 Vector Database (FAISS)

**Facebook AI Similarity Search:**
- **Efficient**: Sub-second similarity search
- **Scalable**: Handles thousands of documents
- **CPU-Optimized**: No GPU required
- **Battle-Tested**: Used in production by Meta

**Technical Details:**
- Embedding Model: `all-MiniLM-L6-v2` (384 dimensions)
- Similarity: Cosine similarity
- Storage: In-memory with session persistence

---

## 🏗️ Architecture

```
User Query
    ↓
┌─────────┴─────────┐
│                   │
Web Search      Vector Store
(DuckDuckGo)       (FAISS)
│                   │
└─────────┬─────────┘
          ↓
   LangChain Chain
   (PromptTemplate
    + LLMChain)
          ↓
   Groq Inference
   (Llama 3.3 70B)
          ↓
┌─────────┴─────────┐
│                   │
Display Report   Save to FAISS
with Citations   Vector Store
```

---

## 🚀 Live Demo

**Try it now:** [Link](https://ai-researchgpt.streamlit.app/)

### Example Queries

```
"What are the latest developments in quantum computing?"

"Explain the impact of AI on healthcare in 2025"

"Compare different approaches to renewable energy"

"Recent breakthroughs in cancer treatment research"
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **LangChain** | 0.1.20 | AI framework & chains |
| **LangChain-Groq** | 0.1.3 | Groq integration |
| **FAISS** | 1.7.4 | Vector similarity search |
| **Sentence-Transformers** | 2.2.2 | Text embeddings |
| **Groq** | Latest | LLM inference |
| **Streamlit** | Latest | Web interface |
| **DuckDuckGo Search** | 5.3.0 | Web search API |

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

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Streamlit secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   ```
   Navigate to http://localhost:8501
   ```

---

## 📁 Project Structure

```
research-gpt/
│
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # Documentation
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
│
└── .streamlit/
    └── secrets.toml        # API keys (local only, gitignored)
```

---

## 🎯 Use Cases

### For Researchers
- **Literature Review** - Quick synthesis of multiple sources
- **Topic Exploration** - Understand new domains rapidly
- **Citation Management** - Automatic source tracking
- **Knowledge Building** - Accumulate research over time

### For Students
- **Assignment Research** - Comprehensive topic coverage
- **Exam Preparation** - Quick summaries with sources
- **Project Research** - Background information gathering
- **Academic Writing** - Cited research compilation

### For Professionals
- **Market Research** - Industry trends and insights
- **Competitive Analysis** - Compare products and strategies
- **Decision Support** - Data-driven recommendations
- **Technical Research** - Latest developments in tech

### For Content Creators
- **Content Research** - Background for articles/videos
- **Fact Checking** - Verify information quickly
- **Trend Analysis** - What's current in your niche
- **Deep Dives** - Comprehensive topic exploration

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **First Query** | 1-2 minutes (model loading) |
| **Subsequent Queries** | 30-60 seconds |
| **Web Search** | 2-5 seconds |
| **Vector Search** | < 100ms |
| **Report Generation** | 20-40 seconds |

---

## 🔬 Technical Highlights

### Advanced Concepts Demonstrated

1. **RAG Architecture** - Complete implementation from scratch
2. **Vector Databases** - FAISS integration and optimization
3. **LangChain Framework** - Production-grade chains
4. **Embeddings** - Semantic similarity search
5. **Prompt Engineering** - Structured, effective prompts
6. **Session Management** - Stateful application design

**Why This Project Stands Out:**
- Production-ready architecture
- Advanced AI/ML concepts
- Real-world application
- Scalable design
- Professional code structure

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Ideas for Contributions

- [ ] PDF/DOCX upload support
- [ ] Multi-language support
- [ ] Advanced citation formats (APA, MLA)
- [ ] Export to PDF/DOCX
- [ ] Research topic comparison
- [ ] Custom knowledge base management
- [ ] API endpoint

---

## 📝 Roadmap

- [x] Core LangChain integration
- [x] RAG architecture
- [x] FAISS vector database
- [x] Web search integration
- [x] Report generation
- [x] Research history
- [ ] Document upload (PDF/DOCX)
- [ ] Export to PDF with formatting
- [ ] Multi-query comparison
- [ ] Advanced filtering
- [ ] API access

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kanav Chauhan**

- GitHub: [@KanavChauhan23](https://github.com/KanavChauhan23)
- LinkedIn: [Kanav Chauhan](https://linkedin.com/in/kanavchauhan23)

---

## 🙏 Acknowledgments

- **LangChain** for the amazing AI framework
- **Groq** for lightning-fast LLM inference
- **Facebook AI** for FAISS vector search
- **Sentence-Transformers** for embeddings
- **Streamlit** for the beautiful UI framework
- The open-source AI community

---

## 💡 How It Works

### RAG Implementation

**1. Indexing Phase:**
```python
# Save research to vector store
document = Document(
    page_content=report_chunk,
    metadata={"query": query, "timestamp": timestamp}
)
embedding = embeddings_model.encode(report_chunk)
vector_store.add_documents([document])
```

**2. Retrieval Phase:**
```python
# Search similar documents
query_embedding = embeddings_model.encode(query)
similar_docs = vector_store.similarity_search(query, k=3)
```

**3. Generation:**
```python
# LangChain combines context and generates
context = web_results + vector_store_results
report = llm_chain.invoke({
    "query": query,
    "context": context
})
```

---

## 📚 Learning Resources

**LangChain:**
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)

**RAG:**
- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

**FAISS:**
- [FAISS Documentation](https://faiss.ai/)
- [FAISS Tutorial](https://github.com/facebookresearch/faiss/wiki/Getting-started)

---

<div align="center">

**Made with ❤️ by Kanav Chauhan**

If you found this helpful, please give it a ⭐!

[⬆ Back to Top](#-researchgpt)

</div>
