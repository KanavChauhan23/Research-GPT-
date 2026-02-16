import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime

# Text splitter class (manual implementation to avoid import issues)
class SimpleTextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text):
        """Simple text splitting"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.chunk_overlap
        
        return chunks

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
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "research_history" not in st.session_state:
    st.session_state.research_history = []

# Initialize Groq
try:
    llm = ChatGroq(
        api_key=st.secrets["GROQ_API_KEY"],
        model="llama-3.3-70b-versatile",
        temperature=0.7
    )
except Exception as e:
    st.error("⚠️ GROQ_API_KEY not found! Add it in Streamlit Secrets.")
    st.stop()

# Initialize embeddings
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# Initialize vector store
@st.cache_resource
def get_vector_store():
    embeddings = get_embeddings()
    try:
        return Chroma(
            collection_name="research_db",
            embedding_function=embeddings,
            persist_directory="./chroma_db"
        )
    except:
        return None

# Web search function
def search_web(query):
    """Search the web using DuckDuckGo"""
    try:
        search = DuckDuckGoSearchAPIWrapper()
        results = search.run(query)
        return results
    except Exception as e:
        return f"Web search temporarily unavailable. Error: {str(e)}"

# Vector search function
def search_knowledge_base(query):
    """Search vector database"""
    try:
        vector_store = get_vector_store()
        if vector_store:
            docs = vector_store.similarity_search(query, k=3)
            if docs:
                return "\n\n".join([doc.page_content for doc in docs])
        return "No relevant information found in knowledge base."
    except:
        return "Knowledge base currently empty."

# Generate research report
def generate_research_report(query, web_results, kb_results):
    """Generate comprehensive research report"""
    
    prompt = PromptTemplate(
        input_variables=["query", "web_results", "kb_results"],
        template="""You are a professional research assistant. Create a comprehensive research report.

Research Query: {query}

Web Search Results:
{web_results}

Knowledge Base Results:
{kb_results}

Create a detailed, well-structured research report with:

# Research Report: [Topic]

## Executive Summary
Brief 2-3 sentence overview of key findings.

## Current Information (Web Sources)
Detailed findings from web search with key points.

## Historical Context (Knowledge Base)
Relevant information from past research.

## Key Insights
Your analysis combining both sources.

## Sources
List sources mentioned inline using [Web], [KB] tags.

## Conclusion
Summary and key takeaways.

Make it professional, cite sources inline, and provide actionable insights.
"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    report = chain.run(
        query=query,
        web_results=web_results[:2000],
        kb_results=kb_results[:1000]
    )
    
    return report

# Save to vector store
def save_to_knowledge_base(query, report):
    """Save research to vector database"""
    try:
        vector_store = get_vector_store()
        if vector_store:
            metadata = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "type": "research_report"
            }
            
            text_splitter = SimpleTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_text(report)
            
            vector_store.add_texts(
                texts=chunks,
                metadatas=[metadata] * len(chunks)
            )
            return True
    except:
        pass
    return False

# Header
st.markdown('<h1 class="main-header">🔬 ResearchGPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">AI-Powered Research with Multi-Source Intelligence</p>', unsafe_allow_html=True)
st.markdown("---")

# Main interface
tab1, tab2, tab3 = st.tabs(["🔍 Research", "📚 History", "ℹ️ About"])

with tab1:
    st.markdown("### 🎯 What would you like to research?")
    
    research_query = st.text_area(
        "",
        placeholder="Example: What are the latest developments in quantum computing?\n\nOr: Explain the impact of AI on healthcare",
        height=100
    )
    
    if st.button("🚀 Start Research", type="primary", use_container_width=True):
        if not research_query.strip():
            st.warning("⚠️ Please enter a research question!")
        else:
            st.markdown("---")
            st.markdown("## 🔍 Research in Progress")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Web search
                status_text.text("📡 Searching web sources...")
                progress_bar.progress(20)
                
                web_results = search_web(research_query)
                
                progress_bar.progress(40)
                status_text.text("💾 Searching knowledge base...")
                
                # Step 2: Knowledge base search
                kb_results = search_knowledge_base(research_query)
                
                progress_bar.progress(60)
                status_text.text("📝 Generating comprehensive report...")
                
                # Step 3: Generate report
                report = generate_research_report(research_query, web_results, kb_results)
                
                progress_bar.progress(80)
                status_text.text("💾 Saving to knowledge base...")
                
                # Step 4: Save to vector store
                save_to_knowledge_base(research_query, report)
                
                progress_bar.progress(100)
                status_text.text("✅ Research complete!")
                
                # Display results
                st.markdown("---")
                st.success("✅ Research Complete!")
                
                st.markdown("## 📊 Research Report")
                st.markdown(report)
                
                # Save to history
                st.session_state.research_history.append({
                    "query": research_query,
                    "report": report,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Download button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ Research error: {str(e)}")
                st.info("💡 Tip: Try simplifying your query or check your internet connection.")

with tab2:
    st.markdown("### 📚 Research History")
    
    if st.session_state.research_history:
        for idx, research in enumerate(reversed(st.session_state.research_history)):
            with st.expander(f"🔍 {research['query'][:100]}... - {research['timestamp']}"):
                st.markdown(research['report'])
                
                st.download_button(
                    label="📥 Download",
                    data=research['report'],
                    file_name=f"research_{idx}.txt",
                    key=f"download_{idx}"
                )
    else:
        st.info("No research history yet. Start researching to see your history here!")
    
    if st.session_state.research_history:
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.research_history = []
            st.rerun()

with tab3:
    st.markdown("### 🔬 About ResearchGPT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **ResearchGPT** is an AI-powered research assistant.
        
        **Features:**
        - 🌐 Multi-source web search
        - 🧠 AI analysis
        - 💾 Knowledge base
        - 📊 Comprehensive reports
        - 📥 Export functionality
        
        **Technology:**
        - LangChain framework
        - Vector Database
        - Groq AI (Llama 3.3)
        - Semantic Search
        """)
    
    with col2:
        st.markdown("""
        **How It Works:**
        
        1. **Input** - Enter research question
        2. **Search** - Web + knowledge base
        3. **Analyze** - AI combines findings
        4. **Report** - Comprehensive output
        5. **Save** - Stores for future queries
        
        **Best Practices:**
        - Be specific with queries
        - Use complete questions
        - Review sources
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔬 ResearchGPT")
    
    st.markdown("""
    **Powered By:**
    - 🤖 LangChain
    - 🧠 Groq AI
    - 📊 Vector DB
    - 🔍 Web Search
    
    **Status:** 🟢 Active
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Sample Queries")
    
    samples = [
        "Latest AI developments 2025",
        "Renewable energy comparison",
        "Quantum computing applications",
        "Climate change solutions"
    ]
    
    for sample in samples:
        if st.button(sample, key=sample, use_container_width=True):
            st.session_state.sample_query = sample
    
    st.markdown("---")
    
    st.markdown("### 📊 Statistics")
    st.metric("Research Conducted", len(st.session_state.research_history))

# Footer
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.link_button(
        "🔗 Connect on LinkedIn",
        "https://linkedin.com/in/kanavchauhan23",
        use_container_width=True,
        type="primary"
    )

st.markdown("<h4 style='text-align: center;'>Built with ❤️ by Kanav Chauhan</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>ResearchGPT - AI Research Made Simple</p>", unsafe_allow_html=True)
