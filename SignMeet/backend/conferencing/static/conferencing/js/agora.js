const APP_ID = '71fbf1e2263a49869725faa8404523ec';
let client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
let localTracks = [];
let remoteUsers = {};

const joinBtn = document.getElementById('joinBtn');
const leaveBtn = document.getElementById('leaveBtn');
const videoContainer = document.getElementById('video_container');

// Function to stop all local tracks
const stopLocalTracks = () => {
    localTracks.forEach(track => track.stop());
    localTracks = [];
};

// Function to fetch token from server
const fetchToken = async (roomName) => {
    const response = await fetch(`/get_token/?channelName=${roomName}`);
    return await response.json();
};

// Join Room Logic
joinBtn.onclick = async () => {
    try {
        // Ensure roomName is defined
        if (!window.roomName || window.roomName.trim() === "") {
            alert("Room name is missing!");
            return;
        }

        const data = await fetchToken(window.roomName);

        if (data.error) {
            throw new Error(data.error);
        }

        const token = data.token;
        const uid = data.uid; // Ensure uid is correctly received from the server

        // Debugging: Log the token and uid
        console.log("Token:", token);
        console.log("UID:", uid);

        // Initialize the Agora client
        client.on('user-published', handleUserPublished);
        client.on('user-unpublished', handleUserUnpublished);

        await client.join(APP_ID, window.roomName, token, uid);

        // Create and display local video
        const localTrack = await AgoraRTC.createCameraVideoTrack();
        localTracks.push(localTrack);

        const localPlayer = document.createElement("div");
        localPlayer.id = `user-${uid}`;
        localPlayer.style.width = "400px";
        localPlayer.style.height = "300px";
        videoContainer.appendChild(localPlayer);
        localTrack.play(localPlayer);

        // Publish the local track
        await client.publish(localTracks);

        joinBtn.disabled = true;
        leaveBtn.disabled = false;

    } catch (err) {
        console.error("Failed to join room:", err);
    }
};

// Handle Remote Users
const handleUserPublished = async (user, mediaType) => {
    await client.subscribe(user, mediaType);
    if (mediaType === "video") {
        const remotePlayer = document.createElement("div");
        remotePlayer.id = `user-${user.uid}`;
        remotePlayer.style.width = "400px";
        remotePlayer.style.height = "300px";
        videoContainer.appendChild(remotePlayer);
        user.videoTrack.play(remotePlayer);
        remoteUsers[user.uid] = user;
    }
};

const handleUserUnpublished = user => {
    const remotePlayer = document.getElementById(`user-${user.uid}`);
    if (remotePlayer) remotePlayer.remove();
    delete remoteUsers[user.uid];
};

// Leave Room Logic
leaveBtn.onclick = async () => {
    stopLocalTracks();
    await client.leave();
    videoContainer.innerHTML = '';
    remoteUsers = {};

    joinBtn.disabled = false;
    leaveBtn.disabled = true;
};
