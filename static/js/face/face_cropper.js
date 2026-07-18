export function cropFace(video, landmarks) {
  const frameCanvas = document.createElement("canvas");
  const frameContext = frameCanvas.getContext("2d");

  frameCanvas.width = video.videoWidth;
  frameCanvas.height = video.videoHeight;

  frameContext.drawImage(video, 0, 0, frameCanvas.width, frameCanvas.height);

  let minX = Infinity;
  let minY = Infinity;

  let maxX = -Infinity;
  let maxY = -Infinity;

  for (const point of landmarks) {
    const x = point.x * frameCanvas.width;
    const y = point.y * frameCanvas.height;

    minX = Math.min(minX, x);
    minY = Math.min(minY, y);

    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
  }

  const faceWidth = maxX - minX;
  const faceHeight = maxY - minY;

  const paddingX = faceWidth * 0.20;
  const paddingY = faceHeight * 0.20;

  minX -= paddingX;
  minY -= paddingY;

  maxX += paddingX;
  maxY += paddingY;

  minX = Math.max(0, minX);
  minY = Math.max(0, minY);

  maxX = Math.min(frameCanvas.width, maxX);
  maxY = Math.min(frameCanvas.height, maxY);

  const cropWidth = maxX - minX;
  const cropHeight = maxY - minY;

  const faceCanvas = document.createElement("canvas");
  const faceContext = faceCanvas.getContext("2d");

  faceCanvas.width = cropWidth;
  faceCanvas.height = cropHeight;

  faceContext.drawImage(
    frameCanvas,
    minX,
    minY,
    cropWidth,
    cropHeight,
    0,
    0,
    cropWidth,
    cropHeight,
  );

  return faceCanvas;
}
