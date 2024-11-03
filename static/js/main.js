document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("file");
  const fileLabel = document.getElementById("file-label");
  const fileInfo = document.getElementById("file-info");
  const fileName = document.getElementById("file-name");
  const removeFile = document.getElementById("remove-file");
  const uploadButton = document.getElementById("upload-button");
  const loading = document.getElementById("loading");
  const loadingText = document.getElementById("loading-text");
  const progressBar = document.getElementById("progress-bar");
  const result = document.getElementById("result");
  const summaryText = document.getElementById("summary-text");
  const audioPlayer = document.getElementById("audio-player");

  // File drag and drop handlers
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    form.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    form.addEventListener(eventName, () => {
      fileLabel.classList.add("file-drag-over");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    form.addEventListener(eventName, () => {
      fileLabel.classList.remove("file-drag-over");
    });
  });

  form.addEventListener("drop", (e) => {
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && isValidFileType(droppedFile)) {
      handleFileSelect(droppedFile);
    }
  });

  // File input change handler
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  });

  function handleFileSelect(file) {
    if (isValidFileType(file)) {
      fileName.textContent = file.name;
      fileLabel.classList.add("hidden");
      fileInfo.classList.remove("hidden");
      uploadButton.disabled = false;
    } else {
      alert("Please select a PDF or DOCX file");
      clearFileSelection();
    }
  }

  function isValidFileType(file) {
    const validTypes = [".pdf", ".docx"];
    const extension = "." + file.name.split(".").pop().toLowerCase();
    return validTypes.includes(extension);
  }

  // Remove file handler
  removeFile.addEventListener("click", clearFileSelection);

  function clearFileSelection() {
    fileInput.value = "";
    fileLabel.classList.remove("hidden");
    fileInfo.classList.add("hidden");
    uploadButton.disabled = true;
  }

  // Form submit handler
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const file = formData.get("file");

    if (!file) {
      alert("Please select a file");
      return;
    }

    loading.classList.remove("hidden");
    result.classList.add("hidden");
    uploadButton.disabled = true;

    try {
      // Upload file
      const uploadResponse = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadResponse.json();

      if (uploadData.error) {
        throw new Error(uploadData.error);
      }

      // Poll for status
      const pollStatus = async () => {
        const statusResponse = await fetch(`/status/${uploadData.file_id}`);
        const statusData = await statusResponse.json();

        if (statusData.status === "processing") {
          // Update progress bar and text
          progressBar.style.width = `${statusData.progress}%`;
          loadingText.textContent = `Processing: ${statusData.step.replace(
            "_",
            " "
          )}...`;

          // Continue polling
          setTimeout(pollStatus, 1000);
        } else if (statusData.status === "completed") {
          // Show results
          summaryText.textContent = statusData.summary;
          audioPlayer.src = `/audio/${statusData.audio_path}`;

          loading.classList.add("hidden");
          result.classList.remove("hidden");
          clearFileSelection();
        } else if (statusData.status === "error") {
          throw new Error(statusData.error);
        }
      };

      // Start polling
      pollStatus();
    } catch (error) {
      alert("Error: " + error.message);
      loading.classList.add("hidden");
      uploadButton.disabled = false;
    }
  });
});
