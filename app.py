"""
ResearchGPT - Professional AI Research Assistant
Built with LangChain, RAG Architecture, and Vector Database

Author: Kanav Chauhan
Tech: LangChain, Groq, FAISS, RAG
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from duckduckgo_search import DDGS
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="ResearchGPT - AI Research Assistant",
    layout="wide",
    page_icon="🔬"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .tech-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "research_history" not in st.session_state:
    st.session_state.research_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# Initialize LLM
try:
    llm = ChatGroq(
        api_key=st.secrets["GROQ_API_KEY"],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=3000
    )
except:
    st.error("⚠️ GROQ_API_KEY not found!")
    st.stop()

# Embeddings
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

# Web search
def search_web(query, max_results=5):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if results:
                formatted = []
                for i, r in enumerate(results, 1):
                    formatted.append(
                        f"Source {i}:\nTitle: {r.get('title')}\n"
                        f"Content: {r.get('body')}\nURL: {r.get('href')}\n"
                    )
                return "\n\n".join(formatted)
        return "No results found."
    except Exception as e:
        return f"Search error: {str(e)}"

# RAG system
def search_vector_store(query):
    try:
        if st.session_state.vector_store:
            docs = st.session_state.vector_store.similarity_search(query, k=3)
            if docs:
                results = []
                for i, doc in enumerate(docs, 1):
                    meta = doc.metadata
                    results.append(
                        f"Past Research {i}:\nQuery: {meta.get('query')}\n"
                        f"Date: {meta.get('timestamp')}\n"
                        f"Content: {doc.page_content[:200]}...\n"
                    )
                return "\n\n".join(results)
        return "Knowledge base empty."
    except:
        return "KB search unavailable."

def add_to_vector_store(texts, metadatas):
    try:
        embeddings = get_embeddings()
        docs = [Document(page_content=t, metadata=m) for t, m in zip(texts, metadatas)]
        
        if st.session_state.vector_store is None:
            st.session_state.vector_store = FAISS.from_documents(docs, embeddings)
        else:
            st.session_state.vector_store.add_documents(docs)
        return True
    except:
        return False

# LangChain research chain
def create_research_chain():
    template = """You are a professional research assistant.

Query: {query}

Web Sources:
{web_results}

Knowledge Base:
{kb_results}

Create a comprehensive research report with:

# {query}

## Executive Summary
2-3 sentences of key findings.

## Key Findings
- Current information from web
- Historical context from knowledge base
- Cite sources as [Source 1], [Source 2]

## Analysis
Your expert analysis and insights.

## Sources
List all sources used.

## Conclusion
Key takeaways and recommendations.

Be thorough, cite sources, provide insights."""

    prompt = PromptTemplate(
        input_variables=["query", "web_results", "kb_results"],
        template=template
    )
    return LLMChain(llm=llm, prompt=prompt)

# Header
st.markdown('<h1 class="main-header">🔬 ResearchGPT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#666;font-size:1.2rem;">Professional AI Research with LangChain & RAG</p>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;margin-bottom:2rem;'>
    <span class='tech-badge'>🦜 LangChain</span>
    <span class='tech-badge'>🧠 RAG</span>
    <span class='tech-badge'>📊 FAISS</span>
    <span class='tech-badge'>⚡ Groq</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Main interface
tab1, tab2, tab3 = st.tabs(["🔍 Research", "📚 History", "ℹ️ About"])

with tab1:
    st.markdown("### 🎯 Enter Your Research Question")
    
    research_query = st.text_area(
        "",
        placeholder="Example: What are the latest developments in quantum computing?",
        height=100
    )
    
    if st.button("🚀 Start Research", type="primary", use_container_width=True):
        if not research_query.strip():
            st.warning("⚠️ Please enter a question!")
        else:
            st.markdown("---")
            progress = st.progress(0)
            status = st.empty()
            
            try:
                # Web search
                status.text("📡 Searching web...")
                progress.progress(33)
                web_results = search_web(research_query)
                
                # KB search
                status.text("💾 Searching knowledge base...")
                progress.progress(66)
                kb_results = search_vector_store(research_query)
                
                # Generate report
                status.text("🦜 LangChain processing...")
                chain = create_research_chain()
                result = chain.invoke({
                    "query": research_query,
                    "web_results": web_results,
                    "kb_results": kb_results
                })
                report = result.get("text", "Error")
                
                # Save to vector store
                metadata = {
                    "query": research_query,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                chunks = [report[i:i+1000] for i in range(0, len(report), 800)]
                add_to_vector_store(chunks, [metadata] * len(chunks))
                
                progress.progress(100)
                status.text("✅ Complete!")
                
                # Display
                st.success("✅ Research Complete! (LangChain + RAG)")
                st.markdown("## 📊 Report")
                st.markdown(report)
                
                # Save history
                st.session_state.research_history.append({
                    "query": research_query,
                    "report": report,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Download
                st.download_button(
                    "📥 Download Report",
                    data=report,
                    file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            finally:
                progress.empty()
                status.empty()

with tab2:
    st.markdown("### 📚 Research History")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Research", len(st.session_state.research_history))
    with col2:
        kb_count = 0
        if st.session_state.vector_store:
            try:
                kb_count = st.session_state.vector_store.index.ntotal
            except:
                pass
        st.metric("KB Vectors", kb_count)
    
    st.markdown("---")
    
    if st.session_state.research_history:
        for idx, r in enumerate(reversed(st.session_state.research_history)):
            with st.expander(f"🔍 {r['query'][:70]}... - {r['timestamp']}"):
                st.markdown(r['report'])
                st.download_button(
                    "📥 Download",
                    data=r['report'],
                    file_name=f"research_{idx}.txt",
                    key=f"dl_{idx}"
                )
        
        if st.button("🗑️ Clear History"):
            st.session_state.research_history = []
            st.rerun()
    else:
        st.info("No history yet.")

with tab3:
    st.markdown("### 🏗️ Architecture")
    
    st.markdown("""
    **🦜 LangChain Integration**
    - LLMChain for processing
    - PromptTemplate for structure
    - ChatGroq backend
    
    **📊 RAG Architecture**
    - Retrieval Augmented Generation
    - FAISS vector database
    - Semantic search
    - Knowledge retention
    
    **🔍 Multi-Source**
    - Web search (current info)
    - Knowledge base (past research)
    - AI synthesis
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔬 ResearchGPT")
    st.markdown("**Status:** 🟢 Active")
    st.markdown("---")
    st.metric("Queries", len(st.session_state.research_history))

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.link_button(
        "🔗 LinkedIn",
        "https://linkedin.com/in/kanavchauhan23",
        use_container_width=True,
        type="primary"
    )

st.markdown("<h4 style='text-align:center;'>Built with ❤️ by Kanav Chauhan</h4>", unsafe_allow_html=True)
