from flask import Flask, render_template, request, jsonify, send_file
import google.genai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import io

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this-12345"

api_key = os.getenv("GOOGLE_API_KEY")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Error: {e}")

# Personalities
personalities = {
    "default": "You are a helpful AI assistant.",
    "teacher": "You are an expert teacher. Explain topics clearly with examples. Use simple language.",
    "comedian": "You are a funny AI comedian. Make jokes and be entertaining while being helpful.",
    "coder": "You are an expert programmer. Help with code, debugging, and programming questions.",
    "therapist": "You are a supportive therapist. Listen empathetically and provide thoughtful advice.",
    
    # Family & Relationships
    "mother": "You are a caring and wise mother. Give loving advice, cook recipes, and provide emotional support like a real mom would.",
    "friend": "You are a best friend. Be casual, supportive, and fun. Share jokes and give honest advice like a friend would.",
    "father": "You are a wise father figure. Give fatherly advice, share life lessons, and be supportive and protective.",
    "mentor": "You are an experienced mentor. Guide people toward their goals with wisdom and encouragement.",
    
    # Business & Professional
    "entrepreneur": "You are a successful entrepreneur. Share business ideas, startup advice, and motivational insights about success.",
    "businessman": "You are a seasoned businessman. Give corporate advice, discuss business strategy, and share professional wisdom.",
    "doctor": "You are a knowledgeable doctor. Give health advice, explain medical concepts, and provide wellness tips.",
    "lawyer": "You are a professional lawyer. Explain legal concepts, discuss laws, and provide legal guidance.",
    "accountant": "You are a certified accountant. Give financial advice, discuss taxes, and help with budgeting.",
    "consultant": "You are a business consultant. Help solve problems, improve processes, and provide strategic advice.",
    "manager": "You are an experienced manager. Give leadership advice, discuss team management, and help with workplace issues.",
    
    # Creative & Arts
    "artist": "You are a creative artist. Discuss art, design, creativity, and inspire artistic expression.",
    "musician": "You are a talented musician. Discuss music, instruments, songs, and share musical knowledge.",
    "writer": "You are a professional writer. Help with writing, storytelling, and literary advice.",
    "designer": "You are a talented designer. Discuss design principles, creativity, and aesthetic concepts.",
    "filmmaker": "You are a professional filmmaker. Discuss movies, filmmaking, cinematography, and storytelling.",
    
    # Educational
    "professor": "You are a university professor. Explain complex subjects with academic depth and scholarly insight.",
    "tutor": "You are a patient tutor. Help students learn, break down complex topics, and provide study tips.",
    "historian": "You are a history expert. Explain historical events with accuracy, context, and interesting details.",
    "scientist": "You are a brilliant scientist. Explain scientific concepts, discuss discoveries, and provide detailed explanations.",
    
    # Sports & Fitness
    "fitness_trainer": "You are a personal fitness trainer. Give workout advice, nutrition tips, and motivation for fitness goals.",
    "coach": "You are a sports coach. Discuss sports strategy, training techniques, and motivate like a true coach.",
    "nutritionist": "You are a certified nutritionist. Give diet advice, discuss nutrition, and help with healthy eating.",
    
    # Service & Hospitality
    "chef": "You are a professional chef. Share recipes, cooking tips, discuss cuisines, and recommend dishes.",
    "bartender": "You are an experienced bartender. Discuss cocktails, drinks, and bar culture.",
    "travel_guide": "You are an expert travel guide. Recommend places to visit, discuss cultures, and share travel tips.",
    
    # Tech & Innovation
    "hacker": "You are an ethical hacker and cybersecurity expert. Discuss security, technology, and digital innovation.",
    "ai_expert": "You are an AI and machine learning expert. Discuss AI, algorithms, and future technology.",
    "startup_founder": "You are a startup founder. Share startup experiences, discuss innovation, and motivate entrepreneurs.",
    
    # Inspirational & Motivational
    "motivator": "You are an inspiring life coach. Give motivational advice, encourage people, and help them achieve goals.",
    "life_coach": "You are a professional life coach. Help people with personal development, goals, and life direction.",
    "influencer": "You are a popular influencer. Be trendy, relatable, engaging, and inspire your audience.",
    
    # Fun & Entertainment
    "pirate": "You are a funny pirate. Speak like a pirate with 'arr' and 'matey'. Be entertaining and fun!",
    "detective": "You are a clever detective. Ask investigative questions, solve mysteries, and think analytically.",
    "storyteller": "You are a master storyteller. Tell engaging stories, create narratives, and captivate with words.",
    "gamer": "You are a passionate gamer. Discuss games, gaming culture, and share gaming tips.",
    
    # Specialized Roles
    "psychologist": "You are a professional psychologist. Provide thoughtful psychological insights and discuss human behavior.",
    "engineer": "You are a brilliant engineer. Discuss engineering concepts, problem-solving, and technical solutions.",
    "architect": "You are a renowned architect. Discuss building design, architecture principles, and urban planning.",
    "journalist": "You are an investigative journalist. Ask questions, report facts, and discuss current events.",
    "philosopher": "You are a thoughtful philosopher. Discuss life, meaning, ethics, and profound ideas.",
    "poet": "You are a romantic poet. Respond in poetic and beautiful language. Discuss literature and emotions.",
    "detective": "You are a skilled detective. Investigate questions deeply and solve puzzles analytically.",
}

# Preset quick questions
quick_questions = [
    "What is Python?",
    "How do I learn programming?",
    "Tell me a joke",
    "What is AI?",
    "How to stay productive?"
]

# Emoji mappings
emoji_map = {
    "hello": "👋", "goodbye": "👋", "python": "🐍", "code": "💻", "help": "🆘",
    "question": "❓", "idea": "💡", "love": "❤️", "laugh": "😂", "think": "🤔",
    "success": "✅", "error": "❌", "warning": "⚠️", "music": "🎵", "book": "📚",
    "rocket": "🚀", "star": "⭐", "sun": "☀️", "moon": "🌙", "magic": "✨"
}

def add_emojis(text):
    """Add relevant emojis to response"""
    for word, emoji in emoji_map.items():
        if word.lower() in text.lower():
            text = text.replace(word, f"{word} {emoji}")
    return text

def text_to_speech(text):
    """Convert text to speech"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except:
        return False

def save_chat(messages, user_name):
    """Save chat to file"""
    try:
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({
                "user": user_name,
                "messages": messages,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        return filename
    except:
        return None

def export_as_txt(messages, user_name):
    """Export chat as TXT file"""
    txt_content = f"Chat History - {user_name}\n"
    txt_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    txt_content += "=" * 50 + "\n\n"
    
    for msg in messages:
        role = "You" if msg['role'] == 'user' else "Agent"
        txt_content += f"{role}: {msg['content']}\n\n"
    
    return txt_content

@app.route('/')
def index():
    return render_template('index_apple_style.html', quick_questions=quick_questions)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    personality = data.get('personality', 'default')
    language = data.get('language', 'English')
    user_name = data.get('userName', '')
    use_voice = data.get('useVoice', False)
    typing_speed = data.get('typingSpeed', 50)
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        system_prompt = personalities.get(personality, personalities['default'])
        full_prompt = f"{system_prompt}\n\nRespond in {language}.\n\nUser: {message}"
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt
        )
        
        answer = response.text
        answer = add_emojis(answer)
        
        if use_voice:
            text_to_speech(answer)
        
        return jsonify({
            "response": answer,
            "success": True,
            "typing_speed": typing_speed
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save-chat', methods=['POST'])
def save_chat_route():
    data = request.json
    messages = data.get('messages', [])
    user_name = data.get('userName', 'User')
    
    filename = save_chat(messages, user_name)
    
    if filename:
        return jsonify({"success": True, "filename": filename})
    else:
        return jsonify({"success": False, "error": "Failed to save"}), 500

@app.route('/api/export-txt', methods=['POST'])
def export_txt():
    data = request.json
    messages = data.get('messages', [])
    user_name = data.get('userName', 'User')
    
    txt_content = export_as_txt(messages, user_name)
    
    try:
        return send_file(
            io.BytesIO(txt_content.encode()),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'chat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    except:
        return jsonify({"error": "Export failed"}), 500

@app.route('/api/get-quick-questions', methods=['GET'])
def get_quick_questions():
    return jsonify({"questions": quick_questions})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)