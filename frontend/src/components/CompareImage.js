import React, { useState, useRef } from "react";
import axios from "axios";
import CameraCaptureOnly from "./CameraCaptureOnly";

const CompareImage = () => {
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [capturedImage, setCapturedImage] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [student_data, setStudent_data] = useState(null);
  const [verified, setVerified] = useState(null);
  const [message, setMessage] = useState(null);
  const [nextExamDate, setNextExamDate] = useState(null); // للتاريخ الأقرب
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [useCamera, setUseCamera] = useState(false);
  const [comparisonType, setComparisonType] = useState("deepface");

  const fileInputRef = useRef(null);

  const handleCompare = async (e) => {
    e.preventDefault();

    if (registrationNumber.length < 6) {
      setError("رقم التسجيل يجب أن يكون 6 أرقام على الأقل");
      return;
    }

    if (!capturedImage) {
      setError("يرجى اختيار صورة للمقارنة");
      return;
    }

    setError("");
    setLoading(true);
    setSimilarity(null);
    setVerified(null);
    setMessage(null);
    setNextExamDate(null);
    setStudent_data(null);

    const formData = new FormData();
    formData.append("registration_number", registrationNumber);
    formData.append("captured_image", capturedImage);

    let apiUrl = "";
    if (comparisonType === "deepface") {
      apiUrl = "http://127.0.0.1:8000/api/compare_image_deepface";
    } else if (comparisonType === "image_recognition") {
      apiUrl = "http://127.0.0.1:8000/api/compare_image_recognition";
    }

    try {
      const response = await axios.post(apiUrl, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      // console.log("response", response);
      // console.log("status", response.data.status);

      if (response.data.status === "success") {
        setMessage(response.data.message);
        setSimilarity(response.data.similarity || null);
        setStudent_data(response.data.student_data || null);
        setVerified(true);
        setNextExamDate(response.data.next_exam_date || null);
      } else if (response.data.status === "error") {
        setMessage(response.data.message);
        setSimilarity(response.data.similarity || null);
        setStudent_data(response.data.student_data || null);
        setVerified(false);
        setNextExamDate(response.data.next_exam_date || null);
      }
    } catch (error) {
      // console.error("success:", error.response.data.status);
      // console.error("message:", error.response.data.message);
      // console.error("Error response:", error.response);
      if (error.response) {
        setMessage(error.response.data.message);
        setStudent_data(error.response.data.student_data || null);
        setVerified(false);
        setNextExamDate(error.response.data.next_exam_date || null);
        setError(
          `فشل الاتصال: ${error.response.data.message || error.message}`
        );
      } else {
        setError("فشلت عملية مقارنة الصور: تأكد من الاتصال بالخادم.");
      }
    } finally {
      setLoading(false);
      setRegistrationNumber("");
      setCapturedImage(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
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
        {error && <p className="text-red-500 text-sm">{error}</p>}

        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => setUseCamera(false)}
            className={`w-1/2 p-2 rounded ${
              !useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            Choose Image
          </button>
          <button
            type="button"
            onClick={() => setUseCamera(true)}
            className={`w-1/2 p-2 rounded ${
              useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            Open Camera
          </button>
        </div>

        <div className="mt-4">
          <label className="mr-2">Choose Comparison Type:</label>
          <select
            value={comparisonType}
            onChange={(e) => setComparisonType(e.target.value)}
            className="p-2 border border-gray-300 rounded"
          >
            <option value="deepface">DeepFace</option>
            <option value="image_recognition">Image Recognition</option>
          </select>
        </div>

        {!useCamera && (
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => setCapturedImage(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded"
          />
        )}

        {useCamera && <CameraCaptureOnly setCapturedImage={setCapturedImage} />}

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {loading ? "جاري المقارنة..." : "Compare Image"}
        </button>
      </form>

      {message && (
        <div
          className={`mt-4 p-4 rounded ${
            verified ? "bg-green-100" : "bg-red-100"
          }`}
        >
          <h3 className="text-lg font-semibold">{message}</h3>
          {nextExamDate && (
            <p className="text-sm text-gray-600">
              Next Exam Date: {nextExamDate}
            </p>
          )}
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
      {student_data !== null && (
        <div>
          <div className="mt-6 p-4 bg-blue-100 border border-blue-500 rounded">
            <h1 className="felx text-center p-2 text-2xl font-semibold mt-[-30px] bg-white border border-gray-400  rounded-lg ">
              {" "}
              الطالب صاحب رقم القيد هو{" "}
            </h1>
            <h3 className="text-lg font-semibold">Name: {student_data.name}</h3>
            <h3 className="text-lg font-semibold">
              Registration Number: {student_data.registration_number}
            </h3>
            <h3 className="text-lg font-semibold">
              College: {student_data.college}
            </h3>
            <h3 className="text-lg font-semibold">
              Level: {student_data.level}
            </h3>
            <h3 className="text-lg font-semibold">
              Specialization: {student_data.specialization}
            </h3>
            <h3 className="text-lg font-semibold">
              Similarity: {similarity !== null ? similarity.toFixed(2) : "N/A"}%
            </h3>
            <h3 className="text-lg font-semibold">
              Verified: {verified ? "Yes" : "No"}
            </h3>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompareImage;
