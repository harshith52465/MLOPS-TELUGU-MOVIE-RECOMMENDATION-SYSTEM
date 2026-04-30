async function getRecommendations() {
  const movie = document.getElementById("movieInput").value;

  const response = await fetch("api/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ movie })
  });

  const data = await response.json();

  let html = "";

  if (data.recommendations) {
    data.recommendations.forEach(m => {
      html += `<div class="movie">${m}</div>`;
    });
  } else {
    html = `<div class="movie">${data.error}</div>`;
  }

  document.getElementById("results").innerHTML = html;
}
