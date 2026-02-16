import streamlit as st
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
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
    
    .research-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .source-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "research_history" not in st.session_state:
    st.session_state.research_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None

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

# Initialize embeddings (cached)
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# Initialize vector store
@st.cache_resource
def get_vector_store():
    embeddings = get_embeddings()
    return Chroma(
        collection_name="research_db",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

# Header
st.markdown('<h1 class="main-header">🔬 ResearchGPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">AI-Powered Research Assistant with Multi-Source Intelligence</p>', unsafe_allow_html=True)
st.markdown("---")

# Initialize tools
@st.cache_resource
def setup_tools():
    """Setup research tools"""
    
    # Web search tool
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="Web Search",
        func=search.run,
        description="Useful for finding current information on the internet. Use this to search for recent data, news, articles, and information."
    )
    
    # Vector store tool
    vector_store = get_vector_store()
    
    def vector_search(query):
        """Search vector database"""
        try:
            docs = vector_store.similarity_search(query, k=3)
            if docs:
                return "\n\n".join([doc.page_content for doc in docs])
            return "No relevant information found in knowledge base."
        except:
            return "Knowledge base is empty."
    
    vector_tool = Tool(
        name="Knowledge Base",
        func=vector_search,
        description="Search through previously researched topics and saved information. Use this to find information from past research."
    )
    
    return [search_tool, vector_tool]

# Setup agent
def create_research_agent():
    """Create LangChain agent"""
    tools = setup_tools()
    
    # Create a simple React prompt
    prompt = PromptTemplate.from_template("""
You are a helpful research assistant. You have access to the following tools:

{tools}

Tool Names: {tool_names}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return agent_executor

# Report generation
def generate_research_report(query, findings):
    """Generate comprehensive research report"""
    
    report_prompt = PromptTemplate(
        input_variables=["query", "findings"],
        template="""You are a professional research assistant. Based on the research findings below, create a comprehensive research report.

Research Query: {query}

Findings from various sources:
{findings}

Create a detailed research report with the following structure:

# Research Report: [Topic]

## Executive Summary
[2-3 sentence overview of key findings]

## Key Findings
[Detailed findings organized by themes/topics]

## Analysis
[Your analysis and insights from the findings]

## Sources & Citations
[List all sources mentioned in the findings]

## Conclusion
[Summary and recommendations]

Make it professional, well-structured, and cite sources inline using [Source: ...] format.
"""
    )
    
    chain = LLMChain(llm=llm, prompt=report_prompt)
    report = chain.run(query=query, findings=findings)
    
    return report

# Save to vector store
def save_to_knowledge_base(query, report):
    """Save research to vector database"""
    try:
        vector_store = get_vector_store()
        
        # Create metadata
        metadata = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "type": "research_report"
        }
        
        # Add to vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(report)
        
        vector_store.add_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks)
        )
        
        return True
    except Exception as e:
        st.error(f"Error saving to knowledge base: {str(e)}")
        return False

# Main interface
tab1, tab2, tab3 = st.tabs(["🔍 Research", "📚 History", "ℹ️ About"])

with tab1:
    st.markdown("### 🎯 What would you like to research?")
    
    # Research input
    research_query = st.text_area(
        "",
        placeholder="Example: What are the latest developments in quantum computing?\n\nOr: Compare renewable energy sources and their efficiency",
        height=100,
        help="Enter your research question. The AI will search multiple sources and create a comprehensive report."
    )
    
    # Research depth
    col1, col2 = st.columns([3, 1])
    with col1:
        research_depth = st.select_slider(
            "Research Depth",
            options=["Quick", "Standard", "Deep"],
            value="Standard",
            help="Quick: Fast overview | Standard: Balanced | Deep: Comprehensive analysis"
        )
    
    # Research button
    if st.button("🚀 Start Research", type="primary", use_container_width=True):
        if not research_query.strip():
            st.warning("⚠️ Please enter a research question!")
        else:
            # Create agent
            with st.spinner("🔬 Initializing AI Research Assistant..."):
                agent = create_research_agent()
            
            # Conduct research
            st.markdown("---")
            st.markdown("## 🔍 Research in Progress")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Initial query
                status_text.text("📡 Searching web sources...")
                progress_bar.progress(20)
                
                # Run agent
                result = agent.invoke({
                    "input": f"Research this topic comprehensively: {research_query}\n\nProvide detailed findings with sources."
                })
                
                # Extract output
                findings = result.get("output", str(result))
                
                progress_bar.progress(60)
                status_text.text("📝 Generating comprehensive report...")
                
                # Generate report
                report = generate_research_report(research_query, findings)
                
                progress_bar.progress(80)
                status_text.text("💾 Saving to knowledge base...")
                
                # Save to vector store
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
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download",
                        data=research['report'],
                        file_name=f"research_{idx}.txt",
                        key=f"download_{idx}"
                    )
    else:
        st.info("No research history yet. Start researching to see your history here!")
    
    # Clear history button
    if st.session_state.research_history:
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.research_history = []
            st.rerun()

with tab3:
    st.markdown("### 🔬 About ResearchGPT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **ResearchGPT** is an advanced AI-powered research assistant that helps you conduct comprehensive research on any topic.
        
        **Key Features:**
        - 🌐 Multi-source web search
        - 🧠 AI-powered analysis
        - 📊 Comprehensive reports
        - 💾 Knowledge base storage
        - 📚 Research history
        - 📥 Export functionality
        
        **Technology:**
        - LangChain Agents
        - Vector Database (ChromaDB)
        - Groq AI (Llama 3.3)
        - Semantic Search
        """)
    
    with col2:
        st.markdown("""
        **How It Works:**
        
        1. **Input Query** - Enter your research question
        
        2. **AI Agent** - LangChain agent activates
        
        3. **Multi-Source Search** - Searches web + knowledge base
        
        4. **Synthesis** - AI analyzes and combines findings
        
        5. **Report** - Generates comprehensive report with citations
        
        6. **Storage** - Saves to vector database for future queries
        
        **Best Practices:**
        - Be specific with queries
        - Use complete questions
        - Review and verify sources
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔬 ResearchGPT")
    
    st.markdown("""
    **Powered By:**
    - 🤖 LangChain Agents
    - 🧠 Groq AI (Llama 3.3)
    - 📊 Vector Database
    - 🔍 Web Search
    
    **Status:** 🟢 Active
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Sample Queries")
    
    samples = [
        "Latest developments in AI research 2025",
        "Compare renewable energy sources",
        "Quantum computing applications",
        "Impact of AI on healthcare",
        "Climate change solutions"
    ]
    
    for sample in samples:
        if st.button(sample, key=sample, use_container_width=True):
            st.session_state.sample_query = sample
    
    st.markdown("---")
    
    st.markdown("### 📊 Statistics")
    st.metric("Research Conducted", len(st.session_state.research_history))
    
    # Knowledge base size
    try:
        vector_store = get_vector_store()
        collection = vector_store._collection
        count = collection.count()
        st.metric("Knowledge Base Items", count)
    except:
        st.metric("Knowledge Base Items", "0")

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
st.markdown("<p style='text-align: center; color: gray;'>ResearchGPT - AI-Powered Research Made Simple</p>", unsafe_allow_html=True)
