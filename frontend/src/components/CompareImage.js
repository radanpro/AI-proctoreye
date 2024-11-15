import React, { useState } from "react";
import axios from "axios";

const CompareImage = () => {
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [capturedImage, setCapturedImage] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [message, setMessage] = useState(null);

  const handleCompare = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("registration_number", registrationNumber);
    formData.append("captured_image", capturedImage);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/compare_image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setSimilarity(response.data.average_similarity);
      setMessage(response.data.message);
    } catch (error) {
      alert("Failed to compare images");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Compare Student Image</h2>
      <form onSubmit={handleCompare} className="space-y-4">
        <input
          type="text"
          placeholder="Registration Number"
          value={registrationNumber}
          onChange={(e) => setRegistrationNumber(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
        />
        <input
          type="file"
          onChange={(e) => setCapturedImage(e.target.files[0])}
          className="w-full p-2 border border-gray-300 rounded"
        />
        <button
          type="submit"
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Compare Image
        </button>
      </form>
      {message !== null && (
        <div className="mt-4 p-4 bg-green-100 border border-green-500 rounded">
          <h3 className="text-lg font-semibold">
            similarity_threshold: {message} ^_^
          </h3>
        </div>
      )}
      <br />
      {similarity !== null && (
        <div className="mt-4 p-4 bg-blue-100 border border-blue-500 rounded">
          <h3 className="text-lg font-semibold">
            Similarity Percentage: {similarity}%
          </h3>
        </div>
      )}
    </div>
  );
};

export default CompareImage;
