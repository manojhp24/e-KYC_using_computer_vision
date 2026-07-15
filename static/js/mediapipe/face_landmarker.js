import { FilesetResolver, FaceLandmarker } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";

let faceLandmarker;

export async function loadFaceLandmarker() {
  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm",
  );

  faceLandmarker = await FaceLandmarker.createFromOptions(
    vision,
    {
        baseOptions:{
            modelAssetPath:"static/models/face_landmarker.task",
        },
        runningMode:"VIDEO",
        numFaces:1
    }
  )
}

export function getFaceLandmarker() {
    return faceLandmarker;
}

export function detectFace(video){
    if(!faceLandmarker){
        return null;
    }

    const now = performance.now();

    return faceLandmarker.detectForVideo(video, now);
}