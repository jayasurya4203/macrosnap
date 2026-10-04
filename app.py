import os
import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE

# Streamlit Page Setup
st.set_page_config(
    page_title="MacroSnap - AI Nutrition Buddy",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

def get_secret(key: str, default: str = "") -> str:
    """Safely retrieves a configuration key from st.secrets or os.environ."""
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)


# Configuration from Streamlit Secrets or Environment Variables
GEMINI_API_KEY = get_secret("GEMINI_API_KEY", "")
GMAIL_ADDRESS = get_secret("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = get_secret("GMAIL_APP_PASSWORD", "")
MODEL_NAME = get_secret("GEMINI_MODEL", "gemini-2.5-flash")


# Cached Client Initializer
@st.cache_resource
def get_gemini_client(api_key: str):
    """
    Initializes and caches the Google GenAI client to preserve connection across Streamlit reruns.
    """
    return genai.Client(api_key=api_key)


# Validate secrets before proceeding
if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-api-key-here":
    st.title("🥗 MacroSnap")
    st.warning(
        "### ⚠️ Setup Required: Missing Gemini API Key\n\n"
        "To get started with MacroSnap:\n"
        "1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`\n"
        "2. Add your free **GEMINI_API_KEY** from [Google AI Studio](https://aistudio.google.com)\n"
        "3. Add your **GMAIL_ADDRESS** and **GMAIL_APP_PASSWORD** (from [Google App Passwords](https://myaccount.google.com/apppasswords))\n"
        "4. Refresh this page to start tracking your meals!"
    )
    st.stop()
    gemini_client = None
else:
    gemini_client = get_gemini_client(GEMINI_API_KEY)


def render_message(message: dict):
    """Renders a single chat message (text or image) to the Streamlit UI."""
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"], caption="Meal Photo 📸", use_container_width=True)


def add_message(role: str, kind: str, content):
    """Appends a message to the session state history and renders it."""
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])


def ask_gemini(parts) -> str:
    """Sends prompt parts (text + images) to the persistent Gemini chat session."""
    try:
        response = st.session_state.chat.send_message(parts)
        return response.text
    except Exception as error:
        return f"Sorry, something went wrong with the AI analysis: {error}"


def send_email(to_address: str, user_name: str, summary: str) -> tuple[bool, str]:
    """
    Sends the nutrition summary directly to the user's email inbox using Gmail SMTP.
    Requires an App Password (generated via Google Account > Security > App Passwords).
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD or GMAIL_ADDRESS == "your-email@gmail.com":
        return (
            False,
            "Gmail credentials not configured. Please set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .streamlit/secrets.toml",
        )

    clean_password = GMAIL_APP_PASSWORD.replace(" ", "").strip()
    subject = f"🥗 MacroSnap Nutrition Summary for {user_name}"

    body = (
        f"Hi {user_name},\n\n"
        f"Here is your MacroSnap nutrition breakdown and meal summary from your session:\n\n"
        f"========================================\n"
        f"{summary}\n"
        f"========================================\n\n"
        f"Stay consistent and keep fueling your goals! 💪\n\n"
        f"- Your MacroSnap AI Nutrition Buddy\n"
    )

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = f"MacroSnap <{GMAIL_ADDRESS}>"
    message["To"] = to_address

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, clean_password)
            server.send_message(message)
        return True, "Email sent successfully"
    except Exception as error:
        return False, str(error)


# -------------------------------------------------------------
# Sidebar: Information, Tips & Controls
# -------------------------------------------------------------
with st.sidebar:
    st.title("🥗 MacroSnap")
    st.caption("AI Nutrition & Calorie Decoder")
    st.markdown("---")

    if st.session_state.get("onboarded", False):
        st.markdown(f"**Logged in as:** `{st.session_state.get('name')}`")
        st.markdown(f"**Email:** `{st.session_state.get('email')}`")

        st.markdown("---")
        st.subheader("💡 Pro Tips")
        st.markdown(
            "- 📸 **Snap or Upload:** Take a photo of your plate or ingredients.\n"
            "- 💬 **Ask Follow-ups:** Try *'How can I get 25g more protein?'* or *'What is a healthier swap?'*\n"
            "- 📧 **Email Digest:** Click **Send to Email** at any time to get a clean summary sent to your inbox!"
        )

        st.markdown("---")
        if st.button("🔄 Reset Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    else:
        st.info("👋 Welcome! Please enter your details on the right to start your session.")

    st.markdown("---")
    st.caption("Powered by **Google Gemini** & **Streamlit**")


# -------------------------------------------------------------
# Step 1: Onboarding Screen
# -------------------------------------------------------------
if "onboarded" not in st.session_state:
    st.title("🥗 MacroSnap")
    st.caption("Snap it. Track it. Email yourself the results.")

    with st.form("onboarding_form"):
        name = st.text_input("Your Name", placeholder="e.g. Alex")
        email = st.text_input(
            "Your Email Address",
            placeholder="e.g. alex@example.com",
            help="MacroSnap will send your meal and macro summaries to this email.",
        )
        submitted = st.form_submit_button("Let's go 🚀", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip():
            st.warning("Please fill in both your name and email address.")
        elif "@" not in email or "." not in email:
            st.warning("Please enter a valid email address (e.g., student@example.com).")
        else:
            st.session_state.name = name.strip()
            st.session_state.email = email.strip()
            # Initialize conversational session with system persona
            try:
                st.session_state.chat = gemini_client.chats.create(
                    model=MODEL_NAME,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
                )
                st.session_state.messages = []
                st.session_state.onboarded = True
                st.rerun()
            except Exception as e:
                st.error(f"Failed to start Gemini chat session: {e}")
    st.stop()


# -------------------------------------------------------------
# Step 2: Main Chat & Action Screen
# -------------------------------------------------------------
header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("🥗 MacroSnap")

with button_col:
    # Disable button until at least one user-assistant meal exchange exists
    messages_history = st.session_state.get("messages", [])
    send_disabled = len(messages_history) <= 2
    if st.button("📧 Send to Email", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your meals..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

        with st.spinner("Dispatching summary to your inbox..."):
            success, info = send_email(
                to_address=st.session_state.email,
                user_name=st.session_state.name,
                summary=summary,
            )

        if success:
            st.success("Sent! Check your email inbox 📬")
        else:
            st.error(f"Couldn't send email: {info}")

st.caption(f"Logged in as **{st.session_state.name}** • Summaries sent to `{st.session_state.email}`")

# Render previous messages
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

# Unified Chat Input: Accepts text, attached images, or both
user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))

    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        # Implicit prompt if user uploads a photo without typing text
        parts.append("What is this meal? Give me the estimated calories and macros.")

    with st.spinner("Crunching the numbers..."):
        answer = ask_gemini(parts)

    add_message("assistant", "text", answer)
