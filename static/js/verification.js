import { startCamera, stopCamera } from "./camera/camera.js";
import { loadFaceLandmarker, detectFace } from "./mediapipe/face_landmarker.js";
import { drawLandmarks } from "./drawing/canvas.js";
import { BlinkDetector } from "./mediapipe/blink_detector.js";
import { LEFT_EYE, RIGHT_EYE } from "./mediapipe/eye_landmark.js";
import { captureFrame } from "./camera/capture.js";
import { clearCanvas } from "./drawing/canvas.js";
import { cropFace } from "./face/face_cropper.js";

const video = document.getElementById("camera");
const blinkCountElement = document.getElementById("blink-count");
const scanningLine = document.getElementById("scanning-line")
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
    if (!isProcessing) return;

    const result = detectFace(video);

    if (result.faceLandmarks.length > 0) {
        const landmarks = result.faceLandmarks[0];

        const leftEAR = blinkDetector.calculateEAR(LEFT_EYE, landmarks);
        const rightEAR = blinkDetector.calculateEAR(RIGHT_EYE, landmarks);

        const resultBlink = blinkDetector.detectBlink(leftEAR, rightEAR);
        blinkCountElement.textContent = resultBlink.blinkCount;

        if (blinkDetector.isLivenessPassed() && !livenessPassed) {
            livenessPassed = true;

            blinkStatus.textContent = "✔ Liveness Passed";
            isProcessing = false;

            setTimeout(() => {
                // const canvas = captureFrame(video);

                const faceCanvas = cropFace(video,landmarks)

                const image = document.getElementById("captured-image");

                image.src = faceCanvas.toDataURL("image/jpeg");

                image.classList.remove("hidden");

                scanningLine.classList.add("hidden")
                clearCanvas()
                stopCamera(video);

                // Trigger Toastr notification after face capture is done
                if (typeof toastr !== "undefined") {
                    toastr.success("Biometric face capture completed successfully.", "Verification Captured", {
                        closeButton: true,
                        progressBar: true,
                        positionClass: "toast-top-right",
                        timeOut: 5000
                    });
                } else {
                    console.log("Toastr not loaded, captured face successfully.");
                }
            }, 2000);
        }
    }

    if (result && result.faceLandmarks && result.faceLandmarks.length > 0) {
        drawLandmarks(video, result.faceLandmarks[0]);
    } else {
        drawLandmarks(video, null);
    }

    requestAnimationFrame(processFrame);
}
init();
