import React from "react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-100 p-4 h-screen rounded-lg shadow-lg">
      <div className="text-2xl font-bold mb-8">AI Exam</div>
      <nav className="space-y-4">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/add-student"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Add Student
        </NavLink>
        <NavLink
          to="/students"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Student List
        </NavLink>
        <NavLink
          to="/compare-image"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Compare Image
        </NavLink>
        <NavLink
          to="/search-image"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Search Image
        </NavLink>
        <NavLink
          to="/camera"
          className={({ isActive }) =>
            `block p-2 rounded-lg ${
              isActive ? "bg-blue-600 text-white" : "text-gray-700"
            }`
          }
        >
          Real Time
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
