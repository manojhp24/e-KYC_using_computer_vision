import { startCamera, stopCamera } from "./camera/camera.js";
import { loadFaceLandmarker, detectFace } from "./mediapipe/face_landmarker.js";
import { drawLandmarks } from "./drawing/canvas.js";
import { BlinkDetector } from "./mediapipe/blink_detector.js";
import { LEFT_EYE, RIGHT_EYE } from "./mediapipe/eye_landmark.js";
import { captureFrame } from "./camera/capture.js";
import { clearCanvas } from "./drawing/canvas.js";
import { cropFace } from "./face/face_cropper.js";
import { initializeUpload, getUploadedIdPath } from "./upload/upload.js";
import { uploadLiveFace } from "./upload/live_upload.js";
import { verifyUser } from "./api/verification_api.js";

const video = document.getElementById("camera");
const blinkCountElement = document.getElementById("blink-count");
const scanningLine = document.getElementById("scanning-line");
const blinkStatus = document.getElementById("liveness-status");
const blinkDetector = new BlinkDetector();

let livenessPassed = false;
let isProcessing = true;

async function init() {
  initializeUpload();

  await startCamera(video);

  await loadFaceLandmarker();

  console.log("Camera Ready");
  console.log("MediaPipe Ready");

  requestAnimationFrame(processFrame);
}

function displayVerificationResult(verificationResult) {
  const resultCard = document.getElementById("verification-result-card");
  const resultDetails = document.getElementById("result-details");
  const status = document.getElementById("result-status");

  resultCard.classList.remove("hidden");

  status.textContent = verificationResult.message;
  status.className = verificationResult.success
    ? "font-semibold text-emerald-400"
    : "font-semibold text-red-400";

  // Duplicate user
  if (verificationResult.user_exists) {
    resultDetails.classList.add("hidden");
    return;
  }

  resultDetails.classList.remove("hidden");

  const ocr = verificationResult.ocr_data || {};

  document.getElementById("result-name").textContent =
    ocr.name ?? "-";

  document.getElementById("result-id-number").textContent =
    ocr.id_number ?? "-";

  document.getElementById("result-id-type").textContent =
    ocr.id_type ?? "-";

  document.getElementById("result-dob").textContent =
    ocr.date_of_birth ?? "-";

  document.getElementById("result-face-match").textContent =
    verificationResult.face_match
      ? "✔ Matched"
      : "✖ Not Matched";
}

async function processFrame() {
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

      setTimeout(async () => {
        // const canvas = captureFrame(video);

        const faceCanvas = cropFace(video, landmarks);

        const image = document.getElementById("captured-image");

        image.src = faceCanvas.toDataURL("image/jpeg");
        const uploadResult = await uploadLiveFace(faceCanvas);

        console.log(uploadResult);
        const liveFacePath = uploadResult.path;

        const idImagePath = getUploadedIdPath();

        if (!idImagePath) {
          console.error("ID image has not been uploaded.");
          return;
        }
         image.classList.remove("hidden");

        scanningLine.classList.add("hidden");
        document.getElementById("loading-overlay").classList.remove("hidden");
        clearCanvas();
        stopCamera(video);

        const verificationResult = await verifyUser({
          idImagePath,
          liveImagePath: liveFacePath,
          idType: "PAN",
          livenessPassed,
        });

        console.log(verificationResult);
        console.log(verificationResult.ocr_data);

        document.getElementById("loading-overlay").classList.add("hidden");

        displayVerificationResult(verificationResult);

       
        

        // Trigger Toastr notification after face capture is done
        if (typeof toastr !== "undefined") {
          toastr.success(
            "Biometric face capture completed successfully.",
            "Verification Captured",
            {
              closeButton: true,
              progressBar: true,
              positionClass: "toast-top-right",
              timeOut: 5000,
            },
          );
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
