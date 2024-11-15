import React, { useState, useEffect } from "react";
import axios from "axios";

const StudentList = () => {
  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/students");
      setStudents(response.data);
    } catch (error) {
      console.error("Failed to fetch students", error);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Student List</h2>
      <ul className="space-y-2">
        {students.map((student) => (
          <li
            key={student.registration_number}
            className="p-2 border-b border-gray-200 flex items-center"
          >
            <img
              src={student.image_url} // استخدم image_url هنا
              alt={student.name}
              className="w-16 h-16 rounded-full mr-4"
            />
            <div>
              <p className="font-semibold">{student.name}</p>
              <p>{student.registration_number}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentList;
