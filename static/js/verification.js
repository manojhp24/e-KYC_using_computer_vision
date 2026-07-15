import { startCamera,stopCamera } from "./camera/camera.js";
import {
    loadFaceLandmarker,
    detectFace
} from "./mediapipe/face_landmarker.js";
import { drawLandmarks } from "./drawing/canvas.js";
import { BlinkDetector } from "./mediapipe/blink_detector.js";
import { LEFT_EYE,RIGHT_EYE } from "./mediapipe/eye_landmark.js";
import { captureFrame } from "./camera/capture.js";

const video = document.getElementById("camera");
const blinkCountElement = document.getElementById("blink-count");
const blinkStatus = document.getElementById("liveness-status");
const blinkDetector = new BlinkDetector();

let livenessPassed = false;
let isProcessing = true;

async function init() {
    await startCamera(video);

    await loadFaceLandmarker();

    console.log("Camera Ready");
    console.log("MediaPipe Ready");

    requestAnimationFrame(processFrame);
}

function processFrame() {

    if(!isProcessing) return;

    const result = detectFace(video);

    if(result.faceLandmarks.length>0){
        const landmarks = result.faceLandmarks[0]

        const leftEAR = blinkDetector.calculateEAR(LEFT_EYE,landmarks)
        const rightEAR = blinkDetector.calculateEAR(RIGHT_EYE,landmarks)

        const resultBlink = blinkDetector.detectBlink(leftEAR,rightEAR)
        blinkCountElement.textContent = resultBlink.blinkCount  

        if(blinkDetector.isLivenessPassed() && !livenessPassed){

            livenessPassed = true


            blinkStatus.textContent = "✔ Liveness Passed"
            isProcessing = false;

            

            const canvas = captureFrame(video)

            const image = document.getElementById("captured-image")

            image.src = canvas.toDataURL("image/jpeg")

            image.classList.remove("hidden")

            stopCamera(video);

        }
    }

    if (result && result.faceLandmarks && result.faceLandmarks.length > 0) {
        drawLandmarks(
            video,
            result.faceLandmarks[0]
        );
    } else {
        drawLandmarks(video, null);
    }

    requestAnimationFrame(processFrame);
}
init();