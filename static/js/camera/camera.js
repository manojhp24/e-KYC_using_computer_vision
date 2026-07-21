let cameraStream = null;

export async function startCamera(video) {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: 1280,
        height: 720,
        facingMode: "user",
      },
      audio: false,
    });

    video.srcObject = cameraStream;
    await video.play();

    console.log("Camera started");
  } catch (error) {
    console.error(error);
  }
}

export function stopCamera(video) {
  if (cameraStream) {
    cameraStream.getTracks().forEach((track) => {
      console.log(track.readyState);
      track.stop();
      console.log(track.readyState);
    });

    cameraStream = null;
  }

  if (video) {
    video.pause();
    video.srcObject = null;
  }

}
