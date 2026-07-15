const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d")


export function drawLandmarks(video,landmarks){
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!landmarks) {
        return;
    }

    ctx.fillStyle = "#00ff00";

    for (const point of landmarks) {

        const x = point.x * canvas.width;
        const y = point.y * canvas.height;

        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
    }
}