import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from datetime import datetime

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
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("⚠️ GROQ_API_KEY not found! Add it in Streamlit Secrets.")
    st.stop()

# Web search function
def search_web(query):
    """Search the web using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            
            if results:
                formatted_results = []
                for i, result in enumerate(results, 1):
                    formatted_results.append(
                        f"Source {i}:\n"
                        f"Title: {result.get('title', 'N/A')}\n"
                        f"Content: {result.get('body', 'N/A')}\n"
                        f"URL: {result.get('href', 'N/A')}\n"
                    )
                return "\n\n".join(formatted_results)
            return "No web results found."
    except Exception as e:
        return f"Web search temporarily unavailable: {str(e)}"

# Generate research report
def generate_research_report(query, web_results):
    """Generate comprehensive research report using Groq"""
    
    prompt = f"""You are a professional research assistant. Create a comprehensive research report.

Research Query: {query}

Web Search Results:
{web_results}

Create a detailed, well-structured research report with these sections:

# Research Report: {query}

## Executive Summary
Brief 2-3 sentence overview of the most important findings.

## Key Findings
Detailed information organized by themes. Use bullet points for clarity.

## Analysis & Insights
Your expert analysis of the information gathered.

## Sources
List the main sources used (mention Source 1, Source 2, etc. from the web results).

## Conclusion
Summary and key takeaways.

Make it professional, well-organized, and cite sources inline using [Source X] format.
Keep the report comprehensive but concise."""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert research assistant who creates comprehensive, well-cited research reports."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=3000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating report: {str(e)}"

# Header
st.markdown('<h1 class="main-header">🔬 ResearchGPT</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">AI-Powered Research Assistant</p>', unsafe_allow_html=True)
st.markdown("---")

# Main interface
tab1, tab2, tab3 = st.tabs(["🔍 Research", "📚 History", "ℹ️ About"])

with tab1:
    st.markdown("### 🎯 What would you like to research?")
    
    research_query = st.text_area(
        "",
        placeholder="Example: What are the latest developments in quantum computing?\n\nOr: Explain the impact of AI on healthcare in 2025",
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
                progress_bar.progress(30)
                
                web_results = search_web(research_query)
                
                progress_bar.progress(60)
                status_text.text("🤖 AI is analyzing and synthesizing information...")
                
                # Step 2: Generate report
                report = generate_research_report(research_query, web_results)
                
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
                st.markdown("---")
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
            
            finally:
                progress_bar.empty()
                status_text.empty()

with tab2:
    st.markdown("### 📚 Research History")
    
    if st.session_state.research_history:
        for idx, research in enumerate(reversed(st.session_state.research_history)):
            with st.expander(f"🔍 {research['query'][:80]}... - {research['timestamp']}"):
                st.markdown(research['report'])
                
                st.download_button(
                    label="📥 Download",
                    data=research['report'],
                    file_name=f"research_{idx}.txt",
                    key=f"download_{idx}"
                )
        
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.research_history = []
            st.rerun()
    else:
        st.info("No research history yet.")

with tab3:
    st.markdown("### 🔬 About ResearchGPT")
    
    st.markdown("""
    **ResearchGPT** is an AI-powered research assistant.
    
    **Features:**
    - 🌐 Multi-source web search
    - 🤖 AI synthesis
    - 📊 Professional reports
    - 📥 Export functionality
    
    **Technology:**
    - Groq AI (Llama 3.3)
    - DuckDuckGo Search
    - Streamlit
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔬 ResearchGPT")
    st.markdown("**Status:** 🟢 Active")
    st.markdown("---")
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
