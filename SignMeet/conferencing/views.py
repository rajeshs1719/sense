from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from agora_token_builder import RtcTokenBuilder
import time, random, json, os
from dotenv import load_dotenv
import google.generativeai as genai
from django.http import HttpRequest, HttpResponse
from gtts import gTTS
from googletrans import Translator
import io,tempfile

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in environment.")
else:
    print("✅ Gemini API key loaded successfully.")

genai.configure(api_key=GEMINI_API_KEY)

# --- Bot instructions ---
# SENSE_BOT_INSTRUCTIONS = """### ROLE ###
# You are a helpful assistant for the "SENSE" meeting conference project. Your name is "Sense Bot".

# ### TASK ###
# Your job is to answer user questions about SENSE.
# - Be friendly, clear, and concise.
# - You MUST answer questions using ONLY the information provided in the "KNOWLEDGE" section below.
# - If the answer is not in the "KNOWLEDGE" section, say: "I'm sorry, I don't have that information. You can contact our support team at support@wisdom.com."
# - Do not make up answers or use your general knowledge.

# ### KNOWLEDGE ###
# ---
# - Product Name: SENSE: A New Light of Communication
# - How to access the whiteboard: Create a meeting Id through Your name > press on ... (menu button) there click on whiteboard
# - How to mute myself: Click on the mic option provided in the tab section.
# ---
# """
SENSE_BOT_INSTRUCTIONS = """
### ROLE ###
You are a helpful assistant for the "SENSE" meeting conference platform. Your name is "Sense Bot".

 ### TASK ###
Your job is to answer user questions about SENSE.
- Be friendly, clear, and concise.
- You MUST answer questions using ONLY the information provided in the "KNOWLEDGE" section below.
- If the answer is not in the "KNOWLEDGE" section, say: "I'm sorry, I don't have that information. You can contact our support team at support@wisdom.com."
- Do not make up answers or use your general knowledge.

### KNOWLEDGE ###
---
 - Product Name: SENSE – A New Light of Communication
 - Purpose: Online video conferencing and collaboration platform (similar to Jitsi/Zoom).
 - Core Features: Video meetings, chat, whiteboard, screen sharing, recording, and file sharing.
 - Supported Platforms: Web, Android, and Desktop (Electron).
 - Website: https://sensemeet.com (example placeholder)
 - Create an account: Go to the homepage → Click Sign Up → Fill in your name, email, and password → Verify via email.
 - Login: Click Login on the homepage → Enter your registered email and password.
 - Forgot password: Click Forgot Password? on the login screen → Check your registered email for reset instructions.
 - Profile update: Go to Profile Settings → Edit your display name, profile picture, or status.
 - Create a meeting: Click Create Meeting on the dashboard → A unique meeting ID and link are generated.
 - Join a meeting: Enter the meeting ID or click on a shared meeting link.
 - Schedule a meeting: Go to Meetings → Schedule Meeting → Set date, time, and participants.
 - Invite participants: Copy the meeting link or use the “Invite” option to send via email or chat.
 - End a meeting: Only the host can click End Meeting for All to close the session.
 - Mute/unmute microphone: Click on the mic icon in the bottom toolbar.
 - Turn on/off camera: Click on the camera icon in the toolbar.
 - Change microphone or camera: Click Settings → Audio/Video → Select device.
 - Echo or audio issue: Ensure only one active audio input, and check browser microphone permissions.
 - Access the whiteboard: Create a meeting → Click on ... (menu button) → Select Whiteboard.
 - Collaborate on whiteboard: All participants can draw, type, or add shapes in real-time.
 - Save whiteboard: Click Export as Image/PDF to download your whiteboard content.
 - Send a message: Open the Chat panel → Type message → Press Enter.
 - Private chat: Click on a participant’s name → Select Private Chat.
 - Send emoji: Click the emoji icon beside the message bar.
 - Share file: Click Attach icon (📎) → Choose a file from your device.
 - Start sharing: Click on the Screen Share icon → Choose screen/window → Confirm.
 - Stop sharing: Click Stop Sharing on the toolbar or browser prompt.
 - Permissions: Browser may prompt for screen sharing access — allow it to continue.
 - Start recording: Host → Click Record → Select Start Recording.
 - Stop recording: Click Stop Recording → The file will be saved automatically.
 - Where to find recordings: Navigate to Dashboard → Recordings Tab.
 - Change background: Go to Settings → Video → Virtual Background.
 - Manage participants: Host can mute/unmute others, remove users, or make someone co-host.
 - Lock meeting: Host → Click More → Lock Meeting to prevent new participants from joining.
 - Upload file: Use the File Share tab or Attach (📎) icon in chat.
 - Supported formats: PDF, DOCX, PPTX, JPG, PNG, MP4.
 - Download file: Click on the shared file name → It will download automatically.
 - Meeting reminder: You’ll receive reminders via app or email (if enabled).
 - Chat notifications: Show in the top-right corner; click to view.
 - Mute notifications: Go to Settings → Notifications → Turn Off.
 - Host privileges: Create meetings, manage participants, record sessions, lock meetings.
 - Co-host role: Similar to host but limited to participant management and chat moderation.
 - Transfer host: Host → Click on participant name → Select Make Host.
 - Password protect meetings: Enable Meeting Password in setup.
 - Waiting room: Hosts can enable waiting rooms to approve participants before joining.
 - Report participant: Click on the participant → Select Report → Provide reason.
---
"""

# --- Initialize Gemini Model ---
try:
    sense_model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SENSE_BOT_INSTRUCTIONS
    )
    chat_session = sense_model.start_chat(history=[])
    print("✅ Gemini SENSE Bot initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing Gemini: {e}")
    sense_model = None
    chat_session = None


# --- Basic Views ---
def home(request):
    return render(request, 'home.html')

def video_call(request, room_name):
    uid = request.GET.get('uid', '')
    return render(request, 'room.html', {'room_name': room_name, 'uid': uid})

def get_agora_token(request):
    app_id = '71fbf1e2263a49869725faa8404523ec'
    app_certificate = 'c30096eedb10445fb0990cb0d0a4f15b'
    channel_name = request.GET.get('channelName')

    if not channel_name:
        return JsonResponse({'error': 'Missing channelName'}, status=400)

    uid = random.randint(1, 230)
    role = 1
    expire_time = 3600
    current_time = int(time.time())
    privilege_expired_ts = current_time + expire_time

    try:
        token = RtcTokenBuilder.buildTokenWithUid(
            app_id, app_certificate, channel_name, uid, role, privilege_expired_ts
        )
        return JsonResponse({'token': token, 'uid': uid})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- Chatbot endpoint ---
@csrf_exempt
def sense_chat_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    if not chat_session:
        print("❌ Chat session is not initialized.")
        return JsonResponse({'error': 'Gemini model not initialized.'}, status=500)

    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        print("📩 User message:", user_message)

        if not user_message:
            return JsonResponse({'error': 'No message provided.'}, status=400)

        # --- Add this debug ---
        print("🚀 Sending message to Gemini...")
        response = chat_session.send_message(user_message)
        print("✅ Gemini response received.")

        return JsonResponse({'reply': response.text})

    except Exception as e:
        import traceback
        print("❌ Gemini API Error:", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    

def process_caption(request):
    import json
    data = json.loads(request.body)
    text = data.get("text", "")

    # Example: convert text to speech dynamically
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        return JsonResponse({"audio_url": "/media/" + os.path.basename(tmp.name)})


def generate_dynamic_tts(request: HttpRequest) -> HttpResponse:
    """
    Translates text and converts it to speech.
    Expects 'text' (in English) and 'lang' (target language)
    Example: /api/dynamic_tts/?text=Welcome&lang=hi
    """
    base_text = request.GET.get('text', 'Hello')
    lang_code = request.GET.get('lang', 'en') # e.g., 'hi', 'ta', 'te'

    if not base_text:
        return HttpResponse("No text provided", status=400)

    try:
        # --- 1. Translate the text ---
        translator = Translator()
        translated = translator.translate(base_text, dest=lang_code)
        translated_text = translated.text

        # --- 2. Convert translated text to speech ---
        mp3_fp = io.BytesIO()
        tts = gTTS(text=translated_text, lang=lang_code, tld='co.in', slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # --- 3. Send the audio back ---
        response = HttpResponse(mp3_fp, content_type='audio/mpeg')
        return response

    except Exception as e:
        # This will catch errors if a language is not supported
        return HttpResponse(f"Error generating dynamic TTS: {e}", status=500)
    


