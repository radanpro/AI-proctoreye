import React, { useState, useRef } from "react";
import axios from "axios";
import CameraCapture from "./CameraCapture";

const SearchImage = () => {
  const [capturedImage, setCapturedImage] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [distance, setDistance] = useState(null);
  const [verified, setVerified] = useState(null);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [useCamera, setUseCamera] = useState(false);
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
    setSimilarity(null);
    setVerified(null);
    setMessage(null);

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
        console.log(response.data);
        console.log(typeof response.data.distance);
        setMessage(response.data.registration_number);
        setDistance(response.data.distance || 0);
        setVerified(true);
      } else if (response.data.status === "error") {
        setMessage(response.data.message);
        setVerified(false);
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
            onClick={() => setUseCamera(false)}
            className={`w-1/2 p-2 rounded ${
              !useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            اختر صورة
          </button>
          <button
            type="button"
            onClick={() => setUseCamera(true)}
            className={`w-1/2 p-2 rounded ${
              useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            فتح الكاميرا
          </button>
        </div>

        {!useCamera && (
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => setCapturedImage(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded"
          />
        )}

        {useCamera && <CameraCapture setCapturedImage={setCapturedImage} />}

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {loading ? "جاري المقارنة..." : "مقارنة الصورة"}
        </button>
      </form>

      {message && (
        <div
          className={`mt-4 p-4 rounded ${
            verified ? "bg-green-100" : "bg-red-100"
          }`}
        >
          <h3 className="text-lg font-semibold">{message}</h3>
        </div>
      )}

      {distance !== null && (
        <div
          className={`mt-4 p-4 rounded ${
            verified ? "bg-green-100" : "bg-red-100"
          }`}
        >
          <h3 className="text-lg font-semibold">
            {" "}
            distance : {distance ?? "0"}
          </h3>
        </div>
      )}

      {similarity !== null && (
        <div className="mt-4 p-4 bg-blue-100 border border-blue-500 rounded">
          <h3 className="text-lg font-semibold">
            Similarity: {similarity.toFixed(2)}%
          </h3>
          <h3 className="text-lg font-semibold">
            Verified: {verified ? "Yes" : "No"}
          </h3>
        </div>
      )}
    </div>
  );
};

export default SearchImage;
