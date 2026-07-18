import { FilesetResolver, FaceLandmarker } from "./lib/vision_bundle.mjs";

let faceLandmarker;

export async function loadFaceLandmarker() {
  const vision = await FilesetResolver.forVisionTasks(
    "/static/js/mediapipe/lib/wasm",
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