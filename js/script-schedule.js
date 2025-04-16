const loadingEl = document.createElement('p')
loadingEl.textContent = '🔄 Đang tạo thời khóa biểu...'
loadingEl.style.position = 'fixed'
loadingEl.style.top = '50%'
loadingEl.style.left = '50%'
loadingEl.style.transform = 'translate(-50%, -50%)'
loadingEl.style.fontSize = '24px'
loadingEl.style.fontWeight = 'bold'
document.body.appendChild(loadingEl)

// Lấy payload từ localStorage
const payload = JSON.parse(localStorage.getItem('schedule_payload'))

if (!payload) {
  loadingEl.remove()
  alert('⚠️ Không có dữ liệu truy vấn. Quay lại trang trước.')
} else {
  fetch('http://127.0.0.1:5001/api/convert', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      loadingEl.remove()
      renderSchedules(data.schedules)
    })
    .catch(err => {
      loadingEl.remove()
      console.error('❌ Lỗi API:', err)
      alert('❌ Không thể tạo thời khóa biểu.')
    })
}

function renderSchedules (schedules) {
  const days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday'
  ]
  const dayMapping = {
    'Thứ Hai': 'Monday',
    'Thứ Ba': 'Tuesday',
    'Thứ Tư': 'Wednesday',
    'Thứ Năm': 'Thursday',
    'Thứ Sáu': 'Friday',
    'Thứ Bảy': 'Saturday'
  }
  const periodLabels = [
    'Tiết 1: 07h30',
    'Tiết 2: 08h30',
    'Tiết 3: 09h30',
    'Tiết 4: 10h30',
    'Tiết 5: 11h30',
    'Tiết 6: 13h00',
    'Tiết 7: 14h00',
    'Tiết 8: 15h00',
    'Tiết 9: 16h00',
    'Tiết 10: 17h00'
  ]

  const wrapper = document.getElementById('wrapper')
  wrapper.innerHTML = ''

  schedules.forEach((scheduleObj, index) => {
    const timetableData = scheduleObj.schedule

    const container = document.createElement('div')
    container.className = 'timetable-container'
    container.innerHTML = `
        <h1>THỜI KHÓA BIỂU ${index + 1}</h1>
        <div class="score-display">Điểm: ${scheduleObj.score}</div>
        <div class="info-grid">
          <div class="info-block"><label>Tên HP:</label><input id="subject-name-${index}" readonly></div>
          <div class="info-block"><label>Giáo viên:</label><input id="subject-teacher-${index}" readonly></div>
          <div class="info-block"><label>Thời gian:</label><input id="subject-time-${index}" readonly></div>
          <div class="info-block"><label>Phòng:</label><input id="subject-room-${index}" readonly></div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Tiết</th>
              ${days.map(day => `<th>${day}</th>`).join('')}
            </tr>
          </thead>
          <tbody id="timetable-body-${index}"></tbody>
        </table>
      `
    wrapper.appendChild(container)

    const tbody = container.querySelector(`#timetable-body-${index}`)
    const inputs = {
      subject: container.querySelector(`#subject-name-${index}`),
      teacher: container.querySelector(`#subject-teacher-${index}`),
      time: container.querySelector(`#subject-time-${index}`),
      room: container.querySelector(`#subject-room-${index}`)
    }

    const rendered = Array.from({ length: 10 }, () =>
      Object.fromEntries(days.map(d => [d, false]))
    )

    for (let i = 1; i <= 10; i++) {
      const row = document.createElement('tr')
      const periodCell = document.createElement('td')
      periodCell.textContent = periodLabels[i - 1]
      periodCell.className = 'period-col'
      row.appendChild(periodCell)

      days.forEach(day => {
        if (rendered[i - 1][day]) return
        const cell = document.createElement('td')

        // Xử lý định dạng mới của dữ liệu
        for (const courseData of timetableData) {
          // courseData bây giờ là một mảng [tên_khóa_học, thông_tin_chi_tiết]
          const courseName = courseData[0]
          const info = courseData[1]

          const mappedDay = dayMapping[info.day]
          if (!mappedDay || mappedDay !== day) continue

          if (info.periods.includes(i)) {
            const isStart = i === Math.min(...info.periods)
            const rowspan = info.periods.length

            if (isStart) {
              cell.textContent = courseName
              cell.classList.add('filled', 'yellow')
              cell.setAttribute('rowspan', rowspan)

              // Thêm thông tin chi tiết cho hộp thông tin khi di chuột vào
              cell.addEventListener('mouseover', () => {
                inputs.subject.value = courseName
                inputs.teacher.value = info.teacher
                inputs.time.value = `${
                  periodLabels[info.periods[0] - 1].split(': ')[1]
                } - ${
                  periodLabels[info.periods[info.periods.length - 1] - 1].split(
                    ': '
                  )[1]
                }`
                inputs.room.value = `${info.area}.${info.room}`

                // Hiển thị thông tin bổ sung nếu có
                if (info.sub_topic) {
                  inputs.subject.value += ` (${info.sub_topic})`
                }
              })

              cell.addEventListener('mouseleave', () => {
                inputs.subject.value = ''
                inputs.teacher.value = ''
                inputs.time.value = ''
                inputs.room.value = ''
              })

              row.appendChild(cell)

              for (let r = 0; r < rowspan; r++) {
                if (i - 1 + r < 10) rendered[i - 1 + r][day] = true
              }
            }
            return
          }
        }

        if (!cell.hasAttribute('rowspan')) row.appendChild(cell)
      })

      tbody.appendChild(row)
    }
  })
}
