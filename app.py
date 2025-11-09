import streamlit as st
import requests
import json
from datetime import datetime
import time
from typing import Dict, List, Optional
from prompts import get_prompt_template, TOPIC_EXAMPLES
from utils import (
    format_markdown_response, 
    export_to_markdown, 
    extract_checklist_items,
    validate_api_key_format,
    estimate_tokens
)
from config import Config

# Page Configuration
st.set_page_config(
    page_title="AI Startup Guide by SitaRaman",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .topic-card {
        padding: 1rem;
        border-radius: 10px;
        background: #f8f9fa;
        margin: 0.5rem 0;
    }
    .response-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .checklist-item {
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-left: 3px solid #667eea;
        background: #f8f9fa;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    """Initialize all session state variables"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'startup_profile' not in st.session_state:
        st.session_state.startup_profile = {}
    if 'checklists' not in st.session_state:
        st.session_state.checklists = {}
    if 'api_calls_count' not in st.session_state:
        st.session_state.api_calls_count = 0
    if 'total_tokens_used' not in st.session_state:
        st.session_state.total_tokens_used = 0
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

init_session_state()

# API Call Function with Streaming
def call_openrouter_api(
    prompt: str, 
    api_key: str, 
    model: str = "openai/gpt-4o-mini",
    max_tokens: int = 2000,
    stream: bool = True,
    context: Optional[List[Dict]] = None
) -> Optional[str]:
    """
    Call OpenRouter API with optional streaming support
    """
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build messages with context
    messages = [
        {"role": "system", "content": "You are an expert startup advisor providing structured, practical guidance. Be specific, actionable, and encouraging."}
    ]
    
    # Add conversation history for context
    if context:
        messages.extend(context[-6:])  # Last 3 exchanges
    
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    try:
        if stream:
            response = requests.post(API_URL, headers=headers, json=payload, stream=True)
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
            
            full_response = ""
            response_placeholder = st.empty()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]
                        if line.strip() == '[DONE]':
                            break
                        try:
                            chunk = json.loads(line)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                full_response += content
                                response_placeholder.markdown(full_response + "▌")
                        except json.JSONDecodeError:
                            continue
            
            response_placeholder.markdown(full_response)
            return full_response
        else:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
            
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"].strip()
            
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return None

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)
    st.markdown("##  Configuration")
    
    # API Configuration
    or_api_token = st.text_input(
        "OpenRouter API Key",
        type="password",
        help="Get your key from https://openrouter.ai/keys"
    )
    
    if or_api_token and not validate_api_key_format(or_api_token):
        st.warning(" API key format looks incorrect")
    
    # Model Selection
    model_choice = st.selectbox(
        "Select Model",
        options=[
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "anthropic/claude-3-5-sonnet",
            "google/gemini-pro"
        ],
        help="Choose the AI model for guidance"
    )
    
    # Response Settings
    with st.expander(" Advanced Settings"):
        enable_streaming = st.checkbox("Enable Streaming Responses", value=True)
        max_tokens = st.slider("Max Response Length", 500, 3000, 2000, 100)
        include_context = st.checkbox("Include Conversation History", value=True)
    
    st.markdown("---")
    
    # Startup Profile
    st.markdown("##  Startup Profile")
    with st.form("startup_profile_form"):
        startup_name = st.text_input("Startup Name (Optional)")
        industry = st.selectbox(
            "Industry",
            ["SaaS", "E-commerce", "Fintech", "Healthcare", "EdTech", "Other"]
        )
        stage = st.selectbox(
            "Current Stage",
            ["Idea", "MVP", "Early Stage", "Growth", "Scale-up"]
        )
        team_size = st.selectbox(
            "Team Size",
            ["Solo Founder", "2-5", "6-10", "11-25", "25+"]
        )
        
        if st.form_submit_button(" Save Profile"):
            st.session_state.startup_profile = {
                "name": startup_name,
                "industry": industry,
                "stage": stage,
                "team_size": team_size,
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.success("Profile saved!")
    
    # Usage Statistics
    st.markdown("---")
    st.markdown("##  Usage Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", st.session_state.api_calls_count)
    with col2:
        st.metric("Tokens Used", f"{st.session_state.total_tokens_used:,}")
    
    # Clear History
    if st.button(" Clear History", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.checklists = {}
        st.rerun()
    
    # Help & Resources
    with st.expander(" Help & Resources"):
        st.markdown("""
        **Quick Tips:**
        - Be specific in your queries
        - Use startup profile for personalized advice
        - Ask follow-up questions for deeper insights
        
        **Troubleshooting:**
        - 401 Error: Check API key
        - Slow responses: Try smaller max_tokens
        - Rate limits: Wait a few minutes
        """)

# Main Header
st.markdown('<h1 class="main-header"> AI Startup Guidance Tool</h1>', unsafe_allow_html=True)
st.markdown("*Get personalized, AI-powered advice to grow your startup*")

# Topic Selection
topics = {
    " Scaling Business": "scaling",
    " Funding & Investment": "funding",
    " Team Setup & Hiring": "team",
    " Legal Documents": "documents",
    " Product Strategy": "product",
    " Marketing & Growth": "marketing",
    " General Advice": "general"
}

st.markdown("###  Select Topic or Ask Anything")
col1, col2 = st.columns([2, 1])

with col1:
    selected_topic_display = st.selectbox(
        "Choose guidance area:",
        options=list(topics.keys()),
        index=0
    )
    selected_topic = topics[selected_topic_display]

with col2:
    st.markdown("**Example Questions:**")
    if selected_topic in TOPIC_EXAMPLES:
        for example in TOPIC_EXAMPLES[selected_topic][:2]:
            if st.button(f" {example[:30]}...", key=example, use_container_width=True):
                st.session_state.quick_query = example

# Query Input
st.markdown("###  Your Question")
default_query = st.session_state.get('quick_query', '')
user_query = st.text_area(
    "Describe your specific question or scenario:",
    value=default_query,
    placeholder="e.g., How can I scale my e-commerce business from 10 to 100 users?",
    height=120,
    key="main_query"
)

# Clear quick query after use
if 'quick_query' in st.session_state:
    del st.session_state.quick_query

# Action Buttons
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    generate_button = st.button(" Get Guidance", type="primary", use_container_width=True)
with col2:
    refine_button = st.button(" Refine", use_container_width=True)
with col3:
    simplify_button = st.button(" Simplify", use_container_width=True)
with col4:
    expand_button = st.button(" Expand", use_container_width=True)

# Process Query
if any([generate_button, refine_button, simplify_button, expand_button]):
    if not user_query.strip():
        st.error(" Please enter a question to get guidance.")
    elif not or_api_token:
        st.warning(" Please provide an OpenRouter API key in the sidebar.")
    else:
        try:
            # Determine query type
            if refine_button:
                modifier = "\n\nProvide a more refined, detailed version of your previous response with specific examples and case studies."
            elif simplify_button:
                modifier = "\n\nSimplify your previous response to be more concise and actionable, focusing on immediate next steps."
            elif expand_button:
                modifier = "\n\nExpand on your previous response with more comprehensive details, additional strategies, and deeper insights."
            else:
                modifier = ""
            
            # Build context-aware prompt
            profile_context = ""
            if st.session_state.startup_profile:
                profile = st.session_state.startup_profile
                profile_context = f"\n\nStartup Context: {profile.get('industry')} startup at {profile.get('stage')} stage with {profile.get('team_size')} team members."
            
            # Get appropriate prompt template
            prompt_template = get_prompt_template(selected_topic)
            full_prompt = prompt_template.format(query=user_query) + profile_context + modifier
            
            # Prepare context from history
            context = None
            if include_context and st.session_state.conversation_history:
                context = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.conversation_history[-6:]
                ]
            
            # Show loading state
            with st.spinner(" Generating personalized guidance..."):
                st.markdown("---")
                st.markdown(f"## 💡 Guidance on {selected_topic_display}")
                
                # Call API
                guidance_text = call_openrouter_api(
                    full_prompt,
                    or_api_token,
                    model=model_choice,
                    max_tokens=max_tokens,
                    stream=enable_streaming,
                    context=context
                )
                
                if guidance_text:
                    # Update stats
                    st.session_state.api_calls_count += 1
                    st.session_state.total_tokens_used += estimate_tokens(full_prompt + guidance_text)
                    
                    # Save to history
                    st.session_state.conversation_history.append({
                        "role": "user",
                        "content": user_query,
                        "topic": selected_topic,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": guidance_text,
                        "topic": selected_topic,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Extract and display checklist if applicable
                    checklist_items = extract_checklist_items(guidance_text)
                    if checklist_items:
                        st.markdown("---")
                        st.markdown("###  Action Checklist")
                        checklist_key = f"{selected_topic}_{len(st.session_state.conversation_history)}"
                        
                        if checklist_key not in st.session_state.checklists:
                            st.session_state.checklists[checklist_key] = [False] * len(checklist_items)
                        
                        for idx, item in enumerate(checklist_items):
                            checked = st.checkbox(
                                item,
                                value=st.session_state.checklists[checklist_key][idx],
                                key=f"check_{checklist_key}_{idx}"
                            )
                            st.session_state.checklists[checklist_key][idx] = checked
                        
                        # Progress tracker
                        completed = sum(st.session_state.checklists[checklist_key])
                        total = len(checklist_items)
                        progress = completed / total if total > 0 else 0
                        st.progress(progress)
                        st.caption(f"Completed: {completed}/{total} tasks ({int(progress*100)}%)")
                    
                    # Export Options
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        markdown_export = export_to_markdown(
                            user_query,
                            guidance_text,
                            selected_topic_display,
                            checklist_items
                        )
                        st.download_button(
                            "📥 Download as Markdown",
                            markdown_export,
                            file_name=f"startup_guidance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    with col2:
                        st.download_button(
                            " Download as Text",
                            guidance_text,
                            file_name=f"guidance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                    # Related Topics
                    st.markdown("---")
                    st.markdown("###  Related Topics You Might Explore")
                    related_topics = [t for t in topics.keys() if t != selected_topic_display][:3]
                    cols = st.columns(len(related_topics))
                    for idx, topic in enumerate(related_topics):
                        with cols[idx]:
                            st.button(topic, key=f"related_{idx}", use_container_width=True)
                    
                    # Disclaimer
                    st.info("💡 **Disclaimer**: This is AI-generated general advice. Always consult with legal, financial, or domain experts for critical business decisions.")
        
        except Exception as e:
            st.error(f" Error: {str(e)}")
            with st.expander("🐛 Debug Information"):
                st.code(str(e))

# Conversation History
if st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("##  Conversation History")
    
    with st.expander("View Previous Queries & Responses", expanded=False):
        for idx in range(0, len(st.session_state.conversation_history), 2):
            if idx + 1 < len(st.session_state.conversation_history):
                user_msg = st.session_state.conversation_history[idx]
                assistant_msg = st.session_state.conversation_history[idx + 1]
                
                st.markdown(f"** Query ({user_msg['timestamp']}):** {user_msg['content'][:100]}...")
                with st.expander("View Full Response"):
                    st.markdown(assistant_msg['content'])
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built with ❤️ by SitaRaman | Powered by OpenRouter AI</p>
    <p style='font-size: 0.8rem;'>🌟 Star this project | 📧 Contact for feedback</p>
</div>
""", unsafe_allow_html=True)