// Ensure the room name is correctly extracted as a string
const roomName = document.getElementById('room-name').textContent.trim();

let localStream;
let peerConnection;
let socket; // Declare the WebSocket variable

const configuration = {
    'iceServers': [
        { 'urls': 'stun:stun.l.google.com:19302' }  // Google STUN server
    ]
};

function connectWebSocket() {
    socket = new WebSocket('ws://' + window.location.host + '/ws/video-call/' + roomName + '/');

    socket.onopen = function () {
        console.log('WebSocket connection established.');
    };

    socket.onmessage = async function (e) {
        const data = JSON.parse(e.data);

        if (data.type === 'offer') {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(data));
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            socket.send(JSON.stringify({ 'type': 'answer', 'sdp': answer.sdp }));
        } else if (data.type === 'answer') {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(data));
        } else if (data.type === 'candidate') {
            const candidate = new RTCIceCandidate(data);
            await peerConnection.addIceCandidate(candidate);
        }
    };

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly. Attempting to reconnect...');
        setTimeout(connectWebSocket, 1000); // Reconnect after 1 second
    };

    socket.onerror = function (error) {
        console.error('WebSocket error: ', error);
    };
}

// Ensure the function is defined before calling
connectWebSocket();

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        // Display local video stream
        const localVideo = document.getElementById('localVideo');
        localVideo.srcObject = stream;
        localStream = stream;

        // Initialize peer connection
        peerConnection = new RTCPeerConnection(configuration);

        // Add local stream tracks to peer connection
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        // Handle incoming ICE candidates
        peerConnection.onicecandidate = async (event) => {
            if (event.candidate) {
                try {
                    await socket.send(JSON.stringify({ 'type': 'candidate', 'candidate': event.candidate }));
                } catch (error) {
                    console.error('WebSocket is not open. Unable to send ICE candidate:', error);
                }
            }
        };

        // Handle incoming remote stream
        peerConnection.ontrack = function (event) {
            const remoteVideo = document.createElement('video');
            remoteVideo.autoplay = true;
            remoteVideo.srcObject = event.streams[0];
            document.body.appendChild(remoteVideo);
        };

        // Create and send an offer after WebSocket connection is open
        const waitForWebSocket = new Promise((resolve) => {
            if (socket.readyState === WebSocket.OPEN) {
                resolve();
            } else {
                socket.onopen = resolve;
            }
        });

        waitForWebSocket.then(() => {
            peerConnection.createOffer()
                .then(offer => peerConnection.setLocalDescription(offer))
                .then(() => {
                    socket.send(JSON.stringify({ 'type': 'offer', 'sdp': peerConnection.localDescription.sdp }));
                })
                .catch(error => console.error('Error creating offer:', error));
        });

    })
    .catch(error => {
        if (error.name === 'NotReadableError') {
            console.error('Device in use. Please close other applications or browser tabs that might be using the camera or microphone.');
            alert('Device in use. Please close other applications or browser tabs that might be using the camera or microphone.');
        } else {
            console.error('Error accessing media devices:', error);
        }
    });

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // Enter key
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ 'message': message }));
    } else {
        console.error('WebSocket is not open. Unable to send message.');
    }
    messageInputDom.value = '';
};
