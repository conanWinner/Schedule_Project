let count = 0;
const tableBody = document.querySelector("#subjectTable tbody");
const subjectInput = document.getElementById("subject");
const suggestionBox = document.getElementById("suggestionBox");

// Gợi ý từ API giả (mock)
subjectInput.addEventListener("input", () => {
  const query = subjectInput.value.trim();
  if (!query) return (suggestionBox.innerHTML = "");

  const payload = { query };
  console.log("📤 Gửi dữ liệu đến API:", JSON.stringify(payload, null, 2));

  const mockResponse = {
    query: query,
    results: [
      {
        course_name: "Phân tích dữ liệu",
        sub_topic: "Pandas, trực quan hóa với Matplotlib"
      },
      {
        course_name: "Cơ sở dữ liệu",
        sub_topic: "SQL và thiết kế cơ sở dữ liệu"
      },
      {
        course_name: "Xử lý dữ liệu",
        sub_topic: ""
      },
      {
        course_name: "Kho dữ liệu",
        sub_topic: ""
      }
    ]
  };

  suggestionBox.innerHTML = "";
  mockResponse.results.forEach(item => {
    const suggestionText = item.sub_topic
      ? `${item.course_name} @ ${item.sub_topic}`
      : item.course_name;

    const li = document.createElement("li");
    li.textContent = suggestionText;
    li.onclick = () => {
      addRow(suggestionText);
      suggestionBox.innerHTML = "";
      subjectInput.value = "";
    };
    suggestionBox.appendChild(li);
  });
});

function addRow(name) {
  const existing = Array.from(tableBody.querySelectorAll("td:nth-child(2)")).some(td => td.textContent === name);
  if (existing) return;
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${++count}</td>
    <td>${name}</td>
    <td><button class="toggle-btn none" onclick="removeRow(this)">❌</button></td>
    <td><button class="toggle-btn none" onclick="toggleWant(this)">✔️</button></td>
  `;
  tableBody.appendChild(row);
}

function removeRow(btn) {
  const row = btn.closest("tr");
  row.remove();
  count--;
  Array.from(tableBody.children).forEach((row, idx) => {
    row.children[0].textContent = idx + 1;
  });
}

function toggleWant(btn) {
  btn.classList.toggle("want");
  btn.classList.toggle("none");
}

// Gửi API JSON khi nhấn nút
function submitForm() {
  const queries = [];
  Array.from(tableBody.querySelectorAll("tr")).forEach(row => {
    const name = row.children[1].textContent;
    const wantBtn = row.children[3].querySelector("button");
    if (wantBtn.classList.contains("want")) {
      queries.push(name);
    }
  });

  const prompt = document.getElementById("note-text").value.trim();
  const payload = {
    query: queries,
    prompt: prompt
  };

  console.log("📤 JSON gửi đến Schedule API:");
  console.log(JSON.stringify(payload, null, 2));
  window.location.href = "schedule_display.html";
  // 👉 Khi có API thật:
  /*
  fetch("http://127.0.0.1:5000/schedule", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => console.log("📥 Kết quả trả về từ API:", data))
    .catch(error => console.error("❌ Lỗi khi gọi API:", error));
  */
}
