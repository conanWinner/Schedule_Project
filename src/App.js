import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({});

  const handleSearch = async () => {
    if (!query) return;

    // Chuyển đổi chuỗi input thành danh sách môn học
    const queryList = query.split(",").map((q) => q.trim());

    const { data } = await axios.post("http://127.0.0.1:5001/search", { queries: queryList });
    setResults(data);
  };

  return (
    <div style={{ padding: 20, textAlign: "center" }}>
      <h2>🔍 Tìm kiếm nhiều môn học</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Nhập danh sách môn học (cách nhau bằng dấu phẩy)..."
        style={{ padding: 10, width: "60%" }}
      />
      <button onClick={handleSearch} style={{ marginLeft: 10, padding: 10 }}>
        Tìm kiếm
      </button>
      <div style={{ marginTop: 20 }}>
        {Object.keys(results).length > 0 ? (
          Object.entries(results).map(([query, courses]) => (
            <div key={query} style={{ marginBottom: 20 }}>
              <h3>🔍 Kết quả cho: <span style={{ color: "blue" }}>{query}</span></h3>
              <table border="1" style={{ margin: "auto", borderCollapse: "collapse", width: "80%" }}>
                <thead>
                  <tr>
                    <th style={{ padding: 10 }}>📚 Tên lớp học phần</th>
                    <th style={{ padding: 10 }}>🧑‍🏫 Giảng viên</th>
                    <th style={{ padding: 10 }}>🔥 Điểm</th>
                  </tr>
                </thead>
                <tbody>
                  {courses.map((course, index) => (
                    <tr key={index}>
                      <td style={{ padding: 10 }}>{course["Tên lớp học phần"]}</td>
                      <td style={{ padding: 10 }}>{course["Giảng viên"]}</td>
                      <td style={{ padding: 10 }}>{course.score.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))
        ) : (
          <p>Không tìm thấy kết quả.</p>
        )}
      </div>
    </div>
  );
}

export default App;
