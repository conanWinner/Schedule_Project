// 📦 MOCKED RESPONSE SIMULATOR (REPLACE WITH FETCH LATER)
const mockResponse = {
    schedules: [
      {
        schedule: [
          {
            subject: "Automat và ngôn ngữ hình thức",
            class_info: {
              name: "Automat và ngôn ngữ hình thức",
              class_index: "3",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "CLC_Kỹ thuật phần mềm",
              teacher: "TS.Nguyễn Đức Hiển",
              day: "Thứ Hai",
              periods: [1, 2],
              area: "K",
              room: "A113",
              class_size: 70
            }
          },
          {
            subject: "Bảo mật và an toàn hệ thống thông tin",
            class_info: {
              name: "Bảo mật và an toàn hệ thống thông tin",
              class_index: "2",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "VP_Công nghệ thông tin",
              teacher: "TS.Đặng Quang Hiển",
              day: "Thứ Hai",
              periods: [6, 7, 8],
              area: "V",
              room: "A214",
              class_size: 60
            }
          },
          {
            subject: "Cấu trúc dữ liệu và giải thuật",
            class_info: {
              name: "Cấu trúc dữ liệu và giải thuật",
              class_index: "1",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "JIT_Khoa học máy tính",
              teacher: "ThS.Lê Song Toàn",
              day: "Thứ Sáu",
              periods: [1, 2],
              area: "K",
              room: "A101",
              class_size: 90
            }
          }
        ],
        score: 1.0
      },
        
      {
        schedule: [
          {
            subject: "Automat và ngôn ngữ hình thức",
            class_info: {
              name: "Automat và ngôn ngữ hình thức",
              class_index: "2",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "CLC_Kỹ thuật phần mềm",
              teacher: "ThS.Dương Thị Mai Nga",
              day: "Thứ Tư",
              periods: [3, 4],
              area: "K",
              room: "A313",
              class_size: 75
            }
          },
          {
            subject: "Bảo mật và an toàn hệ thống thông tin",
            class_info: {
              name: "Bảo mật và an toàn hệ thống thông tin",
              class_index: "2",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "VP_Công nghệ thông tin",
              teacher: "TS.Đặng Quang Hiển",
              day: "Thứ Hai",
              periods: [6, 7, 8],
              area: "V",
              room: "A214",
              class_size: 60
            }
          },
          {
            subject: "Cấu trúc dữ liệu và giải thuật",
            class_info: {
              name: "Cấu trúc dữ liệu và giải thuật",
              class_index: "1",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "JIT_Khoa học máy tính",
              teacher: "ThS.Lê Song Toàn",
              day: "Thứ Sáu",
              periods: [1, 2],
              area: "K",
              room: "A101",
              class_size: 90
            }
          }
        ],
        score: 0.8
      },
      {
        schedule: [
          {
            subject: "Automat và ngôn ngữ hình thức",
            class_info: {
              name: "Automat và ngôn ngữ hình thức",
              class_index: "2",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "CLC_Kỹ thuật phần mềm",
              teacher: "ThS.Dương Thị Mai Nga",
              day: "Thứ Tư",
              periods: [6, 7],
              area: "K",
              room: "A310",
              class_size: 75
            }
          },
          {
            subject: "Bảo mật và an toàn hệ thống thông tin",
            class_info: {
              name: "Bảo mật và an toàn hệ thống thông tin",
              class_index: "2",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "VP_Công nghệ thông tin",
              teacher: "TS.Đặng Quang Hiển",
              day: "Thứ Hai",
              periods: [6, 7, 8],
              area: "V",
              room: "A214",
              class_size: 60
            }
          },
          {
            subject: "Cấu trúc dữ liệu và giải thuật",
            class_info: {
              name: "Cấu trúc dữ liệu và giải thuật",
              class_index: "1",
              language: "Tiếng Việt",
              field: "IT",
              sub_topic: "JIT_Khoa học máy tính",
              teacher: "ThS.Lê Song Toàn",
              day: "Thứ Sáu",
              periods: [8, 9],
              area: "K",
              room: "A101",
              class_size: 90
            }
          }
        ],
        score: 0.8
      }
      
    ],
    message: "Đã sắp xếp thành công"
  };
  
  // Gọi hàm renderSchedules từ mock

  

// Gọi hàm renderSchedules từ mock
const loadingEl = document.createElement("p");
loadingEl.textContent = "🔄 Đang tạo thời khóa biểu...";
loadingEl.style.position = "fixed";
loadingEl.style.top = "50%";
loadingEl.style.left = "50%";
loadingEl.style.transform = "translate(-50%, -50%)";
loadingEl.style.fontSize = "24px";
loadingEl.style.fontWeight = "bold";
document.body.appendChild(loadingEl);

setTimeout(() => {
  loadingEl.remove();
  renderSchedules(mockResponse.schedules.map(s => s.schedule));
}, 1000);

  
  // 👇 KHI DÙNG API THẬT => THAY = fetch như sau:
  // fetch("http://127.0.0.1:5000/schedule", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify(payload)
  // })
  //   .then(res => res.json())
  //   .then(data => {
  //     const schedules = data.schedules.map(s => s.schedule);
  //     renderSchedules(schedules);
  //   });
  
  function renderSchedules(demoSchedules) {
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const dayMapping = {
      "Thứ Hai": "Monday",
      "Thứ Ba": "Tuesday",
      "Thứ Tư": "Wednesday",
      "Thứ Năm": "Thursday",
      "Thứ Sáu": "Friday",
      "Thứ Bảy": "Saturday"
    };
    const periodLabels = [
      "Tiết 1: 07h30", "Tiết 2: 08h30", "Tiết 3: 09h30",
      "Tiết 4: 10h30", "Tiết 5: 11h30", "Tiết 6: 13h00",
      "Tiết 7: 14h00", "Tiết 8: 15h00", "Tiết 9: 16h00", "Tiết 10: 17h00"
    ];
  
    const wrapper = document.getElementById("wrapper");
    wrapper.innerHTML = "";
  
    demoSchedules.forEach((timetableData, index) => {
      const container = document.createElement("div");
      container.className = "timetable-container";
      container.innerHTML = `
        <h1>THỜI KHÓA BIỂU ${index + 1}</h1>
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
      `;
      wrapper.appendChild(container);
  
      const tbody = container.querySelector(`#timetable-body-${index}`);
      const inputs = {
        subject: container.querySelector(`#subject-name-${index}`),
        teacher: container.querySelector(`#subject-teacher-${index}`),
        time: container.querySelector(`#subject-time-${index}`),
        room: container.querySelector(`#subject-room-${index}`)
      };
  
      const rendered = Array.from({ length: 10 }, () => Object.fromEntries(days.map(d => [d, false])));
  
      for (let i = 1; i <= 10; i++) {
        const row = document.createElement("tr");
        const periodCell = document.createElement("td");
        periodCell.textContent = periodLabels[i - 1];
        periodCell.className = "period-col";
        row.appendChild(periodCell);
  
        days.forEach(day => {
          if (rendered[i - 1][day]) return;
          const cell = document.createElement("td");
  
          for (const data of timetableData) {
            const info = data.class_info;
            const mappedDay = dayMapping[info.day];
            if (!mappedDay || mappedDay !== day) continue;
            if (info.periods.includes(i)) {
              const isStart = i === Math.min(...info.periods);
              const rowspan = info.periods.length;
              if (isStart) {
                cell.textContent = info.name;
                cell.classList.add("filled", "yellow");
                cell.setAttribute("rowspan", rowspan);
                cell.addEventListener("mouseover", () => {
                  inputs.subject.value = info.name;
                  inputs.teacher.value = info.teacher;
                  inputs.time.value = `${periodLabels[info.periods[0] - 1].split(': ')[1]} - ${periodLabels[info.periods[info.periods.length - 1]].split(': ')[1]}`;
                  inputs.room.value = `${info.area}.${info.room}`;
                });
                cell.addEventListener("mouseleave", () => {
                  inputs.subject.value = "";
                  inputs.teacher.value = "";
                  inputs.time.value = "";
                  inputs.room.value = "";
                });
                row.appendChild(cell);
                for (let r = 0; r < rowspan; r++) {
                  if (i - 1 + r < 10) rendered[i - 1 + r][day] = true;
                }
              }
              return;
            }
          }
          if (!cell.hasAttribute("rowspan")) row.appendChild(cell);
        });
        tbody.appendChild(row);
      }
    });
  }