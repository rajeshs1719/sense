// detect.js

// Ensure Fingerpose is available
if (typeof fp === 'undefined') {
    console.error("Fingerpose library not loaded. Ensure the Fingerpose CDN is included.");
    throw new Error("Fingerpose library not loaded");
}

const { GestureEstimator, GestureDescription, Finger, FingerCurl, FingerDirection } = fp;

let handposeModel = null;
let gestureEstimator = null;
let isDetecting = false;

// Load Handpose model and define ASL gestures (digits and letters)
async function loadHandposeAndGestures() {
    try {
        console.log("Loading Handpose model...");
        handposeModel = await handpose.load();
        console.log("Handpose model loaded successfully");

        // Define ASL digit gestures (existing)
        const aslDigit1 = new GestureDescription('1');
        aslDigit1.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslDigit1.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslDigit1.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslDigit1.addCurl(Finger.Middle, FingerCurl.FullCurl, 1.0);
        aslDigit1.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslDigit1.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslDigit2 = new GestureDescription('2');
        aslDigit2.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslDigit2.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslDigit2.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslDigit2.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslDigit2.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslDigit2.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslDigit2.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslDigit3 = new GestureDescription('3');
        aslDigit3.addCurl(Finger.Thumb, FingerCurl.NoCurl, 1.0);
        aslDigit3.addDirection(Finger.Thumb, FingerDirection.VerticalUp, 1.0);
        aslDigit3.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslDigit3.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslDigit3.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslDigit3.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslDigit3.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslDigit3.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslDigit4 = new GestureDescription('4');
        aslDigit4.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslDigit4.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslDigit4.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslDigit4.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslDigit4.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslDigit4.addCurl(Finger.Ring, FingerCurl.NoCurl, 1.0);
        aslDigit4.addDirection(Finger.Ring, FingerDirection.VerticalUp, 1.0);
        aslDigit4.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslDigit5 = new GestureDescription('5');
        aslDigit5.addCurl(Finger.Thumb, FingerCurl.NoCurl, 1.0);
        aslDigit5.addDirection(Finger.Thumb, FingerDirection.VerticalUp, 1.0);
        aslDigit5.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslDigit5.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslDigit5.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslDigit5.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslDigit5.addCurl(Finger.Ring, FingerCurl.NoCurl, 1.0);
        aslDigit5.addDirection(Finger.Ring, FingerDirection.VerticalUp, 1.0);
        aslDigit5.addCurl(Finger.Pinky, FingerCurl.NoCurl, 1.0);
        aslDigit5.addDirection(Finger.Pinky, FingerDirection.VerticalUp, 1.0);

        // Define ASL letter gestures (A-F)
        const aslLetterA = new GestureDescription('A');
        aslLetterA.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslLetterA.addCurl(Finger.Index, FingerCurl.FullCurl, 1.0);
        aslLetterA.addCurl(Finger.Middle, FingerCurl.FullCurl, 1.0);
        aslLetterA.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslLetterA.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslLetterB = new GestureDescription('B');
        aslLetterB.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslLetterB.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslLetterB.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslLetterB.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslLetterB.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslLetterB.addCurl(Finger.Ring, FingerCurl.NoCurl, 1.0);
        aslLetterB.addDirection(Finger.Ring, FingerDirection.VerticalUp, 1.0);
        aslLetterB.addCurl(Finger.Pinky, FingerCurl.NoCurl, 1.0);
        aslLetterB.addDirection(Finger.Pinky, FingerDirection.VerticalUp, 1.0);

        const aslLetterC = new GestureDescription('C');
        aslLetterC.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslLetterC.addCurl(Finger.Index, FingerCurl.HalfCurl, 1.0);
        aslLetterC.addCurl(Finger.Middle, FingerCurl.HalfCurl, 1.0);
        aslLetterC.addCurl(Finger.Ring, FingerCurl.HalfCurl, 1.0);
        aslLetterC.addCurl(Finger.Pinky, FingerCurl.HalfCurl, 1.0);

        const aslLetterD = new GestureDescription('D');
        aslLetterD.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslLetterD.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
        aslLetterD.addDirection(Finger.Index, FingerDirection.VerticalUp, 1.0);
        aslLetterD.addCurl(Finger.Middle, FingerCurl.FullCurl, 1.0);
        aslLetterD.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslLetterD.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslLetterE = new GestureDescription('E');
        aslLetterE.addCurl(Finger.Thumb, FingerCurl.FullCurl, 1.0);
        aslLetterE.addCurl(Finger.Index, FingerCurl.FullCurl, 1.0);
        aslLetterE.addCurl(Finger.Middle, FingerCurl.FullCurl, 1.0);
        aslLetterE.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
        aslLetterE.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);

        const aslLetterF = new GestureDescription('F');
        aslLetterF.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 1.0);
        aslLetterF.addCurl(Finger.Index, FingerCurl.HalfCurl, 1.0);
        aslLetterF.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
        aslLetterF.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
        aslLetterF.addCurl(Finger.Ring, FingerCurl.NoCurl, 1.0);
        aslLetterF.addDirection(Finger.Ring, FingerDirection.VerticalUp, 1.0);
        aslLetterF.addCurl(Finger.Pinky, FingerCurl.NoCurl, 1.0);
        aslLetterF.addDirection(Finger.Pinky, FingerDirection.VerticalUp, 1.0);

        // Initialize GestureEstimator with all gestures
        gestureEstimator = new GestureEstimator([
            aslDigit1,
            aslDigit2,
            aslDigit3,
            aslDigit4,
            aslDigit5,
            aslLetterA,
            aslLetterB,
            aslLetterC,
            aslLetterD,
            aslLetterE,
            aslLetterF,
        ]);
        console.log("Gesture estimator initialized with ASL digits 1-5 and letters A-F");
    } catch (error) {
        console.error("Failed to load Handpose or initialize gestures:", error);
        throw new Error("Failed to load Handpose or gestures");
    }
}

// Start sign language detection
async function startDetection(videoElement, subtitleElement) {
    if (!handposeModel || !gestureEstimator) {
        throw new Error("Handpose model or gesture estimator not loaded");
    }

    isDetecting = true;

    async function predict() {
        if (!isDetecting) return;

        // Detect hands in the video frame
        const predictions = await handposeModel.estimateHands(videoElement);
        let translation = "[None]";

        if (predictions.length > 0) {
            const hand = predictions[0]; // Take the first detected hand
            const landmarks = hand.landmarks;

            // Estimate gesture using Fingerpose
            const gesture = gestureEstimator.estimate(landmarks, 8.0); // Confidence threshold: 8.0
            if (gesture.gestures && gesture.gestures.length > 0) {
                // Log all detected gestures with their confidence scores
                console.log("All detected gestures:", gesture.gestures);
                const bestGesture = gesture.gestures.reduce((prev, current) =>
                    (prev.confidence > current.confidence) ? prev : current
                );
                translation = bestGesture.name; // e.g., "A", "B", "1", etc.
                console.log("Best detected gesture:", bestGesture.name, "Confidence:", bestGesture.confidence);
            } else {
                console.log("No gesture detected with sufficient confidence");
            }
        } else {
            console.log("No hand detected");
        }

        subtitleElement.textContent = `Translation: ${translation}`;
        setTimeout(predict, 100); // Run every 100ms for smoother detection
    }

    predict();
}

// Stop sign language detection
function stopDetection() {
    isDetecting = false;
}

// Export functions for use in room.html
window.detect = {
    loadHandposeAndGestures,
    startDetection,
    stopDetection
};