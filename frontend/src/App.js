import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AddStudent from "./students/AddStudent";
import StudentList from "./students/StudentList";
import CompareImage from "./components/CompareImage";
import SearchImage from "./components/SearchImage";
import SearchRealTime from "./components/SearchRealTime";
import Layout from "./Layout";

function Home() {
  return <h1>Welcome to Home Page</h1>;
}

function App() {
  return (
    <Router future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
      <div className="App ">
        <div className="p-4 rounded-sm shadow-lg">
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/add-student" element={<AddStudent />} />
              <Route path="/students" element={<StudentList />} />
              <Route path="/compare-image" element={<CompareImage />} />
              <Route
                path="/camera"
                element={<SearchRealTime setCapturedImage={() => {}} />}
              />
              <Route path="/search-image" element={<SearchImage />} />
            </Route>
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
