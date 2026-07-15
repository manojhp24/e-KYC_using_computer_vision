
export async function startCamera(video) {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video:{
                width:1280,
                height:720,
                facingMode:"user"
            },
            audio:false
        })
         video.srcObject = stream
         console.log("Camera started")
    } catch (error) {
        console.error(error);
        alert("Camera access denied or unavailable.");
    }
    
}


export function stopCamera(video){
    const stream = video.srcObject;

    if(!stream) return;

    stream.getTracks().forEach(track => track.stop());

    video.srcObject = null;
}
