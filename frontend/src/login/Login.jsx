// frontend/src/components/Login.jsx
import React, { useState } from "react";
import axios from "axios";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/api/login", {
        username,
        password,
      });
      alert(response.data.message);
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed, please try again.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-200">
      <form onSubmit={handleLogin} className="p-4 bg-white rounded shadow-md">
        <h2 className="text-xl mb-4">Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mb-2 p-2 w-full border"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mb-2 p-2 w-full border"
        />
        <button type="submit" className="p-2 w-full bg-blue-500 text-white">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
