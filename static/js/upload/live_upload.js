export async function uploadLiveFace(faceCanvas) {
  return new Promise((resolve, reject) => {
    faceCanvas.toBlob(async (blob) => {
      try {
        const formData = new FormData();
        formData.append("file", blob, "live_face.jpg");

        const response = await fetch("/api/upload/live", {
          method: "POST",
          body: formData,
        });
        const result = await response.json();

        resolve(result);
      } catch (error) {
        reject(error)
      }
    },"image/jpeg");
  });
}
