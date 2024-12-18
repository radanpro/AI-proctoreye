import React, { useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const SearchImage = () => {
  const [capturedImage, setCapturedImage] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleCompare = async (e) => {
    e.preventDefault();

    if (!capturedImage) {
      setError("يرجى اختيار صورة للمقارنة");
      return;
    }

    setError("");
    setLoading(true);
    setResults([]);

    const formData = new FormData();
    formData.append("captured_image", capturedImage);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/search_image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.data.status === "success") {
        setResults(response.data.data); // Handle all results
      } else if (response.data.status === "error") {
        setError(response.data.message);
      }
    } catch (error) {
      if (error.response) {
        setError(
          `فشل الاتصال: ${error.response.data.message || error.message}`
        );
      } else {
        setError("فشلت عملية مقارنة الصور: تأكد من الاتصال بالخادم.");
      }
    } finally {
      setLoading(false);
      setCapturedImage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">مقارنة صورة الطالب</h2>
      <form onSubmit={handleCompare} className="space-y-4">
        {error && <p className="text-red-500 text-sm">{error}</p>}

        <div className="flex gap-4">
          <button
            type="button"
            className="w-1/2 p-2 rounded bg-blue-500 text-white"
          >
            اختر صورة
          </button>

          <Link
            to="/camera"
            className="w-1/2 p-2 rounded bg-blue-500 text-white"
          >
            فتح الكاميرا
          </Link>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={(e) => setCapturedImage(e.target.files[0])}
          className="w-full p-2 border border-gray-300 rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {loading ? "جاري المقارنة..." : "مقارنة الصورة"}
        </button>
      </form>

      {results.length > 0 && (
        <div className="mt-4">
          {results.map((result, index) => (
            <div
              key={index}
              className="p-4 mb-2 bg-blue-100 border border-blue-500 rounded"
            >
              <h3 className="text-lg font-semibold">
                رقم التسجيل: {result.registration_number}
              </h3>
              <h4 className="text-sm">المسافة:</h4>
              <p className="text-sm">distance: {result.distance}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchImage;
