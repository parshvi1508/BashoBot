import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client
from groq import Groq
import random

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.markdown("""
<style>
    :root {
        --bg-primary: #121212;
        --bg-secondary: #1e1e2a;
        --text-primary: #e0e0e0;
        --accent-primary: #6a5acd;
        --accent-secondary: #4169e1;
        --accent-tertiary: #20b2aa;

        --gradient-primary: linear-gradient(135deg, #8a2be2, #4169e1);
        --gradient-secondary: linear-gradient(135deg, #20b2aa, #2e8b57);
        --gradient-accent: linear-gradient(135deg, #ff6b6b, #feca57);
    }

    body {
        
        color: var(--text-primary);
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, 
        rgba(15, 32, 39, 0.9), 
        rgba(32, 58, 67, 0.9), 
        rgba(44, 83, 100, 0.9)
    );
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    }

    .animated-title {
        background: var(--gradient-primary);
        background-size: 300% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: shine 4s ease infinite;
        text-shadow: 0 4px 15px rgba(106, 90, 205, 0.4);
    }

    @keyframes shine {
        0% { background-position: 0% center; }
        50% { background-position: 200% center; }
        100% { background-position: 0% center; }
    }

    .haiku-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.2),
            0 5px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        position: relative;
        overflow: hidden;
    }

    .haiku-card:hover {
        transform: scale(1.05) translateY(-10px);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.3),
            0 10px 20px rgba(0, 0, 0, 0.2);
    }

    .topic-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        background: var(--gradient-secondary);
        color: white;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }

    .topic-badge:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 6px 12px rgba(32, 178, 170, 0.3);
    }

    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid var(--accent-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: var(--accent-secondary) !important;
        box-shadow: 0 0 15px rgba(65, 105, 225, 0.3) !important;
    }

    .stButton>button {
        background: var(--gradient-accent) !important;
        border-radius: 25px !important;
        color: white !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3) !important;
    }

    @media (max-width: 768px) {
        .animated-title {
            font-size: 2.5rem !important;
        }
        
        .haiku-card {
            margin-bottom: 15px !important;
        }
    }
    @media (max-width: 768px) {
    .animated-title {
        font-size: 2.5rem !important;
    }
    
    .haiku-card {
        margin-bottom: 15px !important;
    }
}
</style>
""", unsafe_allow_html=True)

TOPIC_COLORS = [
    "linear-gradient(135deg, #8a2be2 0%, #4169e1 100%)",   # Blueviolet to Royal Blue
    "linear-gradient(135deg, #20b2aa 0%, #2e8b57 100%)",   # Light Sea Green to Sea Green
    "linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)",   # Soft Red to Bright Yellow
    "linear-gradient(135deg, #8e44ad 0%, #e74c3c 100%)",   # Deep Purple to Vibrant Red
    "linear-gradient(135deg, #3498db 0%, #2ecc71 100%)"    # Bright Blue to Emerald Green

]

def generate_haiku(topic):
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """Create a traditional haiku following 5-7-5 syllable structure. 
                    Focus on imagery, nature, and emotion."""
                },
                {
                    "role": "user", 
                    "content": f"Create a haiku about {topic}."
                }
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Haiku generation failed: {e}")
        return None

def main():
    st.markdown('''
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 class="animated-title" style="font-size: 3rem; letter-spacing: -2px;">
                🍃BashoBot: Haiku Forge🍃
            </h1>
            <p style="color: rgba(255,255,255,0.7); margin-top: -10px; font-size: 1.2rem;">
                Weave Poetry with AI Whispers
            </p>
        </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns([3,1])
    with col1:
        topic = st.text_input(
            "Enter a topic", 
            placeholder="Whisper your inspiration...",
            label_visibility="collapsed"
        )

    generate_button = st.button("✨ Conjure Haiku", key="generate")

    if generate_button and topic:
        with st.spinner('Weaving poetic threads...'):
            haiku = generate_haiku(topic)
        
        if haiku:
            topic_color = random.choice(TOPIC_COLORS)
            
            try:
                data = {"topic": topic, "haiku": haiku}
                supabase.table("haiku_table").insert(data).execute()
                
                st.markdown(f'''
                <div class="haiku-card" style="padding: 20px; margin-bottom: 20px;">
                    <div style="text-align: center; margin-bottom: 15px;">
                        <span class="topic-badge" style="background: {topic_color};">
                            🌿 {topic.capitalize()} 🌿
                        </span>
                    </div>
                    <div style="color: white; text-align: center; font-family: 'Georgia', serif; font-style: italic;">
                        {haiku}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.success("Haiku captured in the digital scroll! 📜")
            
            except Exception as e:
                st.error(f"Failed to save haiku: {e}")

    st.markdown('<h2 style="text-align: center; margin-top: 30px; color: white;">Haiku Archives</h2>', unsafe_allow_html=True)

    try:
        response = supabase.table("haiku_table").select("*").execute()
        
        if response.data:
            cols = st.columns(3)
            for i, row in enumerate(response.data):
                topic_color = TOPIC_COLORS[i % len(TOPIC_COLORS)]
                
                with cols[i % 3]:
                    st.markdown(f'''
                    <div class="haiku-card" style="margin-bottom: 20px; padding: 15px;">
                        <div style="text-align: center; margin-bottom: 10px;">
                            <span class="topic-badge" style="background: {topic_color};">
                                {row.get('topic').capitalize()}
                            </span>
                        </div>
                        <div style="color: white; text-align: center; font-family: 'Georgia', serif; font-style: italic;">
                            {row.get('haiku')}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="haiku-card" style="text-align: center; padding: 20px; color: white;">
                No haiku echoes yet... Be the first poet 📜
            </div>
            ''', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Archive retrieval failed: {e}")

if __name__ == "__main__":
    main()