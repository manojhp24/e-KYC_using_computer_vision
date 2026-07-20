export async function verifyUser({
  idImagePath,
  liveImagePath,
  idType,
  livenessPassed,
}) {
  const response = await fetch("/api/verify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id_image_path: idImagePath,
      live_image_path: liveImagePath,
      id_type: idType,
      liveness_passed: livenessPassed,
    }),
  });

  if (!response.ok) {
    throw new Error("Verification request failed.");
  }

  return await response.json();
}