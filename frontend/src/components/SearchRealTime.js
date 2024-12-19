import React, { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

const SearchRealTime = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [imageResults, setImageResults] = useState([]);
  const [flash, setFlash] = useState(false);
  const [devices, setDevices] = useState([]); // قائمة الأجهزة
  const [selectedDeviceId, setSelectedDeviceId] = useState(null); // الكاميرا المختارة

  // الحصول على قائمة الكاميرات المتاحة
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

  // بدء الكاميرا باستخدام الكاميرا المختارة
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

  // إيقاف الكاميرا
  const stopCamera = () => {
    if (cameraActive) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
    }
  };

  // دالة لالتقاط الصورة من الفيديو
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

  // إرسال الصورة إلى الخادم
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
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      {/* قائمة الكاميرات */}
      <div className="mt-4">
        <label htmlFor="camera-select" className="mr-2">
          اختر الكاميرا:
        </label>
        <select
          id="camera-select"
          onChange={(e) => setSelectedDeviceId(e.target.value)}
          value={selectedDeviceId || ""}
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
          >
            فتح الكاميرا
          </button>
        ) : (
          <button
            onClick={stopCamera}
            className="p-2 bg-red-500 text-white rounded ml-4"
          >
            إغلاق الكاميرا
          </button>
        )}
      </div>

      <div className="mt-4">
        <button
          onClick={captureImage}
          className="p-2 bg-blue-500 text-white rounded"
        >
          التقاط صورة
        </button>
      </div>

      <div
        style={{ position: "relative" }}
        className="border-4 border-sky-200 rounded-lg mt-6 m-2"
      >
        <video ref={videoRef} width="640" height="480" autoPlay />
        <canvas
          ref={canvasRef}
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            pointerEvents: "none",
            zIndex: -1,
          }}
        />

        {flash && (
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              backgroundColor: "white",
              opacity: 0.5,
              zIndex: 10,
            }}
          ></div>
        )}

        {loading && <p>جاري التحميل...</p>}
      </div>

      <div className="mt-4 flex">
        {imageResults.length > 0 ? (
          imageResults.map((result, index) => (
            <div key={index}>
              <h3>نتيجة {index + 1}</h3>
              {result.imageUrl ? (
                <img
                  src={result.imageUrl}
                  alt={`Result ${index + 1}`}
                  width="200"
                />
              ) : (
                <p>لا توجد صورة.</p>
              )}
              <p>{JSON.stringify(result)}</p>
            </div>
          ))
        ) : (
          <p>لا توجد نتائج بعد.</p>
        )}
      </div>
    </div>
  );
};

export default SearchRealTime;
