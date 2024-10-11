import streamlit as st
import requests
import json
from datetime import datetime
import random
import time
import streamlit.components.v1 as components

# ============================
# Configuration and Setup
# ============================

# Set page configuration
st.set_page_config(page_title="🙏 AI-Powered Multi-Religious Guidance 🙏", layout="wide")

# Hide Streamlit's default style elements for a cleaner look
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define CSS for themes, animations, and chat bubbles
theme_css = """
<style>
/* Theme Styles */
body.light-theme {
    background-color: #FFFFFF;
    color: #000000;
}
.sidebar.light-theme {
    background-color: #F0F0F0;
    color: #000000;
}

body.dark-theme {
    background-color: #2C2C2C;
    color: #FFFFFF;
}
.sidebar.dark-theme {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

body.blue-theme {
    background-color: #E6F0FF;
    color: #003366;
}
.sidebar.blue-theme {
    background-color: #CCE0FF;
    color: #003366;
}

body.green-theme {
    background-color: #E6FFE6;
    color: #006600;
}
.sidebar.green-theme {
    background-color: #CCFFCC;
    color: #006600;
}

/* Chat Bubble Styles */
.chat-container {
    display: flex;
    flex-direction: column;
}

.user-bubble {
    align-self: flex-end;
    background-color: #DCF8C6;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    max-width: 70%;
    animation: fadeIn 0.5s ease-in-out;
}

.assistant-bubble {
    align-self: flex-start;
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 10px;
    margin: 5px;
    max-width: 70%;
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Invisible Audio Player */
#audio_player {
    display: none;
}

/* Additional Animations */
.message {
    animation: slideIn 0.5s ease-in-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Button Styles */
.stButton > button {
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #45a049;
}
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# JavaScript for setting body and sidebar classes based on theme
theme_js = """
<script>
function setTheme(theme) {
    document.body.className = theme + '-theme';
    document.querySelector('.sidebar').className = theme + '-theme';
}
</script>
"""

st.markdown(theme_js, unsafe_allow_html=True)

# Function to set the theme
def apply_theme(theme):
    st.session_state.theme = theme
    st.markdown(f"<script>setTheme('{theme}');</script>", unsafe_allow_html=True)

# ============================
# Sidebar - User Preferences
# ============================

st.sidebar.header("Setup Your Preferences")

# Religion Selection
religions = [
    "Christianity", "Islam", "Hinduism", "Buddhism", "Judaism",
    "Sikhism", "Jainism", "Baha'i", "Shinto", "Taoism"
]
religion = st.sidebar.selectbox("Select Your Religion", religions)

# Language Selection
languages = [
    "English", "Spanish", "French", "German", "Chinese",
    "Hindi", "Arabic", "Portuguese", "Russian", "Japanese"
]
language = st.sidebar.selectbox("Select Language", languages)

# Theme Selection
themes = ["Light", "Dark", "Blue", "Green"]
theme = st.sidebar.selectbox("Select Theme", themes)

# Apply the selected theme
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
apply_theme(theme.lower())

# Initialize session state for messages and user profile
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {"username": "Guest"}

# ============================
# API Keys and Endpoints
# ============================

# Retrieve the API key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# Define the Chat Completion API endpoint
API_URL = "https://api.aimlapi.com/chat/completions"

# Define the Background Music API endpoint (Assuming a hypothetical API)
MUSIC_API_URL = "https://api.religiousmusicapi.com/get_music"

# Define additional API endpoints
BIBLE_API_URL = "https://beta.ourmanna.com/api/v1/get/?format=json&order=random"  # For daily verses
NEWS_API_URL = "https://newsapi.org/v2/everything"  # Requires API key
TRANSLATION_API_URL = "https://libretranslate.de/translate"  # Free translation API

# ============================
# Helper Functions
# ============================

# Function to call the custom Chat Completion API
def get_api_response(model, messages, max_tokens=500, temperature=0.7, top_p=1.0, frequency_penalty=0.0, stream=False):
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "stream": stream
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        
        # Adjust based on your API's response structure
        ai_message = data.get('choices', [])[0].get('message', {}).get('content', '').strip()
        return ai_message
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to get background music URL based on religion
def get_background_music(religion):
    # Example: Fetch music from a hypothetical API
    params = {"religion": religion}
    try:
        response = requests.get(MUSIC_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        music_url = data.get("music_url")
        return music_url
    except:
        # Fallback to predefined music URLs if API fails
        predefined_music = {
            "Christianity": "https://example.com/christian_music.mp3",
            "Islam": "https://example.com/islam_music.mp3",
            "Hinduism": "https://example.com/hindu_music.mp3",
            "Buddhism": "https://example.com/buddhism_music.mp3",
            "Judaism": "https://example.com/judaism_music.mp3",
            "Sikhism": "https://example.com/sikhism_music.mp3",
            "Jainism": "https://example.com/jainism_music.mp3",
            "Baha'i": "https://example.com/bahai_music.mp3",
            "Shinto": "https://example.com/shinto_music.mp3",
            "Taoism": "https://example.com/taoism_music.mp3"
        }
        return predefined_music.get(religion, "")

# Function to get daily verse or scripture
def get_daily_verse(religion, language):
    if religion == "Christianity":
        # Using OurManna API for random Bible verses
        try:
            response = requests.get(BIBLE_API_URL)
            data = response.json()
            verse = data.get("verse", {}).get("details", {}).get("text", "Stay blessed and have a peaceful day.")
            return verse
        except:
            return "Stay blessed and have a peaceful day."
    else:
        # Placeholder for other religions
        daily_verses = {
            "Islam": "Quran 2:255 - Allah! There is no deity except Him...",
            "Hinduism": "Bhagavad Gita 2:47 - You have the right to perform your prescribed duties...",
            "Buddhism": "Dhammapada 1: Mind precedes all...",
            "Judaism": "Psalm 23: The Lord is my shepherd...",
            "Sikhism": "Japji Sahib - Meditation on God's name...",
            "Jainism": "Acharanga Sutra - Non-violence is the highest duty...",
            "Baha'i": "The Hidden Words - By Him that loveth best...",
            "Shinto": "Kojiki - Kami are revered...",
            "Taoism": "Tao Te Ching 1 - The Tao that can be told..."
        }
        return daily_verses.get(religion, "Stay blessed and have a peaceful day.")

# Function to get inspirational quotes
def get_inspirational_quote(religion):
    # Placeholder for actual implementation
    quotes = {
        "Christianity": "Faith is taking the first step even when you don't see the whole staircase.",
        "Islam": "The best among you are those who have the best manners and character.",
        "Hinduism": "Where there is Dharma, there is victory.",
        "Buddhism": "Peace comes from within. Do not seek it without.",
        "Judaism": "Whoever saves one life, it is as if they have saved the entire world.",
        "Sikhism": "Live without regret, love without limits.",
        "Jainism": "A man is great by deeds, not by birth.",
        "Baha'i": "Be generous in prosperity, and thankful in adversity.",
        "Shinto": "Harmony with nature brings peace.",
        "Taoism": "Nature does not hurry, yet everything is accomplished."
    }
    return quotes.get(religion, "Inspirational quote here.")

# Function to get prayer times (Simplified - based on fixed times)
def get_prayer_times(religion):
    prayer_times = {
        "Islam": ["Fajr: 5:00 AM", "Dhuhr: 12:30 PM", "Asr: 3:45 PM", "Maghrib: 6:15 PM", "Isha: 7:30 PM"],
        # Add other religions' prayer times if applicable
    }
    return prayer_times.get(religion, [])

# Function to get upcoming religious events (Simplified)
def get_upcoming_events(religion):
    events = {
        "Christianity": ["Easter - April 9, 2024", "Christmas - December 25, 2024"],
        "Islam": ["Ramadan - Starts March 10, 2024", "Eid al-Fitr - April 9, 2024"],
        "Hinduism": ["Diwali - November 1, 2024", "Holi - March 25, 2024"],
        "Buddhism": ["Vesak - May 23, 2024"],
        "Judaism": ["Yom Kippur - October 11, 2024", "Hanukkah - December 25, 2024"],
        # Add more as needed
    }
    return events.get(religion, [])

# Function to get donation links (Simplified)
def get_donation_links(religion):
    donation_links = {
        "Christianity": "https://www.christiancharities.org/donate",
        "Islam": "https://www.islamiccharities.org/donate",
        "Hinduism": "https://www.hinducharities.org/donate",
        "Buddhism": "https://www.buddhistcharities.org/donate",
        "Judaism": "https://www.jewishcharities.org/donate",
        "Sikhism": "https://www.sikhcharities.org/donate",
        "Jainism": "https://www.jaincharities.org/donate",
        "Baha'i": "https://www.bahaicharities.org/donate",
        "Shinto": "https://www.shintocharities.org/donate",
        "Taoism": "https://www.taaocharities.org/donate"
    }
    return donation_links.get(religion, "")

# Function to get inspirational videos (Using YouTube API - requires API key)
def get_inspirational_videos(religion):
    # Placeholder: Using YouTube search for religious inspirational videos
    # You need a YouTube Data API key and handle quotas
    # For simplicity, returning static video links
    videos = {
        "Christianity": "https://www.youtube.com/embed/1i3Z3vZJh0Y",
        "Islam": "https://www.youtube.com/embed/YOUR_ISLAM_VIDEO_ID",
        "Hinduism": "https://www.youtube.com/embed/YOUR_HINDUISM_VIDEO_ID",
        "Buddhism": "https://www.youtube.com/embed/YOUR_BUDDHISM_VIDEO_ID",
        "Judaism": "https://www.youtube.com/embed/YOUR_JUDAISM_VIDEO_ID",
        "Sikhism": "https://www.youtube.com/embed/YOUR_SIKHISM_VIDEO_ID",
        "Jainism": "https://www.youtube.com/embed/YOUR_JAINISM_VIDEO_ID",
        "Baha'i": "https://www.youtube.com/embed/YOUR_BAHAI_VIDEO_ID",
        "Shinto": "https://www.youtube.com/embed/YOUR_SHINTO_VIDEO_ID",
        "Taoism": "https://www.youtube.com/embed/YOUR_TAOISM_VIDEO_ID"
    }
    return videos.get(religion, "")

# Function to translate text using LibreTranslate API
def translate_text(text, target_language):
    payload = {
        "q": text,
        "source": "en",
        "target": target_language.lower(),
        "format": "text"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(TRANSLATION_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        translated_text = data.get("translatedText", text)
        return translated_text
    except:
        return text  # Fallback to original text if translation fails

# Function to get religious news using NewsAPI
def get_religious_news(religion):
    # Note: You need to obtain a NewsAPI key and add it to Streamlit secrets
    NEWS_API_KEY = st.secrets.get("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return ["News API key not found."]
    params = {
        "q": religion,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "relevancy"
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        news = [f"[{article['title']}]({article['url']})" for article in articles]
        return news if news else ["No recent news found."]
    except:
        return ["Unable to fetch news at this time."]

# Function to get meditation guides (Placeholder)
def get_meditation_guide(religion):
    guides = {
        "Christianity": "Focus on the presence of God and reflect on His blessings.",
        "Islam": "Concentrate on the remembrance of Allah and your daily prayers.",
        "Hinduism": "Engage in deep breathing and focus on the divine within.",
        "Buddhism": "Practice mindfulness and observe your thoughts without judgment.",
        "Judaism": "Reflect on your daily deeds and seek inner peace through prayer.",
        "Sikhism": "Meditate on the divine name and cultivate inner harmony.",
        "Jainism": "Practice deep breathing and focus on non-violence and truth.",
        "Baha'i": "Contemplate the unity of humanity and the presence of God.",
        "Shinto": "Connect with nature and honor the spirits around you.",
        "Taoism": "Embrace the flow of the Tao and maintain inner balance."
    }
    return guides.get(religion, "Focus on your breath and find inner peace.")

# Function to get community forum links
def get_community_forums(religion):
    forums = {
        "Christianity": "https://www.reddit.com/r/Christianity/",
        "Islam": "https://www.reddit.com/r/islam/",
        "Hinduism": "https://www.reddit.com/r/hinduism/",
        "Buddhism": "https://www.reddit.com/r/Buddhism/",
        "Judaism": "https://www.reddit.com/r/Judaism/",
        "Sikhism": "https://www.reddit.com/r/sikh/",
        "Jainism": "https://www.reddit.com/r/Jainism/",
        "Baha'i": "https://www.reddit.com/r/Bahai/",
        "Shinto": "https://www.reddit.com/r/shinto/",
        "Taoism": "https://www.reddit.com/r/taoism/"
    }
    return forums.get(religion, "")

# ============================
# Prayer of the Day Section
# ============================

# Function to get Prayer of the Day
def get_prayer_of_the_day(religion, language):
    system_prompt = f"You are a respectful assistant providing detailed prayers for {religion} in {language}."
    user_prompt = "Please provide the Prayer of the Day with a relevant quotation."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    prayer = get_api_response(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
        stream=False
    )
    # Translate if necessary
    if language != "English":
        prayer = translate_text(prayer, language)
    return prayer

# ============================
# Meditation Guide Section
# ============================

# Function to display meditation guide
def display_meditation_guide():
    guide = get_meditation_guide(religion)
    st.markdown("### 🧘‍♂️ Guided Meditation 🧘‍♀️")
    st.write(guide)

# ============================
# Main Content
# ============================

st.title("🙏 AI-Powered Multi-Religious Guidance 🙏")
st.markdown("""
Welcome to the AI-Powered Multi-Religious Guidance platform. Select your religion and language to receive personalized prayers, scriptures, inspirational content, and more.
""")

# Display Prayer of the Day Button
if st.button("Show Prayer of the Day"):
    with st.spinner('Generating Prayer of the Day...'):
        prayer = get_prayer_of_the_day(religion, language)
    st.markdown("### 🕊️ Prayer of the Day 🕊️")
    st.write(prayer)

st.markdown("---")

# Chat Interface
st.markdown("### 💬 Ask Your Religious Questions 💬")

# Function to handle user input and AI response
def handle_user_input(user_input):
    if user_input.strip() == "":
        return
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    system_prompt = f"You are a knowledgeable and respectful assistant for {religion} followers. Answer the following question based on {religion} teachings in {language}."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    with st.spinner('Generating response...'):
        ai_response = get_api_response(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            stream=False
        )
    
    # Translate if necessary
    if language != "English":
        ai_response = translate_text(ai_response, language)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# User Input with Emoji Support and Voice Input
user_input = st.text_input("You:", key="input", placeholder="Type your message here... 😊")

# Handle user input on Send button click
if st.button("Send"):
    handle_user_input(user_input)

# Display the conversation with animated chat bubbles
st.markdown("### Conversation")
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"<div class='chat-container'><div class='user-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='assistant-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)

# ============================
# Additional Features Section
# ============================

st.markdown("---")
st.markdown("## Additional Features")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    # Meditation Guides
    display_meditation_guide()

with col2:
    # Religious News Feed
    st.markdown("### 📰 Religious News 📰")
    news = get_religious_news(religion)
    for item in news:
        st.markdown(f"- {item}")

with col3:
    # Inspirational Videos
    st.markdown("### 📹 Inspirational Videos 📹")
    video_url = get_inspirational_videos(religion)
    if video_url:
        st.video(video_url)
    else:
        st.write("No videos available.")

with col4:
    # Community Forums
    st.markdown("### 🗣️ Community Forums 🗣️")
    forum_link = get_community_forums(religion)
    if forum_link:
        st.markdown(f"[Join the Discussion]({forum_link})")
    else:
        st.write("Community forums not available.")

with col5:
    # Language Translation Toggle
    st.markdown("### 🌐 Language Translation 🌐")
    translate = st.checkbox("Enable Translation")
    if translate and language != "English":
        st.markdown(f"**Translations are enabled. Responses will be in {language}.**")
    elif translate:
        st.markdown("**Translations are enabled but already in English.**")
    else:
        st.markdown("**Translations are disabled. Responses will be in English.**")

# ============================
# Religious Events Calendar
# ============================

st.markdown("### 📅 Upcoming Religious Events 📅")
events = get_upcoming_events(religion)
if events:
    for event in events:
        st.write(f"- {event}")
else:
    st.write("No upcoming events available.")

# ============================
# Donation Links
# ============================

st.markdown("### 💖 Support Us 💖")
donation_link = get_donation_links(religion)
if donation_link:
    st.markdown(f"[Donate Here]({donation_link})")
else:
    st.write("Donation links are not available for the selected religion.")

# ============================
# Religious News Feed
# ============================

# (Already implemented above)

# ============================
# Background Music Integration (Invisible)
# ============================

music_url = get_background_music(religion)
if music_url:
    st.markdown(f"""
    <audio autoplay loop>
        <source src="{music_url}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)
else:
    st.write("🎶 No background music available for the selected religion.")

# ============================
# Footer with Animation
# ============================

footer_css = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #333333;
    text-align: center;
    animation: fadeIn 2s;
}
</style>
"""

footer_html = """
<div class="footer">
    &copy; 2024 AI-Powered Multi-Religious Guidance. All rights reserved.
</div>
"""

st.markdown(footer_css + footer_html, unsafe_allow_html=True)

# ============================
# Voice Interaction (Optional)
# ============================

# Note: Streamlit doesn't natively support voice input/output.
# This can be implemented using Streamlit Components or external libraries.
# Here's a placeholder for future implementation.

st.markdown("---")
st.markdown("## 🔊 Voice Interaction 🔊")
st.write("*Voice interaction feature is under development. Stay tuned!*")

# ============================
# User Profiles (Optional)
# ============================

# Placeholder for user profile management
st.markdown("### 👤 User Profile 👤")
username = st.text_input("Enter your name:", value=st.session_state.user_profile.get("username", "Guest"))

if st.button("Save Profile"):
    st.session_state.user_profile["username"] = username
    st.success("Profile saved!")

st.write(f"**Welcome, {st.session_state.user_profile['username']}!**")

# ============================
# Donation Links (Already Implemented)
# ============================

# Already implemented above

# ============================
# Closing Remarks
# ============================

st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    &copy; 2024 AI-Powered Multi-Religious Guidance. All rights reserved.
</div>
""", unsafe_allow_html=True)
