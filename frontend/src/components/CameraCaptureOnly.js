import React, { useState, useRef, useCallback } from "react";

const CameraCaptureOnly = ({ setCapturedImage }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [flash, setFlash] = useState(false);

  // Start the camera
  const startCamera = () => {
    if (!cameraActive) {
      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { ideal: 1280 }, // العرض المثالي
            height: { ideal: 720 }, // الارتفاع المثالي
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

  // Stop the camera
  const stopCamera = () => {
    if (cameraActive) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
    }
  };

  // Capture image from video
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

      const imageData = canvasRef.current.toDataURL("image/jpeg");

      setFlash(true);
      setTimeout(() => setFlash(false), 300);

      // Pass the captured image to the parent component
      setCapturedImage(imageData);
    }
  }, [setCapturedImage]);

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div className="mt-4">
        {!cameraActive ? (
          <button
            type="button"
            onClick={startCamera}
            className="p-2 bg-green-500 text-white rounded"
          >
            فتح الكاميرا
          </button>
        ) : (
          <button
            type="button"
            onClick={stopCamera}
            className="p-2 bg-red-500 text-white rounded ml-4"
          >
            إغلاق الكاميرا
          </button>
        )}
      </div>

      <div className="mt-4">
        <button
          type="button"
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
      </div>
    </div>
  );
};

export default CameraCaptureOnly;
