# agent.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import json
import re

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

def clean_json_response(response_text):
    """Clean AI response and extract valid JSON"""
    try:
        # Remove markdown code blocks if present
        cleaned = response_text.strip()
        
        # Remove ```json and ``` markers
        if cleaned.startswith('```'):
            # Find the JSON content between code blocks
            lines = cleaned.split('\n')
            start_idx = 0
            end_idx = len(lines)
            
            for i, line in enumerate(lines):
                if line.strip().startswith('['):
                    start_idx = i
                    break
                    
            for i in range(len(lines)-1, -1, -1):
                if line.strip().endswith(']'):
                    end_idx = i + 1
                    break
                    
            cleaned = '\n'.join(lines[start_idx:end_idx])
        
        # Try to parse as JSON
        return json.loads(cleaned)
        
    except json.JSONDecodeError as e:
        # If still fails, try to extract JSON using regex
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        raise ValueError(f"Could not parse JSON: {e}")

def match_students_to_role(students, role):
    template = PromptTemplate.from_template("""
You are a recruiter AI.

Given the following role:
{role}

And these students:
{students}

Match the top 10 students who best fit the role based on skills, interests, and certifications.

IMPORTANT: Return ONLY a valid JSON array. No markdown, no extra text, no explanations.

Example format:
[
  {{
    "name": "Student Name",
    "match_reason": "Brief explanation of why they match",
    "score": 85
  }}
]

Return the JSON array now:
""")
    
    prompt = template.format(role=role, students=students)
    response = llm.invoke(prompt).content
    
    return clean_json_response(response)
