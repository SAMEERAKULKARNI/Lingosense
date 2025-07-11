async function processMessage() {
  const userInput = document.getElementById("userInput").value;
  if (!userInput.trim()) {
    alert("Please enter some text.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    updateResults(data);
  } catch (error) {
    alert("Something went wrong while connecting to the server.");
    console.error(error);
  }
}

async function processFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze-file", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    updateResults(data);
  } catch (error) {
    alert("Something went wrong while uploading the file.");
    console.error(error);
  }
}

function updateResults(data) {
  document.getElementById("langResult").textContent = data.language || "-";
  document.getElementById("translatedText").textContent = data.translated || "-";
  document.getElementById("intentResult").textContent = data.intent || "-";
}
