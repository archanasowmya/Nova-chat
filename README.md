# ✨ Aura AI

> A personalized, multi-role AI conversational companion designed with an Apple-inspired glassmorphism interface. Powered by Python, Flask, and the Google Gemini API.

---

## 🎯 What Does This Project Actually Do?

Standard AI interfaces usually speak in a single, neutral tone and require technical prompting to get specific kinds of responses. **Aura AI** turns the AI into a customizable personal companion that adapts its tone, vocabulary, and expertise to fit whatever role you need in real time.

### 1. Shifts Tone & Personality on the Fly
Instead of getting generic AI answers, you can switch between dedicated personas instantly using a dropdown menu:
* **👩 Mother:** Gives warm, loving advice, family support, and comforting recipe suggestions.
* **👨‍🏫 Teacher:** Explains tough academic or technical concepts using simple analogies and beginner-friendly examples.
* **😂 Comedian:** Keeps things lighthearted, delivering answers with wit, jokes, and humor.
* **🚀 Entrepreneur:** Offers direct, startup-focused advice, business strategies, and motivational feedback.
* **🏥 Doctor:** Breaks down health and wellness concepts into clear, easy-to-understand explanations.
* **👯 Friend:** Chats casually, empathetically, and supportively like a close peer.

### 2. Speaks Multiple Languages
Select your language of choice (English, Spanish, French, German, or Hindi), and the agent automatically adapts both its vocabulary and cultural phrasing without needing you to instruct it manually.

### 3. Talks Back Out Loud
When voice is switched **ON**, Aura AI uses speech synthesis to read responses aloud right through your browser, creating a hands-free conversational experience.

### 4. Personalizes Your Experience
Enter your name, and the agent remembers who it is speaking to. It stores your name, selected personality, and language settings directly in your browser's local storage so you don't have to reconfigure them every time you reload.

### 5. Saves & Exports Your Conversations
Keep track of helpful advice, notes, or brainstorming sessions by saving your chat history to a cleanly formatted JSON or text file with a single click.

---

## 🌟 Key Features

* **🍎 Apple-Inspired Glassmorphism UI:** Translucent frosted-glass aesthetic featuring smooth animations, soft gradients, and mobile-friendly layouts.
* **🎭 30+ Backend Personalities:** A comprehensive dictionary of pre-tuned personas ranging from creative writers to software architects.
* **🗣️ Browser-Native Voice Playback:** Instant audio responses using the Web Speech API without server-side lag.
* **⚡ Instant Fast-Response Engine:** Connected to Google Gemini models via the latest Google GenAI SDK for fast, context-aware answers.
* **💾 One-Click Chat Export:** Save and download full conversation logs directly to your device.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Gunicorn
* **AI Model:** Google Gemini API (`google-genai` SDK)
* **Frontend:** Vanilla HTML5, Modern CSS3 (Backdrop Blur, CSS Grid, Flexbox), JavaScript (Fetch API & Web Speech API)
* **Storage:** Client-side `localStorage` for user preferences and downloadable JSON/TXT archives

---

## 📂 Project Structure

```text
aura-ai/
├── templates/
│   └── index_apple_style.html  # Glassmorphism frontend interface & chat logic
├── app.py                      # Flask API, persona instructions & Gemini SDK integration
├── requirements.txt            # Python dependencies (Flask, google-genai, gunicorn, etc.)
├── .gitignore                  # Keeps sensitive keys and virtual environments off GitHub
└── README.md                   # Project documentation
