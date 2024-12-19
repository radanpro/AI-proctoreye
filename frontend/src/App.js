import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AddStudent from "./students/AddStudent";
import StudentList from "./students/StudentList";
import CompareImage from "./components/CompareImage";
import SearchImage from "./components/SearchImage";
import SearchRealTime from "./components/SearchRealTime";

function Home() {
  return <h1>Welcome to Home Page</h1>;
}

function App() {
  return (
    <Router future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
      <div className="App">
        <nav className="bg-gray-800 p-4">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="text-white hover:text-gray-400">
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/add-student"
                className="text-white hover:text-gray-400"
              >
                Add Student
              </Link>
            </li>
            <li>
              <Link to="/students" className="text-white hover:text-gray-400">
                Student List
              </Link>
            </li>
            <li>
              <Link
                to="/compare-image"
                className="text-white hover:text-gray-400"
              >
                Compare Image
              </Link>
            </li>
            <li>
              <Link
                to="/search-image"
                className="text-white hover:text-gray-400"
              >
                Search Image
              </Link>
            </li>
            <li>
              <Link to="/camera" className="text-white hover:text-gray-400">
                Real Time
              </Link>
            </li>
          </ul>
        </nav>
        <div className="p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add-student" element={<AddStudent />} />
            <Route path="/students" element={<StudentList />} />
            <Route path="/compare-image" element={<CompareImage />} />
            <Route
              path="/camera"
              element={<SearchRealTime setCapturedImage={() => {}} />}
            />
            <Route path="/search-image" element={<SearchImage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
