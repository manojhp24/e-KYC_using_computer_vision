let uploadedIdPath = null;

export function initializeUpload(onUploadSuccess,onReset) {
  const input = document.getElementById("id-upload");
  const preview = document.getElementById("id-card-preview");
  const prompt = document.getElementById("id-upload-prompt");
  const resetBtn = document.getElementById("id-reset-btn");



  if (input) {
    input.addEventListener("change", async () => {
      const file = input.files[0];

      if (!file) return;

      preview.src = URL.createObjectURL(file);
      preview.classList.remove("hidden");
      if (prompt) prompt.classList.add("hidden");
      if (resetBtn) resetBtn.classList.remove("hidden");

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("/api/upload/id", {
          method: "POST",
          body: formData,
        });
        const result = await response.json();

        if (result.success) {
          uploadedIdPath = result.path;

          if(onUploadSuccess){
            onUploadSuccess(result.path)
          }
        }
      } catch (error) {
        console.error(error);
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (input) input.value = "";
      uploadedIdPath = null;
      if (preview) {
        preview.src = "";
        preview.classList.add("hidden");
      }
      if (prompt) prompt.classList.remove("hidden");
      resetBtn.classList.add("hidden");

      if(onReset){
        onReset()
      }
    });
  }
}


export function getUploadedIdPath() {
    return uploadedIdPath;
}
