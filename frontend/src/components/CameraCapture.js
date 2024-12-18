import React, { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

const CameraCapture = ({ setCapturedImage }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [imageResults, setImageResults] = useState([]);
  const [flash, setFlash] = useState(false); // لتمثيل وميض الفلاش
  // const [capturedImage, setCapturedImageState] = useState(null); // لتخزين الصورة الملتقطة

  // بدء الكاميرا
  const startCamera = () => {
    if (!cameraActive) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
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
      const ctx = canvasRef.current.getContext("2d");
      ctx.drawImage(
        videoRef.current,
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );

      // الحصول على الصورة الملتقطة
      const imageData = canvasRef.current.toDataURL("image/jpeg");
      // setCapturedImageState(imageData); // حفظ الصورة الملتقطة

      // إظهار وميض الكاميرا
      setFlash(true);
      setTimeout(() => setFlash(false), 300); // إيقاف الوميض بعد 300 ملي ثانية

      // تحويل الصورة إلى Blob قبل الإرسال
      const byteString = atob(imageData.split(",")[1]);
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uintArray = new Uint8Array(arrayBuffer);
      for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([arrayBuffer], { type: "image/jpeg" });

      // إرسال الصورة إلى الخادم
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
        setImageResults((prevResults) => [
          ...prevResults,
          response.data.faceData,
        ]);
      }
    } catch (error) {
      console.error("Error in sending image:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      // يمكن إضافة هنا الكود الخاص بالتقاط الصورة بشكل دوري إذا أردت
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div className="mt-4">
        {/* عرض زر تشغيل/إيقاف الكاميرا */}
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
        {/* زر التقاط الصورة */}
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
          width="640"
          height="480"
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            pointerEvents: "none", // تأكد من أن الـ canvas لا يعطل التفاعل مع الأزرار
            zIndex: -1, // جعل الـ canvas في الخلف
          }}
        />

        {/* إضافة تأثير الوميض */}
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
              zIndex: 10, // التأكد من أن الوميض فوق باقي العناصر
            }}
          ></div>
        )}

        {loading && <p>جاري التحميل...</p>}
      </div>

      <br />

      <div className="mt-4">
        {/* عرض الصورة الملتقطة */}
        {/* {capturedImage && (
          <div>
            <h3>الصورة الملتقطة</h3>
            <img src={capturedImage} alt="Captured" width="200" />
          </div>
        )} */}
      </div>

      <div className="mt-4 flex ">
        {/* عرض نتائج الكشف عن الوجوه */}
        {imageResults.length > 0 &&
          imageResults.map((result, index) => (
            <div key={index}>
              <h3>نتيجة {index + 1}</h3>
              <img
                src={result.imageUrl}
                alt={`Result ${index + 1}`}
                width="200"
              />
              <p>{JSON.stringify(result.faceData)}</p>
            </div>
          ))}
      </div>
    </div>
  );
};

export default CameraCapture;
