const toggleBtn = document.getElementById("toggleBtn");
const sidebar = document.getElementById("sidebar");
const closeBtn = document.getElementById("closeSidebar");

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("-translate-x-full");
});

closeBtn.addEventListener("click", () => {
  sidebar.classList.add("-translate-x-full");
});
const diagnosisTitle = document.getElementById("diagnosisTitle");
const diagnosisDate = document.getElementById("diagnosisDate");
const diagnosisDescription = document.getElementById(
  "diagnosisDescription"
);
const diagnosisDetails = document.getElementById("diagnosisDetails");

  const diagnosisDataArray = [
{
  title: "Tomato Leaf Spot",
  date: "April 20, 2025",
  summary:
    "Detected early symptoms of fungal infection. Recommended copper-based treatment.",
  id: 1,
},
{
  title: "Cassava Mosaic Virus",
  date: "April 18, 2025",
  summary:
    "Viral infection detected. Isolate affected crops to reduce spread.",
  id: 2,
},
{
  title: "Potato Late Blight",
  date: "April 15, 2025",
  summary:
    "High confidence in late blight based on leaf pattern recognition.",
  id: 3,
},
{
title: "Corn Rootworm Infestation",
  date: "April 10, 2025",
  summary:
    "Detected root damage. Recommended insecticide application.",
  id: 4,
},
{
  title: "Rice Blast Disease",
  date: "April 5, 2025",
  summary:
    "Fungal infection detected. Recommended fungicide treatment.",
  id: 5,
},
{
  title: "Soybean Aphid Infestation",
  date: "April 1, 2025",
  summary:
    "High aphid population detected. Recommended insecticide application.",
  id: 6,
},
];

const diagnosisCardsContainer = document.querySelector(".diagnosis-cards");
diagnosisCardsContainer.innerHTML = ""; // Clear skeleton loaders

diagnosisDataArray.forEach((diagnosis) => {
const card = document.createElement("div");
card.className =
  "bg-white shadow-md rounded-lg p-4 mb-4 border-l-4 border-green-500";

card.innerHTML = `
  <div class="flex justify-between items-center mb-2">
    <h3 class="text-lg font-semibold text-gray-800">${diagnosis.title}</h3>
    <span class="text-sm text-gray-500">${diagnosis.date}</span>
  </div>
  <p class="text-gray-600 text-sm mb-2">${diagnosis.summary}</p>
  <a
    href="diagnosis-detail.html?id=${diagnosis.id}"
    class="text-green-700 text-sm hover:underline font-bold"
  >
    View Details
  </a>
`;

diagnosisCardsContainer.appendChild(card);
});

lucide.createIcons();
