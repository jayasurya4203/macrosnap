# 🥗 MacroSnap — AI Nutrition & Macro Decoder

> **Snap it. Track it. Email yourself the results.**\
> An AI-powered vision and chat application built with **Streamlit**, **Google Gemini (Vision + Chat)**, and **Gmail SMTP**.

---

## 📖 Overview

**MacroSnap** acts as your instant nutrition buddy. Simply type what you ate or snap/upload a photo of your meal:
- 🥗 **Instant Recognition:** Uses Google Gemini Multimodal Vision to recognize meals and portion sizes.
- ⚡ **Calorie & Macro Breakdown:** Estimates calories and macronutrients (protein, carbs, fat) in seconds.
- 💬 **Conversational Memory:** Preserves multi-turn chat context for follow-up questions (*"How can I add 20g more protein?"* or *"What are healthier swaps?"*).
- 📧 **One-Click Email Digest:** With one click of the **Send to Email** button, MacroSnap compiles a clean, running summary of all meals tracked and delivers it straight to your inbox via Gmail SMTP.

---

## 🏗️ Project Structure

```text
macrosnap/
├── app.py                      # Main Streamlit application with chat & email dispatch
├── prompts.py                  # Persona definitions, system guardrails & templates
├── requirements.txt            # Python dependencies
├── .gitignore                  # Keeps secrets and virtual environments out of Git
├── README.md                   # Project documentation & setup instructions
└── .streamlit/
    └── secrets.toml.example    # Configuration template for API keys & credentials
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.9+ installed
- A free **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com)
- A **Gmail Account** with an [App Password](https://myaccount.google.com/apppasswords)

### 2. Clone or Navigate to the Project
```bash
cd macrosnap
```

### 3. Create and Activate Virtual Environment
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If script execution is disabled, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*
- **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Secrets
1. Copy the example secrets file:
   - **macOS / Linux:**
     ```bash
     cp .streamlit/secrets.toml.example .streamlit/secrets.toml
     ```
   - **Windows:**
     ```powershell
     Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
     ```
2. Open `.streamlit/secrets.toml` in your editor and fill in your values:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   GMAIL_ADDRESS = "yourname@gmail.com"
   GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"
   GEMINI_MODEL = "gemini-2.5-flash"
   ```

> 🔐 **How to get a Gmail App Password:**
> 1. Turn ON **2-Step Verification** in [Google Account Security](https://myaccount.google.com/security).
> 2. Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
> 3. Enter an app name (e.g. `MacroSnap`) and click **Create**.
> 4. Copy the generated 16-character code into `GMAIL_APP_PASSWORD`.

### 6. Run the Application Locally
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

1. **Push your repository to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit of MacroSnap"
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
   > ⚠️ **Verification:** Verify that `.streamlit/secrets.toml` was **not** committed (`.gitignore` protects this).

2. **Deploy on Streamlit:**
   - Head over to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
   - Click **New app**, select your repository, branch (`main`), and set the main file path to `app.py`.
   - Click **Advanced settings** -> **Secrets**.
   - Copy and paste the contents of your local `.streamlit/secrets.toml` (with your real keys).
   - Click **Deploy!**

---

## 🎯 Evaluation Checklist

- [x] **Functionality (40%):** Onboarding, multimodal meal analysis (photo + text), chat memory, and email digest delivery.
- [x] **Prompt Design (20%):** Scoped system prompt in `prompts.py` that keeps the AI strictly focused on nutrition, meals, and fitness while declining off-topic prompts.
- [x] **Code Quality (20%):** Separation of concerns (`prompts.py` vs `app.py`), cached clients with `@st.cache_resource`, safe UTF-8 MIME handling, and clean error messages.
- [x] **Creativity & Polish (20%):** Responsive layout, clear statuses, session reset button, informative sidebar with pro tips, and zero-leak secrets management.

---

## 📮 Submission Details

- **Submission Form:** [CCBP AI Vision Chatbot Final Project Submission](https://forms.ccbp.in/ai-vision-chatbot-last-project-submission)
- **Deadline:** 4th October, 11:59 PM
