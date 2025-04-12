// Room.js
import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { useLocation } from 'react-router-dom';

const Room = () => {
    const location = useLocation();
    const [localStream, setLocalStream] = useState(null);
    const [peerConnection, setPeerConnection] = useState(null);
    const [socket, setSocket] = useState(null);
    const [remoteStreams, setRemoteStreams] = useState([]);
    const [isCameraEnabled, setIsCameraEnabled] = useState(true);

    useEffect(() => {
        const roomName = new URLSearchParams(location.search).get('roomName');
        const socket = io(`http://localhost:8000/ws/video-call/${roomName}/`);
        setSocket(socket);

        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                setLocalStream(stream);
                const localVideo = document.getElementById('localVideo');
                localVideo.srcObject = stream;
                localVideo.play();

                const peerConnection = new RTCPeerConnection({
                    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
                });
                setPeerConnection(peerConnection);

                stream.getTracks().forEach(track => {
                    peerConnection.addTrack(track, stream);
                });

                peerConnection.onicecandidate = event => {
                    if (event.candidate) {
                        socket.emit('candidate', { candidate: event.candidate });
                    }
                };

                peerConnection.ontrack = event => {
                    const remoteVideo = document.createElement('video');
                    remoteVideo.autoplay = true;
                    remoteVideo.srcObject = event.streams[0];
                    document.getElementById('remoteVideos').appendChild(remoteVideo);
                    setRemoteStreams(prevStreams => [...prevStreams, remoteVideo]);
                };

                socket.on('offer', async offer => {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    socket.emit('answer', { sdp: answer.sdp });
                });

                socket.on('answer', async answer => {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
                });

                socket.on('candidate', async candidate => {
                    await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
                });
            })
            .catch(error => {
                console.error('Error accessing media devices:', error);
            });

        return () => {
            socket.disconnect();
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
            }
        };
    }, [location]);

    const toggleCamera = () => {
        if (localStream) {
            const videoTrack = localStream.getVideoTracks()[0];
            videoTrack.enabled = !videoTrack.enabled;
            setIsCameraEnabled(!isCameraEnabled);
        }
    };

    return (
        <div>
            <h1>{location.search}</h1>
            <video id="localVideo" autoPlay muted />
            <button onClick={toggleCamera}>Toggle Camera ({isCameraEnabled ? 'On' : 'Off'})</button>
            <div id="remoteVideos">
                {remoteStreams.map((stream, index) => (
                    <video key={index} autoPlay />
                ))}
            </div>
        </div>
    );
};

export default Room;