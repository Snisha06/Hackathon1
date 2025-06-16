# main.py
import streamlit as st
from utils import load_data
from agent import match_students_to_role
import json

st.set_page_config(layout="wide", page_title="AI Matchmaker")
st.title("🎯 Company–Student Matchmaker")

# Load data
students = load_data("data/students.json")
roles = load_data("data/roles.json")

# UI
role_options = [r["role"] for r in roles]
selected_role = st.selectbox("Choose a Role", role_options)

if st.button("Generate Top 10 Shortlist"):
    with st.spinner("🔍 Finding best matches..."):
        try:
            # Get selected role data
            role = next(r for r in roles if r["role"] == selected_role)
            
            # Get matches (now returns parsed JSON)
            matches = match_students_to_role(
                json.dumps(students, indent=2), 
                json.dumps(role, indent=2)
            )
            
            st.subheader("🏆 Top 10 Matches")
            
            # Display matches
            for i, match in enumerate(matches, 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
**{i}. {match['name']}**  
✅ **Match Reason:** {match['match_reason']}
""")
                    
                    with col2:
                        st.metric("Score", f"{match['score']}/100")
                    
                    st.divider()
                    
        except Exception as e:
            st.error("❌ Error generating matches.")
            st.error(f"Error details: {str(e)}")
            
            # Debug information
            with st.expander("🔧 Debug Information"):
                role = next(r for r in roles if r["role"] == selected_role)
                raw_response = match_students_to_role.__globals__['llm'].invoke(
                    match_students_to_role.__globals__['PromptTemplate'].from_template("""
You are a recruiter AI.
Given the following role: {role}
And these students: {students}
Match the top 10 students who best fit the role based on skills, interests, and certifications.
Return ONLY a valid JSON array.
""").format(role=json.dumps(role, indent=2), students=json.dumps(students, indent=2))
                ).content
                
                st.code(raw_response, language="text")
                st.caption(f"Response type: {type(raw_response)} | Length: {len(raw_response)}")
