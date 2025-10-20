// =========================
// SENSE Speech Engine
// Handles Speech-to-Text (STT) + Text-to-Speech (TTS)
// =========================

let recognition;
let isRecognizing = false;
const captionDisplay = document.getElementById("caption-display");
const startBtn = document.getElementById("start-stt");
const stopBtn = document.getElementById("stop-stt");
const speakBtn = document.getElementById("speak-btn");


// ========== SPEECH TO TEXT ==========
function startSpeechToText() {
  const lang = document.getElementById("stt-language").value;

  // Check browser support
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Speech Recognition not supported in this browser. Try Chrome or Edge.");
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = lang;
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isRecognizing = true;
    captionDisplay.innerHTML = `<p class='status'>Listening...</p>`;
    console.log("🎙️ Speech recognition started");
  };

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      transcript += event.results[i][0].transcript;
    }
    captionDisplay.innerHTML = `<p>${transcript}</p>`;
    captionDisplay.scrollTop = captionDisplay.scrollHeight;
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    captionDisplay.innerHTML += `<p class='status'>Error: ${event.error}</p>`;
  };

  recognition.onend = () => {
    isRecognizing = false;
    captionDisplay.innerHTML += `<p class='status'>Recognition stopped.</p>`;
    console.log("🛑 Speech recognition stopped");
  };

  recognition.start();
}

function stopSpeechToText() {
  if (recognition && isRecognizing) {
    recognition.stop();
    isRecognizing = false;
  }
}

// ========== TEXT TO SPEECH ==========
function speakText() {
  const text = document.getElementById("tts-text").value.trim();
  const lang = document.getElementById("tts-language").value;

  if (!text) {
    alert("Please enter text to speak.");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  utterance.rate = 1;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
}


// ========== EVENT LISTENERS ==========
startBtn.addEventListener("click", startSpeechToText);
stopBtn.addEventListener("click", stopSpeechToText);
speakBtn.addEventListener("click", speakText);
