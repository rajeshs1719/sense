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
import io, tempfile
import base64
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import mediapipe as mp

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in environment.")
else:
    print("✅ Gemini API key loaded successfully.")

genai.configure(api_key=GEMINI_API_KEY)

# --- Bot instructions (CLEANED UP) ---
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
#### 🔹 GENERAL OVERVIEW
- Product Name: SENSE – A New Light of Communication
- Purpose: Online video conferencing and collaboration platform (similar to Jitsi/Zoom).
- Core Features: Video meetings, chat, whiteboard, screen sharing, recording, and file sharing.
- Supported Platforms: Web, Android, and Desktop (Electron).
- Website: https://sensemeet.com (example placeholder)

#### 🔹 ACCOUNT
- Create an account: Go to the homepage → Click Sign Up → Fill in your name, email, and password → Verify via email.
- Login: Click Login on the homepage → Enter your registered email and password.
- Forgot password: Click Forgot Password? on the login screen → Check your registered email for reset instructions.
- Profile update: Go to Profile Settings → Edit your display name, profile picture, or status.

#### 🔹 MEETING MANAGEMENT
- Create a meeting: Click Create Meeting on the dashboard → A unique meeting ID and link are generated.
- Join a meeting: Enter the meeting ID or click on a shared meeting link.
- Schedule a meeting: Go to Meetings → Schedule Meeting → Set date, time, and participants.
- Invite participants: Copy the meeting link or use the “Invite” option to send via email or chat.
- End a meeting: Only the host can click End Meeting for All to close the session.
- Host privileges: Create meetings, manage participants, record sessions, lock meetings.
- Co-host role: Similar to host but limited to participant management and chat moderation.
- Transfer host: Host → Click on participant name → Select Make Host.
- Password protect meetings: Enable Meeting Password in setup.
- Waiting room: Hosts can enable waiting rooms to approve participants before joining.

#### 🔹 AUDIO & VIDEO
- Mute/unmute microphone: Click on the mic icon in the bottom toolbar.
- Turn on/off camera: Click on the camera icon in the toolbar.
- Change microphone or camera: Click Settings → Audio/Video → Select device.
- Echo or audio issue: Ensure only one active audio input, and check browser microphone permissions.
- Change background: Go to Settings → Video → Virtual Background.

#### 🔹 COLLABORATION TOOLS
- Access the whiteboard: Create a meeting → Click on ... (menu button) → Select Whiteboard.
- Collaborate on whiteboard: All participants can draw, type, or add shapes in real-time.
- Save whiteboard: Click Export as Image/PDF to download your whiteboard content.
- Send a message: Open the Chat panel → Type message → Press Enter.
- Private chat: Click on a participant’s name → Select Private Chat.
- Send emoji: Click the emoji icon beside the message bar.
- Share file: Click Attach icon (📎) → Choose a file from your device.
- Supported formats: PDF, DOCX, PPTX, JPG, PNG, MP4.
- Download file: Click on the shared file name → It will download automatically.

#### 🔹 SCREEN SHARING & RECORDING
- Start sharing: Click on the Screen Share icon → Choose screen/window → Confirm.
- Stop sharing: Click Stop Sharing on the toolbar or browser prompt.
- Permissions: Browser may prompt for screen sharing access — allow it to continue.
- Start recording: Host → Click Record → Select Start Recording.
- Stop recording: Click Stop Recording → The file will be saved automatically.
- Where to find recordings: Navigate to Dashboard → Recordings Tab.

#### 🔹 ACCESSIBILITY (DEAF / DUMB / DISABLED USERS)
- Sense is designed to support inclusive communication for all users, including people who are deaf, hard of hearing, or speech-impaired.
- Deaf users can rely on **real-time captions and sign-language recognition**, which transcribes spoken words into readable text and gestures.
- Dumb (speech-impaired) users can use **text-to-speech (TTS)** and **chat translation** to express themselves. Their text messages can be automatically spoken aloud using AI voices.
- Users can choose their **preferred language for captions or TTS output**, making communication across languages seamless.
- The AI can **detect sign language** (when enabled) and convert it into text or voice for others in the meeting.
- Accessibility features can be found in Settings → Accessibility → Enable Captioning / Sign Language / TTS.
- The goal of Sense is to create equal participation for all — bridging gaps between speech, hearing, and gesture-based communication.

#### 🔹 NOTIFICATIONS & SECURITY
- Meeting reminder: You’ll receive reminders via app or email (if enabled).
- Chat notifications: Show in the top-right corner; click to view.
- Mute notifications: Go to Settings → Notifications → Turn Off.
- Lock meeting: Host → Click More → Lock Meeting to prevent new participants from joining.
- Report participant: Click on the participant → Select Report → Provide reason.
---
"""

# --- Initialize Gemini Model ---
try:
    sense_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Using 1.5-flash
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


def generate_dynamic_tts(request):
    """
    GET /api/dynamic_tts/?text=Hello&lang=hi
    or via POST form with 'text' and 'lang'
    """
    text = request.GET.get('text') or request.POST.get('text')
    lang = request.GET.get('lang') or request.POST.get('lang') or 'en'

    if not text:
        return HttpResponse("No text provided", status=400)

    try:
        # 1️⃣ Translate to target language
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        translated_text = translated.text

        # 2️⃣ Generate speech from translated text
        mp3_fp = io.BytesIO()
        tts = gTTS(text=translated_text, lang=lang, slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # 3️⃣ Return the audio stream
        response = HttpResponse(mp3_fp.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename="speech.mp3"'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


# Load model once globally
MODEL_PATH = "ml_models/best_sign_model.h5"
try:
    classifier_model = load_model(MODEL_PATH)
    print(f"✅ Sign classifier model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ ERROR: Could not load sign classifier model from {MODEL_PATH}. Error: {e}")
    classifier_model = None

# Load MediaPipe Hand Detector Model
try:
    mp_hands = mp.solutions.hands
    # Initialize with static_image_mode=True for processing individual images
    # max_num_hands=1 because we only care about one sign at a time
    hand_detector = mp_hands.Hands(
        static_image_mode=True, 
        max_num_hands=1, 
        min_detection_confidence=0.5
    )
    print("✅ MediaPipe hand detector loaded successfully.")
except Exception as e:
    print(f"❌ ERROR: Could not load MediaPipe hands model. Error: {e}")
    hand_detector = None

CLASS_NAMES = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

# --- ⭐️ 3. HELPER FUNCTION TO PAD IMAGE TO A SQUARE ⭐️ ---
def squarify_image(pil_img):
    """Pads a PIL image to be square."""
    # Get the larger dimension
    width, height = pil_img.size
    new_size = max(width, height)
    
    # Create a new square background image (black)
    new_im = Image.new("RGB", (new_size, new_size), (0, 0, 0))
    
    # Paste the original image into the center of the square background
    new_im.paste(pil_img, ((new_size - width) // 2, (new_size - height) // 2))
    return new_im


# --- ⭐️ 4. UPDATED DETECT_SIGN VIEW ⭐️ ---
@csrf_exempt
def detect_sign(request):
    if request.method == 'POST':
        # Check if models are loaded
        if not classifier_model or not hand_detector:
             return JsonResponse({'error': 'Models not loaded on server'}, status=500)
             
        image_data = request.POST.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image received'}, status=400)

        try:
            # --- Decode image from Base64 ---
            _, imgstr = image_data.split(';base64,')
            img_bytes = base64.b64decode(imgstr)
            # original_pil_image is the 224x224 image from the canvas
            original_pil_image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            
            # Convert PIL image to NumPy array for MediaPipe
            # MediaPipe expects RGB images, which .convert('RGB') provides
            frame_rgb = np.array(original_pil_image)

            # --- STEP 1: DETECT HAND ---
            results = hand_detector.process(frame_rgb)

            # If no hands are found, return a specific response
            if not results.multi_hand_landmarks:
                return JsonResponse({'label': 'No Hand', 'confidence': 0})

            # --- Hand IS found, calculate bounding box ---
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Get image dimensions
            img_height, img_width, _ = frame_rgb.shape

            # Find min/max x and y coordinates from landmarks
            x_coords = [landmark.x * img_width for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y * img_height for landmark in hand_landmarks.landmark]
            
            x_min = int(min(x_coords))
            x_max = int(max(x_coords))
            y_min = int(min(y_coords))
            y_max = int(max(y_coords))

            # Add padding to the bounding box (e.g., 20 pixels)
            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(img_width, x_max + padding)
            y_max = min(img_height, y_max + padding)

            # --- Crop the *original PIL image* to the bounding box ---
            cropped_hand_img = original_pil_image.crop((x_min, y_min, x_max, y_max))
            
            # --- "Squarify" the cropped hand image ---
            square_hand_img = squarify_image(cropped_hand_img)

            # --- STEP 2: CLASSIFY SIGN ---
            
            # Resize this new *square hand image* to what the classifier expects
            image_to_predict = square_hand_img.resize((224, 224))
            
            # Preprocess for Keras model
            img_array = img_to_array(image_to_predict)
            img_array = np.expand_dims(img_array / 255.0, axis=0) # (1, 224, 224, 3)

            # Predict
            preds = classifier_model.predict(img_array)
            class_index = np.argmax(preds[0])
            confidence = float(np.max(preds[0]))
            predicted_label = CLASS_NAMES[class_index]

            return JsonResponse({
                'label': predicted_label,
                'confidence': round(confidence * 100, 2)
            })
        
        except Exception as e:
            import traceback
            print(f"Error during prediction: {e}")
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)