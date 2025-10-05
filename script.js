const imageInput = document.getElementById("imageInput");
const uploadBtn = document.getElementById("uploadBtn");
const preview = document.getElementById("preview");
const resultsDiv = document.getElementById("results");

let selectedFile = null;

imageInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});

uploadBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Please select an image first!");
    return;
  }

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const response = await fetch("http://127.0.0.1:5000/detect", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    resultsDiv.innerHTML = "";
    data.forEach(obj => {
      const chip = document.createElement("div");
      chip.className = "chip";
      chip.textContent = `${obj.class} (${(obj.confidence * 100).toFixed(1)}%)`;
      resultsDiv.appendChild(chip);
    });
  } catch (err) {
    console.error(err);
    alert("Error analyzing the image!");
  }
});
