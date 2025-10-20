// ===============================
// SENSE: Integrated Speech Captions Overlay
// ===============================

let recognition;
let isRecognizing = false;
const overlay = document.getElementById("caption-overlay");
const startBtn = document.getElementById("start-stt");
const stopBtn = document.getElementById("stop-stt");

// === Start STT ===
function startSpeechRecognition() {
    const lang = document.getElementById("stt-language").value;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition not supported. Use Chrome or Edge.");
        return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = lang;
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
        isRecognizing = true;
        overlay.textContent = "🎤 Listening...";
        overlay.style.opacity = 1;
        console.log("Speech recognition started");
    };

    recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            transcript += event.results[i][0].transcript;
        }
        overlay.textContent = transcript;
        overlay.style.opacity = 1;
    };

    recognition.onerror = (event) => {
        overlay.textContent = "⚠️ Error: " + event.error;
        console.error("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
        isRecognizing = false;
        overlay.textContent = "🛑 Recognition stopped.";
        setTimeout(() => (overlay.style.opacity = 0.5), 2000);
    };

    recognition.start();
}

// === Stop STT ===
function stopSpeechRecognition() {
    if (recognition && isRecognizing) {
        recognition.stop();
        isRecognizing = false;
    }
}

// === Event Listeners ===
startBtn.addEventListener("click", startSpeechRecognition);
stopBtn.addEventListener("click", stopSpeechRecognition);

