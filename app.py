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
        
        --bg-primary: #0f2027;
        --bg-secondary: #203a4b;
        --text-primary: #ffffff;
        --accent-1: #6a11cb;
        --accent-2: #2575fc;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --gradient-3: linear-gradient(135deg, #ff6a00 0%, #ee0979 100%);
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
        background: linear-gradient(to right, #6a11cb, #2575fc, #43e97b);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: shine 3s linear infinite;
    }

    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }

    .haiku-card {
        position: relative;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.125);
        overflow: hidden;
        transition: all 0.3s ease;
        transform-style: preserve-3d;
    }

    .haiku-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: var(--gradient-1);
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.3s ease;
    }

    .haiku-card:hover {
        transform: scale(1.03) translateZ(20px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }

    .haiku-card:hover::before {
        transform: scaleX(1);
        transform-origin: left;
    }

    
    .topic-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
        background: var(--gradient-2);
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }

    .topic-badge:hover {
        transform: scale(1.05) rotate(3deg);
    }

    
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button {
        background: var(--gradient-3) !important;
        border-radius: 15px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-4px) rotate(2deg) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

TOPIC_COLORS = [
    "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)",   # Purple to Blue
    "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",   # Green to Cyan
    "linear-gradient(135deg, #ff6a00 0%, #ee0979 100%)",   # Orange to Pink
    "linear-gradient(135deg, #8a2387 0%, #e94057 100%)",   # Deep Purple to Red
    "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"    # Teal to Green
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
            <h1 class="animated-title" style="font-size: 3.5rem; letter-spacing: -2px;">
                🍃Bashobot: Haiku Forge 🍃
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