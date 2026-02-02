

import streamlit as st
import anthropic
import os

try:
    API_KEY = st.secrets["ANTHROPIC_API_KEY"]
except:
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    if not API_KEY:
        st.error("⚠️ API key not configured. Please contact the developer.")
        st.stop()

def analyze_gaps(job_description, resume):
    """Analyzes gaps and generates interview prep"""
    
    client = anthropic.Anthropic(api_key=API_KEY)
    
    prompt = f"""You are an expert career coach and interviewer. 

Compare this job description with this candidate's resume and help them prepare for the interview.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume}

Please provide:

1. SKILL GAPS (3-5 items)
   - List specific skills, experiences, or qualifications mentioned in the job that are missing or weak in the resume
   - Focus on requirements, not nice-to-haves
   - Be specific (e.g., "No SQL experience mentioned" not just "lacking technical skills")

2. TOUGH INTERVIEW QUESTIONS (1 question per gap)
   - For each gap, generate one behavioral or technical question an interviewer might ask to probe that weakness
   - Make questions realistic and specific to the role
   - Frame as actual interview questions (e.g., "Tell me about a time when...")

3. PREPARATION SUGGESTIONS (brief, 1-2 sentences per gap)
   - How the candidate can quickly build credibility in this area
   - What stories from their resume could be reframed to address this
   - What they should study/review before the interview

Format your response clearly with headers for each section."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"


st.set_page_config(
    page_title="Interview Weakness Spotter",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Interview Weakness Spotter")
st.markdown("### Identify skill gaps and prepare for tough interview questions")
st.markdown("---")

with st.expander("ℹ️ How to use this tool"):
    st.markdown("""
    1. Paste the job description in the left box
    2. Paste your resume in the right box
    3. Click Analyze and wait 10-20 seconds
    4. Review your personalized interview prep insights
    5. Download the results if you want to save them
    """)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the full job description here:",
        height=300,
        placeholder="Copy and paste the job description from LinkedIn, Indeed, or company website..."
    )

with col2:
    st.subheader("📄 Resume")
    resume = st.text_area(
        "Paste your resume here:",
        height=300,
        placeholder="Copy and paste your resume text here..."
    )

st.markdown("---")
col_button1, col_button2, col_button3 = st.columns([1, 1, 1])

with col_button2:
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze_button:
    if not job_description or len(job_description) < 50:
        st.error("⚠️ Please paste a complete job description (at least 50 characters)")
    elif not resume or len(resume) < 50:
        st.error("⚠️ Please paste your resume (at least 50 characters)")
    else:
        with st.spinner("🔍 Analyzing... This takes 10-20 seconds"):
            results = analyze_gaps(job_description, resume)
        
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        st.markdown(results)
        
        st.download_button(
            label="📥 Download Results",
            data=results,
            file_name="interview_prep.txt",
            mime="text/plain"
        )
        
        st.success("✅ Analysis complete! Review the gaps and prepare accordingly.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built by Adwit | Powered by Claude AI"
    "</div>",
    unsafe_allow_html=True
)
