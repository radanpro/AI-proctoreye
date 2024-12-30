import React, { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

const SearchRealTime = () => {
  const [loading, setLoading] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [imageResults, setImageResults] = useState([]);
  const [flash, setFlash] = useState(false);
  const [devices, setDevices] = useState([]); // قائمة الأجهزة
  const [selectedDeviceId, setSelectedDeviceId] = useState(null); // الكاميرا المختارة

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then((deviceInfos) => {
      const videoDevices = deviceInfos.filter(
        (device) => device.kind === "videoinput"
      );
      setDevices(videoDevices);
      if (videoDevices.length > 0) {
        setSelectedDeviceId(videoDevices[0].deviceId); // افتراضيًا الكاميرا الأولى
      }
    });
  }, []);

  const startCamera = () => {
    if (!cameraActive && selectedDeviceId) {
      navigator.mediaDevices
        .getUserMedia({
          video: {
            deviceId: { exact: selectedDeviceId },
            width: 1280,
            height: 720,
          },
        })
        .then((stream) => {
          videoRef.current.srcObject = stream;
          setCameraActive(true);
        })
        .catch((err) => {
          console.error("Error accessing webcam:", err);
        });
    }
  };

  const stopCamera = () => {
    if (cameraActive) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
    }
  };

  const captureImage = useCallback(() => {
    if (videoRef.current && canvasRef.current) {
      const videoWidth = videoRef.current.videoWidth;
      const videoHeight = videoRef.current.videoHeight;

      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const ctx = canvasRef.current.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);

      const imageData = canvasRef.current.toDataURL("image/jpeg", 1.0);

      setFlash(true);
      setTimeout(() => setFlash(false), 300);

      const byteString = atob(imageData.split(",")[1]);
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uintArray = new Uint8Array(arrayBuffer);
      for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([arrayBuffer], { type: "image/jpeg" });

      sendImageToServer(blob);
    }
  }, []);

  const sendImageToServer = async (imageBlob) => {
    const formData = new FormData();
    formData.append("image", imageBlob, "image.jpg");

    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/detect_face",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.data.status === "success") {
        const faceData = response.data.faceData || {};
        setImageResults((prevResults) => [...prevResults, faceData]);
      } else {
        console.error("Face detection failed:", response.data.message);
      }
    } catch (error) {
      console.error("Error in sending image:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "10px",
        boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
      }}
    >
      {/* قائمة الكاميرات */}
      <div className="mt-4">
        <label
          htmlFor="camera-select"
          className="mr-2"
          style={{ fontSize: "18px" }}
        >
          اختر الكاميرا:
        </label>
        <select
          id="camera-select"
          onChange={(e) => setSelectedDeviceId(e.target.value)}
          value={selectedDeviceId || ""}
          style={{
            padding: "10px",
            fontSize: "16px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        >
          {devices.map((device) => (
            <option key={device.deviceId} value={device.deviceId}>
              {device.label || `Camera ${device.deviceId}`}
            </option>
          ))}
        </select>
      </div>

      {/* أزرار التحكم بالكاميرا */}
      <div className="mt-4">
        {!cameraActive ? (
          <button
            onClick={startCamera}
            className="p-2 bg-green-500 text-white rounded"
            style={{ padding: "10px", fontSize: "16px", borderRadius: "5px" }}
          >
            فتح الكاميرا
          </button>
        ) : (
          <button
            onClick={stopCamera}
            className="p-2 bg-red-500 text-white rounded ml-4"
            style={{ padding: "10px", fontSize: "16px", borderRadius: "5px" }}
          >
            إغلاق الكاميرا
          </button>
        )}
      </div>

      <div className="mt-4">
        <button
          onClick={captureImage}
          className="p-2 bg-blue-500 text-white rounded"
          style={{ padding: "10px", fontSize: "16px", borderRadius: "5px" }}
        >
          التقاط صورة
        </button>
      </div>

      <div
        style={{
          position: "relative",
          padding: "20px",
          border: "1px solid #ccc",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
        }}
      >
        <video ref={videoRef} width="640" height="480" autoPlay />
        {/* <canvas
          ref={canvasRef}
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            pointerEvents: "none",
            zIndex: -1,
          }}
        /> */}

        {flash && (
          <div
            style={{
              position: "absolute",
              backgroundColor: "white",
              opacity: 0.5,
              zIndex: 10,
            }}
          ></div>
        )}

        {loading && <p style={{ fontSize: "18px" }}>جاري التحميل...</p>}
      </div>

      <div className="mt-4 flex">
        {imageResults.length > 0 ? (
          imageResults.map((result, index) => (
            <div
              key={index}
              style={{
                padding: "20px",
                border: "1px solid #ccc",
                borderRadius: "10px",
                boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
              }}
            >
              <h3 style={{ fontSize: "20px" }}>نتيجة {index + 1}</h3>
              {result.imageUrl ? (
                <img
                  className="mt-4 block justify-center w-64 h-64"
                  src={result.imageUrl}
                  alt={`Result ${index + 1}`}
                  width="100"
                  style={{ borderRadius: "10px" }}
                />
              ) : (
                <p style={{ fontSize: "18px" }}>لا توجد صورة.</p>
              )}
              <p style={{ fontSize: "16px" }}>{JSON.stringify(result)}</p>
            </div>
          ))
        ) : (
          <p style={{ fontSize: "18px" }}>لا توجد نتائج بعد.</p>
        )}
      </div>
    </div>
  );
};

export default SearchRealTime;
