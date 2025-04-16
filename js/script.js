let count = 0
const tableBody = document.querySelector('#subjectTable tbody')
const subjectInput = document.getElementById('subject')
const suggestionBox = document.getElementById('suggestionBox')

// Gợi ý từ API giả (mock)
subjectInput.addEventListener('input', () => {
  const query = subjectInput.value.trim()
  if (!query) return (suggestionBox.innerHTML = '')

  const payload = { query }

  fetch('http://127.0.0.1:5000/api/search-recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
    .then(response => {
      if (!response.ok) throw new Error('Lỗi từ server!')
      return response.json()
    })
    .then(data => {
      suggestionBox.innerHTML = ''

      const seen = new Set()

      ;(data.results || []).forEach(item => {
        const courseName = item.course_name
          ? String(item.course_name).trim()
          : ''
        const subTopic = item.sub_topic ? String(item.sub_topic).trim() : ''

        // Nếu không có courseName thì bỏ qua luôn
        if (!courseName) return

        const suggestionText = subTopic
          ? `${courseName} @ ${subTopic}`
          : courseName

        if (seen.has(suggestionText)) return
        seen.add(suggestionText)

        const li = document.createElement('li')
        li.textContent = suggestionText
        li.onclick = () => {
          addRow(suggestionText)
          suggestionBox.innerHTML = ''
          subjectInput.value = ''
        }
        suggestionBox.appendChild(li)
      })

      if (suggestionBox.innerHTML === '') {
        suggestionBox.innerHTML = '<li>Không tìm thấy kết quả phù hợp.</li>'
      }
    })
    .catch(error => {
      console.error('❌ Lỗi khi gọi API:', error)
      suggestionBox.innerHTML = '<li>Không thể tải gợi ý...</li>'
    })
})

function addRow (name) {
  const existing = Array.from(
    tableBody.querySelectorAll('td:nth-child(2)')
  ).some(td => td.textContent === name)
  if (existing) return
  const row = document.createElement('tr')
  row.innerHTML = `
    <td>${++count}</td>
    <td>${name}</td>
    <td><button class="toggle-btn none" onclick="removeRow(this)">❌</button></td>
    <td><button class="toggle-btn none" onclick="toggleWant(this)">✔️</button></td>
  `
  tableBody.appendChild(row)
}

function removeRow (btn) {
  const row = btn.closest('tr')
  row.remove()
  count--
  Array.from(tableBody.children).forEach((row, idx) => {
    row.children[0].textContent = idx + 1
  })
}

function toggleWant (btn) {
  btn.classList.toggle('want')
  btn.classList.toggle('none')
}

function submitForm () {
  const queries = []
  Array.from(tableBody.querySelectorAll('tr')).forEach(row => {
    const name = row.children[1].textContent
    const wantBtn = row.children[3].querySelector('button')
    if (wantBtn.classList.contains('want')) {
      queries.push(name)
    }
  })

  const prompt = document.getElementById('note-text').value.trim()
  const payload = {
    queries: queries,
    prompt: prompt
  }

  // 👉 Lưu vào localStorage
  localStorage.setItem('schedule_payload', JSON.stringify(payload))

  // 👉 Chuyển trang (trang này sẽ gọi API)
  window.location.href = 'schedule_display.html'
}
